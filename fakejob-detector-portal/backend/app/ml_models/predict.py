import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import requests
import torch
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.core.config import settings
from app.ml_models.preprocess import EMSCADPreprocessor


class FraudPredictor:
    def __init__(self, artifacts_dir: Path | None = None):
        self.artifacts_dir = artifacts_dir or settings.MODEL_DIR
        self.preprocessor = EMSCADPreprocessor.load(self.artifacts_dir / "preprocessor")
        self.rf = joblib.load(self.artifacts_dir / "random_forest.joblib")
        self.xgb = joblib.load(self.artifacts_dir / "xgboost.joblib")

        metrics_path = self.artifacts_dir / "metrics.json"
        if metrics_path.exists():
            with open(metrics_path) as f:
                self.metrics = json.load(f)
        else:
            self.metrics = {"random_forest": {"f1_score": 0.85}, "xgboost": {"f1_score": 0.87}}

        # Load DistilBERT if fine-tuned artifacts exist
        self.bert_tokenizer = None
        self.bert_model = None
        bert_dir = self.artifacts_dir / "distilbert"
        if (bert_dir / "pytorch_model.bin").exists() or (bert_dir / "model.safetensors").exists():
            self.bert_tokenizer = AutoTokenizer.from_pretrained(str(bert_dir))
            self.bert_model = AutoModelForSequenceClassification.from_pretrained(str(bert_dir))
            self.bert_model.eval()

    def predict_structured(self, job: dict) -> dict:
        df = pd.DataFrame([job])
        X, _ = self.preprocessor.transform(df)

        rf_proba = self.rf.predict_proba(X)[0]
        xgb_proba = self.xgb.predict_proba(X)[0]

        rf_f1 = self.metrics.get("random_forest", {}).get("f1_score", 0.5)
        xgb_f1 = self.metrics.get("xgboost", {}).get("f1_score", 0.5)
        total = rf_f1 + xgb_f1
        w_rf, w_xgb = rf_f1 / total, xgb_f1 / total

        ensemble_proba = w_rf * rf_proba[1] + w_xgb * xgb_proba[1]
        is_fraudulent = bool(ensemble_proba > 0.5)

        result = {
            "is_fraudulent": is_fraudulent,
            "confidence_score": float(round(ensemble_proba, 4)),
            "risk_percentage": float(round(ensemble_proba * 100, 2)),
            "model_used": "ensemble_rf_xgb",
            "rf_proba": float(round(rf_proba[1], 4)),
            "xgb_proba": float(round(xgb_proba[1], 4)),
        }

        # Include DistilBERT if available for a three-model ensemble
        if self.bert_model and self.bert_tokenizer:
            bert_proba = self._predict_bert(job.get("description", "") + " " + job.get("title", ""))
            bert_f1 = self.metrics.get("distilbert", {}).get("f1_score", 0.5)
            total_f1 = rf_f1 + xgb_f1 + bert_f1
            ensemble_proba_3 = (rf_f1 / total_f1) * rf_proba[1] + (xgb_f1 / total_f1) * xgb_proba[1] + (bert_f1 / total_f1) * bert_proba
            result = {
                "is_fraudulent": bool(ensemble_proba_3 > 0.5),
                "confidence_score": float(round(ensemble_proba_3, 4)),
                "risk_percentage": float(round(ensemble_proba_3 * 100, 2)),
                "model_used": "ensemble_rf_xgb_bert",
                "rf_proba": float(round(rf_proba[1], 4)),
                "xgb_proba": float(round(xgb_proba[1], 4)),
                "bert_proba": float(round(bert_proba, 4)),
            }

        return result

    def _predict_bert(self, text: str) -> float:
        inputs = self.bert_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=512
        )
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
        proba = float(outputs.logits.softmax(dim=-1)[0][1].item())
        return proba

    @staticmethod
    def scrape_job_url(url: str, timeout: int = 15) -> dict:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        title = soup.find("title")
        title_text = title.get_text(strip=True) if title else ""

        description = ""
        for selector in ["meta[name='description']", ".job-description", "#job-description", "[data-testid='job-description']", ".description"]:
            el = soup.select_one(selector)
            if el:
                description = el.get_text(strip=True, separator=" ")
                break

        company = ""
        for selector in [".company-name", "[data-testid='company-name']", ".employer", "#company"]:
            el = soup.select_one(selector)
            if el:
                company = el.get_text(strip=True)
                break

        return {
            "title": title_text,
            "description": description,
            "company_profile": company,
            "location": "",
            "department": "",
            "salary_range": "",
            "requirements": "",
            "benefits": "",
            "telecommuting": False,
            "has_company_logo": False,
            "has_questions": False,
            "employment_type": "",
            "required_experience": "",
            "required_education": "",
            "industry": "",
            "function": "",
            "source_url": url,
        }
