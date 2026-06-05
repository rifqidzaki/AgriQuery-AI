# ════════════════════════════════════════════════════════════════
# MODEL LOADER — Load all 13 pre-trained models from pkl files
# No training from scratch — pure pkl loading for speed
# ════════════════════════════════════════════════════════════════

import os
import time
import joblib
import numpy as np
import streamlit as st
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# ── All 13 model scenarios ──
SCENARIOS = [
    # Classical NLP
    {"name": "DT + BoW",      "algo": "dt", "feature": "BoW",      "group": "Classical NLP",          "model_file": "model_dt_bow.pkl",      "vec_file": "vectorizer_bow.pkl"},
    {"name": "NB + BoW",      "algo": "nb", "feature": "BoW",      "group": "Classical NLP",          "model_file": "model_nb_bow.pkl",      "vec_file": "vectorizer_bow.pkl"},
    {"name": "DT + TF-IDF",   "algo": "dt", "feature": "TF-IDF",   "group": "Classical NLP",          "model_file": "model_dt_tf-idf.pkl",   "vec_file": "vectorizer_tfidf.pkl"},
    {"name": "NB + TF-IDF",   "algo": "nb", "feature": "TF-IDF",   "group": "Classical NLP",          "model_file": "model_nb_tf-idf.pkl",   "vec_file": "vectorizer_tfidf.pkl"},
    {"name": "DT + N-Gram",   "algo": "dt", "feature": "N-Gram",   "group": "Classical NLP",          "model_file": "model_dt_n-gram.pkl",   "vec_file": "vectorizer_ngram.pkl"},
    {"name": "NB + N-Gram",   "algo": "nb", "feature": "N-Gram",   "group": "Classical NLP",          "model_file": "model_nb_n-gram.pkl",   "vec_file": "vectorizer_ngram.pkl"},
    # Semantic Embedding
    {"name": "DT + Word2Vec", "algo": "dt", "feature": "Word2Vec", "group": "Semantic Embedding",     "model_file": "model_dt_word2vec.pkl", "vec_file": None},
    {"name": "NB + Word2Vec", "algo": "nb", "feature": "Word2Vec", "group": "Semantic Embedding",     "model_file": "model_nb_word2vec.pkl", "vec_file": None},
    {"name": "DT + GloVe",    "algo": "dt", "feature": "GloVe",    "group": "Semantic Embedding",     "model_file": "model_dt_glove.pkl",    "vec_file": None},
    {"name": "NB + GloVe",    "algo": "nb", "feature": "GloVe",    "group": "Semantic Embedding",     "model_file": "model_nb_glove.pkl",    "vec_file": None},
    # Contextual Embedding
    {"name": "DT + BERT",     "algo": "dt", "feature": "BERT",     "group": "Contextual Embedding",   "model_file": "model_dt_bert.pkl",     "vec_file": None},
    {"name": "NB + BERT",     "algo": "nb", "feature": "BERT",     "group": "Contextual Embedding",   "model_file": "model_nb_bert.pkl",     "vec_file": None},
    # Transformer Fine-Tuning
    {"name": "DistilBERT Fine-Tuning", "algo": "transformer", "feature": "DistilBERT", "group": "Transformer Fine-Tuning", "model_file": None, "vec_file": None},
]

SCENARIO_NAMES = [s["name"] for s in SCENARIOS]
SKLEARN_SCENARIOS = [s for s in SCENARIOS if s["algo"] != "transformer"]

# ── Alternative file naming patterns (backward compatibility) ──
ALT_NAMES = {
    "model_dt_bow.pkl": "model_dt__bow.pkl",
    "model_nb_bow.pkl": "model_nb__bow.pkl",
    "model_dt_tf-idf.pkl": "model_dt__tf-idf.pkl",
    "model_nb_tf-idf.pkl": "model_nb__tf-idf.pkl",
    "model_dt_n-gram.pkl": "model_dt__n-gram.pkl",
    "model_nb_n-gram.pkl": "model_nb__n-gram.pkl",
}


def _resolve_model_path(filename):
    """Find model file, trying primary name then alternative."""
    if filename is None:
        return None
    path = os.path.join(MODELS_DIR, filename)
    if os.path.exists(path):
        return path
    alt = ALT_NAMES.get(filename)
    if alt:
        alt_path = os.path.join(MODELS_DIR, alt)
        if os.path.exists(alt_path):
            return alt_path
    return None


@st.cache_resource(show_spinner=False)
def load_sklearn_model(filename):
    """Load a single sklearn model from pkl."""
    path = _resolve_model_path(filename)
    if path is None:
        return None
    try:
        return joblib.load(path)
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_vectorizer(filename):
    """Load a vectorizer from pkl."""
    if filename is None:
        return None
    path = os.path.join(MODELS_DIR, filename)
    if not os.path.exists(path):
        return None
    try:
        return joblib.load(path)
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_label_encoder():
    """Load the label encoder."""
    path = os.path.join(MODELS_DIR, "label_encoder.pkl")
    if os.path.exists(path):
        try:
            return joblib.load(path)
        except Exception:
            pass
    return None


def _evaluate(model, X_test, y_test):
    """Evaluate model and return metrics dict."""
    t0 = time.time()
    y_pred = model.predict(X_test)
    
    # Get probabilities if available
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)
    else:
        # Fallback for models without predict_proba
        y_prob = np.zeros((len(y_test), len(np.unique(y_test))))
        for i, p in enumerate(y_pred):
            y_prob[i, int(p)] = 1.0

    inference_time = time.time() - t0
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
    }


def _transform_classical(X_texts, vec_file):
    """Transform texts using a classical vectorizer."""
    vec = load_vectorizer(vec_file)
    if vec is None:
        return None, None
    try:
        return vec.transform(X_texts), vec
    except Exception:
        return None, None


@st.cache_resource(show_spinner=False)
def _load_w2v_model():
    from gensim.models import Word2Vec, KeyedVectors
    paths = [
        os.path.join(MODELS_DIR, "word2vec_model.bin"),
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                w2v = Word2Vec.load(p)
                return w2v.wv if hasattr(w2v, "wv") else w2v
            except Exception:
                try:
                    return KeyedVectors.load_word2vec_format(p, binary=True)
                except Exception:
                    pass
    return None


@st.cache_resource(show_spinner=False)
def _load_glove_model():
    from gensim.models import KeyedVectors
    paths = [
        os.path.join(MODELS_DIR, "glove.6B.50d.txt"),
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return KeyedVectors.load_word2vec_format(p, binary=False, no_header=True)
            except Exception:
                pass
    return None


@st.cache_resource(show_spinner=False)
def _load_bert_encoder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')


def _avg_word_vectors(texts, model, dim):
    """Average word vectors for a list of texts."""
    result = []
    for text in texts:
        words = str(text).lower().split()
        vecs = [model[w] for w in words if w in model]
        result.append(np.mean(vecs, axis=0) if vecs else np.zeros(dim))
    return np.array(result)


@st.cache_data(show_spinner=False)
def _transform_word2vec(texts_list):
    model = _load_w2v_model()
    if model is None:
        return None
    dim = getattr(model, "vector_size", 300)
    return _avg_word_vectors(texts_list, model, dim)


@st.cache_data(show_spinner=False)
def _transform_glove(texts_list):
    model = _load_glove_model()
    if model is None:
        return None
    dim = getattr(model, "vector_size", 50)
    return _avg_word_vectors(texts_list, model, dim)


@st.cache_data(show_spinner=False)
def _transform_bert(texts_list):
    model = _load_bert_encoder()
    return model.encode(texts_list, show_progress_bar=False, batch_size=64)


def transform_modern(X_texts, feature_type):
    """Transform texts using modern embedding models."""
    texts_list = X_texts.tolist() if hasattr(X_texts, 'tolist') else list(X_texts)
    if feature_type == "Word2Vec":
        return _transform_word2vec(tuple(texts_list))
    elif feature_type == "GloVe":
        return _transform_glove(tuple(texts_list))
    elif feature_type == "BERT":
        return _transform_bert(tuple(texts_list))
    return None


def load_and_evaluate_all(X_test_text, y_test, progress_callback=None):
    """Load all 12 sklearn models and evaluate them on test data.
    Returns dict of {scenario_name: metrics_dict}.
    """
    results = {}
    vectorizers = {}
    models = {}
    total = len(SKLEARN_SCENARIOS)

    for i, sc in enumerate(SKLEARN_SCENARIOS):
        name = sc["name"]
        if progress_callback:
            progress_callback(i + 1, total + 1, f"Loading {name}...")

        # Load model
        model = load_sklearn_model(sc["model_file"])
        if model is None:
            continue

        # Transform test data
        if sc["vec_file"]:
            # Classical: use vectorizer
            X_test_transformed, vec = _transform_classical(X_test_text, sc["vec_file"])
            if X_test_transformed is None:
                continue
            vectorizers[sc["feature"]] = vec
        else:
            # Modern: use embedding
            X_test_transformed = transform_modern(X_test_text, sc["feature"])
            if X_test_transformed is None:
                continue

        # Evaluate
        try:
            metrics = _evaluate(model, X_test_transformed, y_test)
            metrics["model"] = model
            metrics["model_type"] = "Decision Tree" if sc["algo"] == "dt" else "Naive Bayes"
            metrics["feature_type"] = sc["feature"]
            metrics["group"] = sc["group"]
            results[name] = metrics
            models[name] = model
        except Exception as e:
            st.warning(f"⚠️ Gagal evaluasi {name}: {e}")

    if progress_callback:
        progress_callback(total + 1, total + 1, "Selesai!")

    best_name = max(results, key=lambda x: results[x]["accuracy"]) if results else ""

    return {
        "results": results,
        "models": models,
        "vectorizers": vectorizers,
        "best_name": best_name,
        "y_test": y_test,
    }
