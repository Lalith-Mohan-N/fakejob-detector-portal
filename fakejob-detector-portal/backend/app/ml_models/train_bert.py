import warnings
from pathlib import Path

import pandas as pd
import torch
from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)

from app.core.config import settings
from app.ml_models.preprocess import EMSCADPreprocessor

warnings.filterwarnings("ignore")


def load_and_prepare_bert_data(csv_path: Path | None = None, max_length: int = 512):
    if csv_path is None:
        csv_path = (
            Path(__file__).resolve().parent.parent.parent.parent.parent
            / "data"
            / "raw"
            / "fake_job_postings.csv"
        )
    df = pd.read_csv(csv_path)

    preprocessor = EMSCADPreprocessor()
    df = preprocessor.extract_text_features(df)
    df["text"] = df["combined_text"].str[:max_length]
    df["label"] = df["fraudulent"].astype(int)

    train_df, test_df = train_test_split(
        df[["text", "label"]], test_size=0.2, stratify=df["label"], random_state=42
    )
    return Dataset.from_pandas(train_df), Dataset.from_pandas(test_df)


def tokenize_function(examples, tokenizer, max_length: int = 512):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=max_length,
    )


def train_distilbert(
    model_name: str = "distilbert-base-uncased",
    output_dir: Path | None = None,
    epochs: int = 3,
    batch_size: int = 16,
):
    output_dir = output_dir or (settings.MODEL_DIR / "distilbert")
    output_dir.mkdir(parents=True, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=2
    )

    train_dataset, test_dataset = load_and_prepare_bert_data()
    train_dataset = train_dataset.map(
        lambda x: tokenize_function(x, tokenizer), batched=True
    )
    test_dataset = test_dataset.map(
        lambda x: tokenize_function(x, tokenizer), batched=True
    )

    train_dataset = train_dataset.rename_column("label", "labels")
    test_dataset = test_dataset.rename_column("label", "labels")
    train_dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])
    test_dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=epochs,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_dir=str(output_dir / "logs"),
        logging_steps=50,
        seed=42,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )

    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"DistilBERT model saved to {output_dir}")
    return trainer


if __name__ == "__main__":
    train_distilbert()
