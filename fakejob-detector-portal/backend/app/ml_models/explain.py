import numpy as np
import pandas as pd
import shap
import joblib
from pathlib import Path
from app.core.config import settings
from app.ml_models.preprocess import EMSCADPreprocessor


class Explainer:
    def __init__(self, artifacts_dir: Path | None = None):
        self.artifacts_dir = artifacts_dir or settings.MODEL_DIR
        self.preprocessor = EMSCADPreprocessor.load(self.artifacts_dir / "preprocessor")
        self.rf = joblib.load(self.artifacts_dir / "random_forest.joblib")
        self.xgb = joblib.load(self.artifacts_dir / "xgboost.joblib")

    def explain_structured(self, job: dict) -> dict:
        df = pd.DataFrame([job])
        X, _ = self.preprocessor.transform(df)

        explainer_rf = shap.TreeExplainer(self.rf)
        shap_values_rf = explainer_rf.shap_values(X)
        if isinstance(shap_values_rf, list):
            shap_values_rf = shap_values_rf[1]

        top_indices = np.argsort(-np.abs(shap_values_rf[0]))[:10]
        feature_importance = []
        feature_names = self._get_feature_names()

        for idx in top_indices:
            feature_importance.append({
                "feature": feature_names[idx] if idx < len(feature_names) else f"feature_{idx}",
                "importance": round(float(shap_values_rf[0][idx]), 4),
            })

        suspicious_phrases = self._detect_suspicious_phrases(job)
        return {
            "suspicious_phrases": suspicious_phrases,
            "feature_importance": feature_importance,
            "shap_summary": "Top features driving prediction based on real EMSCAD patterns",
        }

    def _get_feature_names(self) -> list[str]:
        tfidf_names = self.preprocessor.tfidf.get_feature_names_out().tolist()
        cat_names = self.preprocessor.CATEGORICAL_COLUMNS
        meta_names = (
            self.preprocessor.BOOLEAN_COLUMNS
            + ["text_length", "word_count"]
            + [f"kw_{kw.replace(' ', '_')}" for kw in self.preprocessor.SUSPICIOUS_KEYWORDS]
        )
        return tfidf_names + cat_names + meta_names

    @staticmethod
    def _detect_suspicious_phrases(job: dict) -> list[dict]:
        text = " ".join(str(job.get(k, "")) for k in ["title", "description", "requirements", "benefits", "company_profile"])
        text = text.lower()
        keywords = [
            "work from home", "no experience needed", "quick cash",
            "earn money fast", "immediate start", "guaranteed income",
            "no interview", "wire transfer", "pay upfront", "training fee",
            "send money", "cashier check", "package reshipment",
            "secret shopper", "easy money", "unlimited earning",
            "bank account", "social security number", "credit card",
            "pay before", "registration fee", "processing fee",
        ]
        found = []
        for kw in keywords:
            if kw in text:
                found.append({"phrase": kw, "severity": "high"})
        return found[:5]
