# ════════════════════════════════════════════════════════════════
# MODEL TRAINING — Decision Tree + Naive Bayes × All Features
# ════════════════════════════════════════════════════════════════

import time
import numpy as np
import streamlit as st
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

from backend.classical_nlp import extract_bow, extract_tfidf, extract_ngram
from backend.modern_nlp import extract_word2vec, extract_glove, extract_bert

# Decision Tree parameters
DT_PARAMS = dict(
    criterion="gini",
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

# Model combination names
SCENARIO_NAMES = [
    # Classical
    "DT + BoW", "DT + TF-IDF", "DT + N-Gram",
    "NB + BoW", "NB + TF-IDF", "NB + N-Gram",
    # Modern
    "DT + Word2Vec", "DT + GloVe", "DT + BERT",
    "NB + Word2Vec", "NB + GloVe", "NB + BERT",
]

CLASSICAL_SCENARIOS = ["DT + BoW", "DT + TF-IDF", "DT + N-Gram", "NB + BoW", "NB + TF-IDF", "NB + N-Gram"]
MODERN_SCENARIOS = ["DT + Word2Vec", "DT + GloVe", "DT + BERT", "NB + Word2Vec", "NB + GloVe", "NB + BERT"]

# Color map for scenarios
COLORS = {
    "DT + BoW": "#0E4B2E", "DT + TF-IDF": "#1F7A4D", "DT + N-Gram": "#2E8B57",
    "NB + BoW": "#3D9B6B", "NB + TF-IDF": "#5FAE6E", "NB + N-Gram": "#7BC17F",
    "DT + Word2Vec": "#0A6847", "DT + GloVe": "#137547", "DT + BERT": "#1A8F5C",
    "NB + Word2Vec": "#48A870", "NB + GloVe": "#68B984", "NB + BERT": "#88CA98",
}

FEATURE_NAMES_MAP = {
    "BoW": "Bag of Words",
    "TF-IDF": "TF-IDF",
    "N-Gram": "N-Gram (2,3)",
    "Word2Vec": "Word2Vec (300d)",
    "GloVe": "GloVe (100d)",
    "BERT": "BERT (384d)",
}


def _evaluate_model(model, X_test, y_test):
    """Evaluate a trained model and return metrics dict."""
    y_pred = model.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="macro", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="macro", zero_division=0),
        "f1_score": f1_score(y_test, y_pred, average="macro", zero_division=0),
        "cm": confusion_matrix(y_test, y_pred),
        "y_pred": y_pred,
        "report": classification_report(y_test, y_pred, output_dict=True, zero_division=0),
    }


def _train_dt(X_train, y_train, X_test, y_test):
    """Train Decision Tree and evaluate."""
    t0 = time.time()
    model = DecisionTreeClassifier(**DT_PARAMS)
    model.fit(X_train, y_train)
    elapsed = time.time() - t0

    metrics = _evaluate_model(model, X_test, y_test)
    metrics["train_time"] = elapsed
    metrics["model"] = model
    metrics["depth"] = model.get_depth()
    metrics["leaves"] = model.get_n_leaves()
    metrics["model_type"] = "Decision Tree"
    return metrics


def _train_nb(X_train, y_train, X_test, y_test, is_sparse=True):
    """Train Naive Bayes and evaluate.
    MultinomialNB for sparse/non-negative data, GaussianNB for dense/signed data.
    """
    t0 = time.time()

    if is_sparse:
        model = MultinomialNB(alpha=1.0)
        model.fit(X_train, y_train)
    else:
        # For modern embeddings (can have negative values)
        model = GaussianNB()
        model.fit(X_train, y_train)

    elapsed = time.time() - t0

    metrics = _evaluate_model(model, X_test, y_test)
    metrics["train_time"] = elapsed
    metrics["model"] = model
    metrics["model_type"] = "Naive Bayes"
    metrics["depth"] = "-"
    metrics["leaves"] = "-"
    return metrics


def train_all_models(df, le, progress_callback=None):
    """Train all 12 model combinations and return comprehensive results."""
    import joblib
    import os

    X = df["clean_text"]
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    results = {}
    vectorizers = {}
    all_models = {}
    predictions = {}
    
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

    # ── CLASSICAL FEATURES ──
    classical_configs = {
        "BoW": {
            "extract": extract_bow,
            "vec_file": "vectorizer_bow.pkl",
            "dt_file": "model_dt__bow.pkl",
            "nb_file": "model_nb__bow.pkl",
            "msg": "Bag of Words"
        },
        "TF-IDF": {
            "extract": extract_tfidf,
            "vec_file": "vectorizer_tfidf.pkl",
            "dt_file": "model_dt__tf-idf.pkl",
            "nb_file": "model_nb__tf-idf.pkl",
            "msg": "TF-IDF"
        },
        "N-Gram": {
            "extract": extract_ngram,
            "vec_file": "vectorizer_ngram.pkl",
            "dt_file": "model_dt__n-gram.pkl",
            "nb_file": "model_nb__n-gram.pkl",
            "msg": "N-Gram"
        }
    }

    classical_data = {}

    step = 1
    for feat_name, cfg in classical_configs.items():
        vec_path = os.path.join(models_dir, cfg["vec_file"])
        
        # Vectorizer
        if os.path.exists(vec_path):
            if progress_callback:
                progress_callback(step, 12, f"Loading pre-trained {cfg['msg']} Vectorizer...")
            try:
                vec = joblib.load(vec_path)
                Xtr = vec.transform(X_train)
                Xte = vec.transform(X_test)
            except Exception as e:
                st.warning(f"Failed to load vectorizer {cfg['vec_file']}: {e}. Extracting from scratch.")
                vec, Xtr, Xte = cfg["extract"](X_train, X_test)
        else:
            if progress_callback:
                progress_callback(step, 12, f"Extracting {cfg['msg']}...")
            vec, Xtr, Xte = cfg["extract"](X_train, X_test)
            
        vectorizers[feat_name] = vec
        classical_data[feat_name] = (Xtr, Xte)
        step += 1

    # Train/Load DT + Classical
    for feat_name, cfg in classical_configs.items():
        sc_name = f"DT + {feat_name}"
        dt_path = os.path.join(models_dir, cfg["dt_file"])
        Xtr, Xte = classical_data[feat_name]
        
        if os.path.exists(dt_path):
            if progress_callback:
                progress_callback(step, 12, f"Loading pre-trained {sc_name}...")
            try:
                dt_model = joblib.load(dt_path)
                r = _evaluate_model(dt_model, Xte, y_test)
                r["train_time"] = 0.0
                r["model"] = dt_model
                r["model_type"] = "Decision Tree"
                try:
                    r["depth"] = dt_model.get_depth()
                    r["leaves"] = dt_model.get_n_leaves()
                except:
                    r["depth"] = "-"
                    r["leaves"] = "-"
            except Exception as e:
                st.warning(f"Failed to load model {cfg['dt_file']}: {e}. Training from scratch.")
                r = _train_dt(Xtr, y_train, Xte, y_test)
        else:
            if progress_callback:
                progress_callback(step, 12, f"Training {sc_name}...")
            r = _train_dt(Xtr, y_train, Xte, y_test)
            
        results[sc_name] = r
        all_models[sc_name] = r["model"]
        predictions[sc_name] = r["y_pred"]
        step += 1

    # Train/Load NB + Classical
    for feat_name, cfg in classical_configs.items():
        sc_name = f"NB + {feat_name}"
        nb_path = os.path.join(models_dir, cfg["nb_file"])
        Xtr, Xte = classical_data[feat_name]
        
        if os.path.exists(nb_path):
            if progress_callback:
                progress_callback(step, 12, f"Loading pre-trained {sc_name}...")
            try:
                nb_model = joblib.load(nb_path)
                r = _evaluate_model(nb_model, Xte, y_test)
                r["train_time"] = 0.0
                r["model"] = nb_model
                r["model_type"] = "Naive Bayes"
                r["depth"] = "-"
                r["leaves"] = "-"
            except Exception as e:
                st.warning(f"Failed to load model {cfg['nb_file']}: {e}. Training from scratch.")
                r = _train_nb(Xtr, y_train, Xte, y_test, is_sparse=True)
        else:
            if progress_callback:
                progress_callback(step, 12, f"Training {sc_name}...")
            r = _train_nb(Xtr, y_train, Xte, y_test, is_sparse=True)
            
        results[sc_name] = r
        all_models[sc_name] = r["model"]
        predictions[sc_name] = r["y_pred"]
        step += 1

    # ── MODERN FEATURES ──
    if progress_callback:
        progress_callback(step, 12, "Loading Word2Vec embeddings...")
    try:
        w2v_model, Xtr_w2v, Xte_w2v, w2v_dim = extract_word2vec(X_train, X_test)
        vectorizers["Word2Vec"] = w2v_model
        modern_data_w2v = ("Word2Vec", Xtr_w2v, Xte_w2v)
    except Exception as e:
        st.warning(f"Word2Vec loading failed: {e}. Skipping Word2Vec scenarios.")
        modern_data_w2v = None

    if progress_callback:
        progress_callback(step + 1, 12, "Loading GloVe embeddings...")
    try:
        glove_model, Xtr_glove, Xte_glove, glove_dim = extract_glove(X_train, X_test)
        vectorizers["GloVe"] = glove_model
        modern_data_glove = ("GloVe", Xtr_glove, Xte_glove)
    except Exception as e:
        st.warning(f"GloVe loading failed: {e}. Skipping GloVe scenarios.")
        modern_data_glove = None

    if progress_callback:
        progress_callback(step + 2, 12, "Loading BERT embeddings...")
    try:
        bert_model, Xtr_bert, Xte_bert, bert_dim = extract_bert(X_train, X_test)
        vectorizers["BERT"] = bert_model
        modern_data_bert = ("BERT", Xtr_bert, Xte_bert)
    except Exception as e:
        st.warning(f"BERT loading failed: {e}. Skipping BERT scenarios.")
        modern_data_bert = None

    modern_items = [modern_data_w2v, modern_data_glove, modern_data_bert]

    # Train DT + Modern & NB + Modern
    for item in modern_items:
        if item is None:
            continue
        feat_name, Xtr, Xte = item

        sc_dt = f"DT + {feat_name}"
        if progress_callback:
            progress_callback(step, 12, f"Training {sc_dt}...")
        r_dt = _train_dt(Xtr, y_train, Xte, y_test)
        results[sc_dt] = r_dt
        all_models[sc_dt] = r_dt["model"]
        predictions[sc_dt] = r_dt["y_pred"]

        sc_nb = f"NB + {feat_name}"
        if progress_callback:
            progress_callback(step, 12, f"Training {sc_nb}...")
        r_nb = _train_nb(Xtr, y_train, Xte, y_test, is_sparse=False)
        results[sc_nb] = r_nb
        all_models[sc_nb] = r_nb["model"]
        predictions[sc_nb] = r_nb["y_pred"]
        step += 1

    # Find best model
    best_name = max(results, key=lambda x: results[x]["accuracy"])

    # Store modern feature arrays for embedding visualization
    embedding_arrays = {}
    if modern_data_w2v:
        embedding_arrays["Word2Vec"] = {"train": modern_data_w2v[1], "test": modern_data_w2v[2]}
    if modern_data_glove:
        embedding_arrays["GloVe"] = {"train": modern_data_glove[1], "test": modern_data_glove[2]}
    if modern_data_bert:
        embedding_arrays["BERT"] = {"train": modern_data_bert[1], "test": modern_data_bert[2]}

    return {
        "results": results,
        "models": all_models,
        "vectorizers": vectorizers,
        "predictions": predictions,
        "best_name": best_name,
        "y_test": y_test,
        "y_train": y_train,
        "X_train": X_train,
        "X_test": X_test,
        "le": le,
        "classical_data": classical_data,
        "embedding_arrays": embedding_arrays,
    }
