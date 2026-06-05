# ════════════════════════════════════════════════════════════════
# TRANSFORMER INFERENCE — DistilBERT Fine-Tuning
# ════════════════════════════════════════════════════════════════

import os
import json
import time
import numpy as np
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TRANSFORMER_DIR = os.path.join(BASE_DIR, "transformer_model")


def is_transformer_available():
    """Check if transformer model files exist."""
    required = ["config.json", "tokenizer.json", "model.safetensors", "label_map.json"]
    return all(os.path.exists(os.path.join(TRANSFORMER_DIR, f)) for f in required)


@st.cache_resource(show_spinner=False)
def load_transformer_model():
    """Load the fine-tuned DistilBERT model and tokenizer."""
    if not is_transformer_available():
        return None, None, None

    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch

        tokenizer = AutoTokenizer.from_pretrained(TRANSFORMER_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(TRANSFORMER_DIR)
        model.eval()

        # Load label map
        label_map_path = os.path.join(TRANSFORMER_DIR, "label_map.json")
        with open(label_map_path, "r") as f:
            label_map = json.load(f)

        return model, tokenizer, label_map
    except Exception as e:
        st.warning(f"⚠️ Gagal memuat model Transformer: {e}")
        return None, None, None


def predict_transformer(text):
    """Run inference with the fine-tuned DistilBERT model.
    
    Returns:
        dict with keys: label, class_name, probabilities, confidence, inference_time
        or None if model not available
    """
    model, tokenizer, label_map = load_transformer_model()
    if model is None:
        return None

    try:
        import torch

        t0 = time.time()

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1).squeeze().cpu().numpy()

        pred_id = int(probs.argmax())
        id2label = label_map.get("id2label", {})
        class_name = id2label.get(str(pred_id), f"Class {pred_id}")
        confidence = float(probs[pred_id]) * 100

        inference_time = time.time() - t0

        return {
            "label": pred_id,
            "class_name": class_name,
            "probabilities": probs.tolist(),
            "confidence": confidence,
            "inference_time": inference_time,
        }
    except Exception as e:
        return {"error": str(e)}


def evaluate_transformer(X_test_texts, y_test):
    """Evaluate transformer on test set for metrics comparison."""
    model, tokenizer, label_map = load_transformer_model()
    if model is None:
        return None

    try:
        import torch
        from sklearn.metrics import (
            accuracy_score, precision_score, recall_score,
            f1_score, confusion_matrix, classification_report
        )

        t0 = time.time()
        y_pred = []
        y_prob = []

        # Batch inference
        batch_size = 32
        texts = list(X_test_texts)
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            inputs = tokenizer(
                batch,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            with torch.no_grad():
                outputs = model(**inputs)
                probs = torch.softmax(outputs.logits, dim=-1).cpu().numpy()
                preds = probs.argmax(axis=-1).tolist()
                y_pred.extend(preds)
                y_prob.extend(probs.tolist())

        inference_time = time.time() - t0
        y_pred = list(y_pred)
        y_prob = np.array(y_prob)

        return {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average="macro", zero_division=0),
            "recall": recall_score(y_test, y_pred, average="macro", zero_division=0),
            "f1_score": f1_score(y_test, y_pred, average="macro", zero_division=0),
            "cm": confusion_matrix(y_test, y_pred),
            "y_pred": y_pred,
            "y_prob": y_prob,
            "report": classification_report(y_test, y_pred, output_dict=True, zero_division=0),
            "inference_time": inference_time,
            "model_type": "DistilBERT Fine-Tuning",
            "feature_type": "DistilBERT",
            "group": "Transformer Fine-Tuning",
        }
    except Exception as e:
        st.warning(f"⚠️ Gagal evaluasi Transformer: {e}")
        return None
