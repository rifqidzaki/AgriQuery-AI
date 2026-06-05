# ════════════════════════════════════════════════════════════════
# APP.PY — Main Entry Point
# AgriMind AI — NLP Analytics Platform v5.0
# ════════════════════════════════════════════════════════════════
# Analisis Perbandingan Representasi Fitur NLP Klasik dan Modern
# pada Klasifikasi Query Pertanian
# Menggunakan Decision Tree dan Naive Bayes
# ════════════════════════════════════════════════════════════════

import streamlit as st
import os
import warnings
warnings.filterwarnings('ignore')

# ── Page Config (must be first Streamlit command) ──
st.set_page_config(
    page_title="AgriMind AI — NLP Analytics Platform",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS Injection ──
from styles import CUSTOM_CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Imports ──
from components.sidebar import render_sidebar
from backend.data_loader import load_data, prepare_data
from backend.model_training import train_all_models

# ── Pages ──
from pages import (
    p01_overview, p02_dataset, p03_nlp_classical, p04_nlp_modern,
    p05_model_training, p06_model_comparison, p07_error_analysis,
    p08_explainability, p09_interactive_prediction, p10_about_research
)


# ════════════════════════════════════════════════════════════════
# DATASET PATH RESOLUTION
# ════════════════════════════════════════════════════════════════
DATASET_PATHS = [
    "query_agg.csv",
    os.path.join(os.path.dirname(__file__), "query_agg.csv"),
    r"d:\SEMESTER 6\Pemrosesan Bahasa Alami (NLP)\Dasboard NLP\query_agg.csv",
    r"d:\SEMESTER 6\Pemrosesan Bahasa Alami (NLP)\New Dasboard\query_agg.csv",
]


def find_dataset():
    """Find the dataset file from known paths."""
    for path in DATASET_PATHS:
        if os.path.exists(path):
            return path
    return None


# ════════════════════════════════════════════════════════════════
# INITIALIZATION
# ════════════════════════════════════════════════════════════════
def initialize_pipeline():
    """Load data, train all models, store in session state."""
    dataset_path = find_dataset()

    if dataset_path is None:
        st.error("❌ Dataset `query_agg.csv` tidak ditemukan!")
        st.markdown("""
        <div class='glass-card' style='padding:24px;'>
            <div style='font-family:Sora; font-weight:700; margin-bottom:10px;'>📂 Cara Menambahkan Dataset</div>
            <div style='font-size:0.9rem; line-height:1.8;'>
                Letakkan file <code>query_agg.csv</code> di salah satu lokasi berikut:<br>
                <code>1. Folder yang sama dengan app.py</code><br>
                <code>2. d:\\SEMESTER 6\\Pemrosesan Bahasa Alami (NLP)\\Dasboard NLP\\</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return False

    # Progress display
    progress_container = st.empty()
    progress_bar = st.progress(0)
    status_text = st.empty()

    def update_progress(step, total, message):
        progress = step / total
        progress_bar.progress(progress)
        status_text.markdown(f"""
        <div style='text-align:center; font-family:Inter; font-size:0.9rem; color:var(--text-muted);'>
            <span class='typing-indicator'>⚡</span> {message} ({step}/{total})
        </div>
        """, unsafe_allow_html=True)

    # Show loading UI
    progress_container.markdown("""
    <div style='text-align:center; padding:60px 0 20px;'>
        <div style='font-size:3rem; margin-bottom:16px;'>🍃</div>
        <div style='font-family:Sora; font-size:1.5rem; font-weight:700; color:var(--text-main); margin-bottom:8px;'>
            Initializing AgriMind AI Engine
        </div>
        <div style='font-size:0.9rem; color:var(--text-muted);'>
            Loading dataset, extracting features, training 12 model combinations...
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    update_progress(1, 15, "Loading dataset...")
    df_raw = load_data(dataset_path)

    if df_raw is None:
        st.error("❌ Gagal memuat dataset.")
        return False

    update_progress(2, 15, "Preparing data...")
    df_clean, le = prepare_data(df_raw)

    # Train all models
    update_progress(3, 15, "Training all model combinations...")
    training_results = train_all_models(df_clean, le, progress_callback=update_progress)

    # Store in session state
    st.session_state["df_raw"] = df_raw
    st.session_state["df_clean"] = df_clean
    st.session_state["le"] = le

    for key, value in training_results.items():
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
    # Render sidebar and get selected page
    menu = render_sidebar()

    # Initialize if not ready
    if not st.session_state.get("ready", False):
        success = initialize_pipeline()
        if not success:
            return

    # Add spacing
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

    # Route to selected page
    ss = st.session_state

    if "Overview" in menu:
        p01_overview.render(ss)
    elif "Dataset" in menu:
        p02_dataset.render(ss)
    elif "Classical" in menu:
        p03_nlp_classical.render(ss)
    elif "Modern" in menu:
        p04_nlp_modern.render(ss)
    elif "Training" in menu:
        p05_model_training.render(ss)
    elif "Comparison" in menu:
        p06_model_comparison.render(ss)
    elif "Error" in menu:
        p07_error_analysis.render(ss)
    elif "Explainability" in menu:
        p08_explainability.render(ss)
    elif "Prediction" in menu:
        p09_interactive_prediction.render(ss)
    elif "About" in menu:
        p10_about_research.render(ss)


if __name__ == "__main__":
    main()
