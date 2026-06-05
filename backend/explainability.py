# ════════════════════════════════════════════════════════════════
# EXPLAINABILITY — Feature Importance & Interpretation
# ════════════════════════════════════════════════════════════════

import numpy as np
import pandas as pd


def get_dt_feature_importance(model, feature_names, top_n=20):
    """Get top feature importances from a Decision Tree model."""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    top_features = [feature_names[i] for i in indices]
    top_importances = [float(importances[i]) for i in indices]
    return top_features, top_importances


def get_keyword_contribution(text, vectorizer, model, le, top_n=10):
    """Analyze per-word contribution for a prediction (classical features only)."""
    from backend.data_loader import clean_text

    clean = clean_text(text)
    words = clean.split()

    # Full prediction
    full_vec = vectorizer.transform([clean])
    full_pred = model.predict(full_vec)[0]
    try:
        full_proba = model.predict_proba(full_vec)[0]
    except:
        full_proba = None

    features = vectorizer.get_feature_names_out()
    feature_set = set(features)

    contributions = []
    for word in words:
        if word in feature_set:
            # Check if removing this word changes confidence
            remaining = " ".join([w for w in words if w != word])
            if remaining.strip():
                reduced_vec = vectorizer.transform([remaining])
                try:
                    reduced_proba = model.predict_proba(reduced_vec)[0]
                    if full_proba is not None:
                        contrib = float(full_proba[full_pred] - reduced_proba[full_pred])
                    else:
                        contrib = 0.0
                except:
                    contrib = 0.0
            else:
                contrib = 0.0

            contributions.append({
                "word": word,
                "contribution": contrib,
                "in_vocab": True
            })
        else:
            contributions.append({
                "word": word,
                "contribution": 0.0,
                "in_vocab": False
            })

    # Sort by absolute contribution
    contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)
    return contributions[:top_n], full_pred, full_proba


def get_top_words_per_class(vectorizer, X_matrix, y, class_names, top_n=15):
    """Get top discriminative words per class."""
    features = vectorizer.get_feature_names_out()
    result = {}

    for cls_idx, cls_name in enumerate(class_names):
        mask = (y == cls_idx)
        cls_matrix = X_matrix[mask]
        other_matrix = X_matrix[~mask]

        cls_freq = np.asarray(cls_matrix.sum(axis=0)).flatten()
        other_freq = np.asarray(other_matrix.sum(axis=0)).flatten()

        # Normalize
        cls_total = cls_freq.sum() if cls_freq.sum() > 0 else 1
        other_total = other_freq.sum() if other_freq.sum() > 0 else 1

        cls_norm = cls_freq / cls_total
        other_norm = other_freq / other_total

        # Discriminative score: difference in normalized frequency
        disc_score = cls_norm - other_norm
        top_idx = disc_score.argsort()[::-1][:top_n]

        result[cls_name] = {
            "words": [features[i] for i in top_idx],
            "scores": [float(disc_score[i]) for i in top_idx],
            "frequencies": [float(cls_freq[i]) for i in top_idx]
        }

    return result


def get_error_analysis(X_test, y_test, y_pred, le, df_clean, top_n=20):
    """Analyze misclassified samples."""
    errors = []
    test_indices = X_test.index.tolist()

    for i, (idx, true, pred) in enumerate(zip(test_indices, y_test, y_pred)):
        if true != pred:
            try:
                query = df_clean.loc[idx, "QueryText"]
                clean = df_clean.loc[idx, "clean_text"]
            except:
                query = str(X_test.iloc[i]) if i < len(X_test) else "N/A"
                clean = query

            actual = le.inverse_transform([true])[0]
            predicted = le.inverse_transform([pred])[0]

            # Simple error reason analysis
            words = clean.lower().split()
            agri_keywords = {"crop", "rice", "paddy", "wheat", "maize", "farm", "field", "soil", "seed", "harvest", "irrigation", "fertilizer"}
            horti_keywords = {"fruit", "vegetable", "flower", "mango", "banana", "tomato", "onion", "garden", "plant", "nursery"}

            agri_score = len(set(words) & agri_keywords)
            horti_score = len(set(words) & horti_keywords)

            if agri_score > 0 and horti_score > 0:
                reason = "Query ambigu — mengandung kata dari kedua kelas"
            elif agri_score == 0 and horti_score == 0:
                reason = "Kurang konteks — tidak ada keyword kelas yang jelas"
            elif len(words) < 3:
                reason = "Query terlalu pendek — informasi terbatas"
            else:
                reason = "Overlap kata — fitur tidak cukup diskriminatif"

            errors.append({
                "Query": query[:120] + "..." if len(str(query)) > 120 else query,
                "Actual": actual,
                "Predicted": predicted,
                "Penyebab": reason,
                "clean_text": clean
            })

            if len(errors) >= top_n:
                break

    return pd.DataFrame(errors) if errors else pd.DataFrame()


def get_error_distribution(y_test, y_pred, le):
    """Get distribution of error types."""
    total = len(y_test)
    correct = int((y_test == y_pred).sum())
    incorrect = total - correct

    # Per-class errors
    class_names = le.classes_
    error_by_class = {}
    for cls_idx, cls_name in enumerate(class_names):
        mask = (y_test == cls_idx)
        cls_total = int(mask.sum())
        cls_correct = int(((y_test == y_pred) & mask).sum())
        cls_error = cls_total - cls_correct
        error_by_class[cls_name] = {
            "total": cls_total,
            "correct": cls_correct,
            "errors": cls_error,
            "error_rate": (cls_error / cls_total * 100) if cls_total > 0 else 0
        }

    return {
        "total": total,
        "correct": correct,
        "incorrect": incorrect,
        "accuracy": correct / total * 100,
        "error_rate": incorrect / total * 100,
        "by_class": error_by_class
    }
