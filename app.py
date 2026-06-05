# ════════════════════════════════════════════════════════════════
# APP.PY — Main Entry Point
# Dashboard NLP Pertanian v6.0 — Final Research Edition
# ════════════════════════════════════════════════════════════════
# Analisis Perbandingan Representasi Fitur NLP Klasik dan Modern
# pada Klasifikasi Query Pertanian
# Decision Tree, Naive Bayes, + DistilBERT Fine-Tuning
# ════════════════════════════════════════════════════════════════

import streamlit as st
import os
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ──
st.set_page_config(
    page_title="Dashboard NLP Pertanian",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ──
from styles import CUSTOM_CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Imports ──
from components.sidebar import render_sidebar
from backend.data_loader import load_data, prepare_data
from backend.model_loader import load_and_evaluate_all
from backend.transformer_inference import evaluate_transformer, is_transformer_available
from sklearn.model_selection import train_test_split

# ── Pages ──
from pages import (
    p01_overview, p02_dataset, p03_preprocessing,
    p04_feature_extraction, p05_training_eval,
    p06_model_comparison, p07_error_analysis,
    p08_prediction, p09_about
)


# ════════════════════════════════════════════════════════════════
# DATASET PATH
# ════════════════════════════════════════════════════════════════
DATASET_PATHS = [
    "query_agg.csv",
    os.path.join(os.path.dirname(__file__), "query_agg.csv"),
    r"d:\SEMESTER 6\Pemrosesan Bahasa Alami (NLP)\Dasboard NLP\query_agg.csv",
    r"d:\SEMESTER 6\Pemrosesan Bahasa Alami (NLP)\New Dasboard\query_agg.csv",
]


def find_dataset():
    for path in DATASET_PATHS:
        if os.path.exists(path):
            return path
    return None


# ════════════════════════════════════════════════════════════════
# INITIALIZATION
# ════════════════════════════════════════════════════════════════
def initialize_pipeline():
    """Load data and evaluate all pre-trained models."""
    dataset_path = find_dataset()

    if dataset_path is None:
        st.error("❌ Dataset `query_agg.csv` tidak ditemukan!")
        st.markdown("""
<div class='card-static' style='padding:24px;'>
<div style='font-family:Sora; font-weight:700; margin-bottom:8px;'>📂 Cara Menambahkan Dataset</div>
<div style='font-size:0.88rem; line-height:1.7;'>
Letakkan file <code>query_agg.csv</code> di folder yang sama dengan <code>app.py</code>.
</div>
</div>
""", unsafe_allow_html=True)
        return False

    # Progress display
    progress_container = st.empty()
    progress_bar = st.progress(0)
    status_text = st.empty()

    def update_progress(step, total, message):
        progress_bar.progress(min(step / total, 1.0))
        status_text.markdown(f"""
<div style='text-align:center; font-size:0.88rem; color:var(--text-muted);'>
<span class='typing-indicator'>⚡</span> {message} ({step}/{total})
</div>
""", unsafe_allow_html=True)

    progress_container.markdown("""
<div style='text-align:center; padding:50px 0 16px;'>
<div style='font-size:2.5rem; margin-bottom:12px;'>🌾</div>
<div style='font-family:Sora; font-size:1.3rem; font-weight:700; color:var(--text-main); margin-bottom:6px;'>
Memuat Dashboard NLP Pertanian
</div>
<div style='font-size:0.88rem; color:var(--text-muted);'>
Memuat dataset, mengevaluasi 13 kombinasi model...
</div>
</div>
""", unsafe_allow_html=True)

    # 1. Load data
    update_progress(1, 15, "Memuat dataset...")
    df_raw = load_data(dataset_path)
    if df_raw is None:
        st.error("❌ Gagal memuat dataset.")
        return False

    update_progress(2, 15, "Menyiapkan data...")
    df_clean, le = prepare_data(df_raw)

    # 2. Split data (same seed as training)
    X = df_clean["clean_text"]
    y = df_clean["label"].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # 3. Load & evaluate all sklearn models
    update_progress(3, 15, "Memuat dan mengevaluasi model...")
    eval_results = load_and_evaluate_all(X_test, y_test, progress_callback=update_progress)

    # 4. Evaluate transformer if available
    if is_transformer_available():
        update_progress(14, 15, "Mengevaluasi DistilBERT Fine-Tuning...")
        transformer_metrics = evaluate_transformer(X_test.tolist(), y_test)
        if transformer_metrics is not None:
            eval_results["results"]["DistilBERT Fine-Tuning"] = transformer_metrics
            # Check if transformer is better
            best = eval_results["best_name"]
            if transformer_metrics["accuracy"] > eval_results["results"].get(best, {}).get("accuracy", 0):
                eval_results["best_name"] = "DistilBERT Fine-Tuning"

    # 5. Store in session state
    st.session_state["df_raw"] = df_raw
    st.session_state["df_clean"] = df_clean
    st.session_state["le"] = le
    st.session_state["X_train"] = X_train
    st.session_state["X_test"] = X_test
    st.session_state["y_train"] = y_train
    st.session_state["y_test"] = y_test

    for key, value in eval_results.items():
        st.session_state[key] = value

    st.session_state["ready"] = True

    # Clear loading UI
    progress_container.empty()
    progress_bar.empty()
    status_text.empty()

    return True


# ════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ════════════════════════════════════════════════════════════════
def main():
    menu = render_sidebar()

    if not st.session_state.get("ready", False):
        success = initialize_pipeline()
        if not success:
            return

    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)

    ss = st.session_state

    if menu == "🏠 Overview":
        p01_overview.render(ss)
    elif menu == "📂 Dataset Overview":
        p02_dataset.render(ss)
    elif menu == "🧹 Preprocessing":
        p03_preprocessing.render(ss)
    elif menu == "⚙️ Feature Extraction":
        p04_feature_extraction.render(ss)
    elif menu == "🧠 Training & Evaluation":
        p05_training_eval.render(ss)
    elif menu == "📊 Model Comparison":
        p06_model_comparison.render(ss)
    elif menu == "🔍 Error Analysis":
        p07_error_analysis.render(ss)
    elif menu == "🎯 Interactive Prediction":
        p08_prediction.render(ss)
    elif menu == "ℹ️ About Project":
        p09_about.render(ss)


if __name__ == "__main__":
    main()
