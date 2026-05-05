import re
import string
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib


class EMSCADPreprocessor:
    """
    Preprocessor for the EMSCAD (Employment Scam Aegean Dataset).
    Handles real dataset columns: title, location, department, company_profile,
    description, requirements, benefits, telecommuting, has_company_logo,
    has_questions, employment_type, required_experience, required_education,
    industry, function, fraudulent.
    """

    TEXT_COLUMNS = [
        "title", "location", "department", "company_profile",
        "description", "requirements", "benefits",
    ]
    CATEGORICAL_COLUMNS = [
        "employment_type", "required_experience",
        "required_education", "industry", "function",
    ]
    BOOLEAN_COLUMNS = [
        "telecommuting", "has_company_logo", "has_questions",
    ]
    SUSPICIOUS_KEYWORDS = [
        "work from home", "no experience needed", "quick cash",
        "earn money fast", "immediate start", "guaranteed income",
        "no interview", "wire transfer", "pay upfront", "training fee",
        "send money", "cashier check", "package reshipment",
        "secret shopper", "easy money", "unlimited earning",
        "bank account", "social security number", "credit card",
        "pay before", "registration fee", "processing fee",
    ]

    def __init__(self, max_features: int = 5000):
        self.max_features = max_features
        self.tfidf = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),
            stop_words="english",
            min_df=2,
        )
        self.label_encoders: dict[str, LabelEncoder] = {}
        self.scaler = StandardScaler()
        self._fit_done = False

    @staticmethod
    def clean_text(text: str) -> str:
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"\d+", "", text)
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def extract_text_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Combine all text fields into a single document per row."""
        df = df.copy()
        for col in self.TEXT_COLUMNS:
            if col in df.columns:
                df[col] = df[col].apply(self.clean_text)

        df["combined_text"] = (
            df.get("title", "")
            + " " + df.get("location", "")
            + " " + df.get("department", "")
            + " " + df.get("company_profile", "")
            + " " + df.get("description", "")
            + " " + df.get("requirements", "")
            + " " + df.get("benefits", "")
        ).str.strip()

        df["text_length"] = df["combined_text"].apply(len)
        df["word_count"] = df["combined_text"].apply(lambda x: len(x.split()))

        for kw in self.SUSPICIOUS_KEYWORDS:
            df[f"kw_{kw.replace(' ', '_')}"] = df["combined_text"].str.contains(
                kw, case=False, na=False
            ).astype(int)

        return df

    def extract_meta_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col in self.BOOLEAN_COLUMNS:
            if col in df.columns:
                df[col] = df[col].fillna(0).astype(int)
            else:
                df[col] = 0

        for col in self.CATEGORICAL_COLUMNS:
            if col not in df.columns:
                df[col] = "unknown"
            else:
                df[col] = df[col].fillna("unknown").astype(str)
        return df

    def fit(self, df: pd.DataFrame) -> "EMSCADPreprocessor":
        df = self.extract_text_features(df)
        df = self.extract_meta_features(df)

        self.tfidf.fit(df["combined_text"])

        for col in self.CATEGORICAL_COLUMNS:
            le = LabelEncoder()
            le.fit(df[col])
            self.label_encoders[col] = le

        meta_cols = self.BOOLEAN_COLUMNS + ["text_length", "word_count"]
        meta_cols += [f"kw_{kw.replace(' ', '_')}" for kw in self.SUSPICIOUS_KEYWORDS]
        self.scaler.fit(df[meta_cols].values)

        self._fit_done = True
        return self

    def transform(self, df: pd.DataFrame) -> tuple[np.ndarray, pd.Series | None]:
        if not self._fit_done:
            raise RuntimeError("Preprocessor must be fit before transform.")

        df = self.extract_text_features(df)
        df = self.extract_meta_features(df)

        tfidf_matrix = self.tfidf.transform(df["combined_text"])

        categorical_encoded = []
        for col in self.CATEGORICAL_COLUMNS:
            le = self.label_encoders[col]
            values = df[col].apply(lambda x: x if x in le.classes_ else "unknown")
            categorical_encoded.append(le.transform(values))
        cat_matrix = np.column_stack(categorical_encoded)

        meta_cols = self.BOOLEAN_COLUMNS + ["text_length", "word_count"]
        meta_cols += [f"kw_{kw.replace(' ', '_')}" for kw in self.SUSPICIOUS_KEYWORDS]
        meta_matrix = self.scaler.transform(df[meta_cols].values)

        X = np.hstack([tfidf_matrix.toarray(), cat_matrix, meta_matrix])

        y = df["fraudulent"].astype(int) if "fraudulent" in df.columns else None
        return X, y

    def fit_transform(self, df: pd.DataFrame) -> tuple[np.ndarray, pd.Series]:
        return self.fit(df).transform(df)

    def save(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.tfidf, path / "tfidf.joblib")
        joblib.dump(self.label_encoders, path / "label_encoders.joblib")
        joblib.dump(self.scaler, path / "scaler.joblib")
        with open(path / "suspicious_keywords.pkl", "wb") as f:
            pickle.dump(self.SUSPICIOUS_KEYWORDS, f)

    @classmethod
    def load(cls, path: Path) -> "EMSCADPreprocessor":
        inst = cls()
        inst.tfidf = joblib.load(path / "tfidf.joblib")
        inst.label_encoders = joblib.load(path / "label_encoders.joblib")
        inst.scaler = joblib.load(path / "scaler.joblib")
        with open(path / "suspicious_keywords.pkl", "rb") as f:
            inst.SUSPICIOUS_KEYWORDS = pickle.load(f)
        inst._fit_done = True
        return inst
