import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from app.core.config import settings
from app.ml_models.preprocess import EMSCADPreprocessor

warnings.filterwarnings("ignore")


def load_emscad_data(raw_path: Path) -> pd.DataFrame:
    csv_path = raw_path / "fake_job_postings.csv"
    if not csv_path.exists():
        raise FileNotFoundError(
            f"EMSCAD dataset not found at {csv_path}. "
            "Download from Kaggle: https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction"
        )
    df = pd.read_csv(csv_path)
    return df


def train_ml_models(
    data_path: Path | None = None,
    artifacts_dir: Path | None = None,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict[str, dict[str, float]]:
    data_path = data_path or (Path(__file__).resolve().parent.parent.parent.parent.parent / "data" / "raw")
    artifacts_dir = artifacts_dir or settings.MODEL_DIR
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    df = load_emscad_data(data_path)
    print(f"Loaded EMSCAD dataset: {len(df)} rows, {df.shape[1]} columns")
    print(f"Real class distribution:\n{df['fraudulent'].value_counts()}")

    preprocessor = EMSCADPreprocessor(max_features=5000)
    X, y = preprocessor.fit_transform(df)
    preprocessor.save(artifacts_dir / "preprocessor")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    smote = SMOTE(random_state=random_state)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    print(f"After SMOTE: {pd.Series(y_train_res).value_counts().to_dict()}")

    results = {}

    # Random Forest
    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=20,
        class_weight="balanced_subsample",
        random_state=random_state,
        n_jobs=-1,
    )
    rf.fit(X_train_res, y_train_res)
    rf_pred = rf.predict(X_test)
    rf_proba = rf.predict_proba(X_test)[:, 1]
    results["random_forest"] = evaluate("Random Forest", y_test, rf_pred, rf_proba)
    joblib.dump(rf, artifacts_dir / "random_forest.joblib")

    # XGBoost
    xgb = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
        random_state=random_state,
        n_jobs=-1,
        eval_metric="logloss",
    )
    xgb.fit(X_train_res, y_train_res)
    xgb_pred = xgb.predict(X_test)
    xgb_proba = xgb.predict_proba(X_test)[:, 1]
    results["xgboost"] = evaluate("XGBoost", y_test, xgb_pred, xgb_proba)
    joblib.dump(xgb, artifacts_dir / "xgboost.joblib")

    best_model_name = max(results, key=lambda k: results[k]["f1_score"])
    print(f"\nBest model: {best_model_name} with F1={results[best_model_name]['f1_score']:.4f}")

    with open(artifacts_dir / "metrics.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


def evaluate(model_name: str, y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> dict[str, float]:
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_proba)),
    }
    print(f"\n{model_name} Results:")
    print(classification_report(y_true, y_pred, target_names=["Real", "Fraudulent"]))
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    return metrics


if __name__ == "__main__":
    train_ml_models()
