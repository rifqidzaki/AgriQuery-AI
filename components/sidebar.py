# ════════════════════════════════════════════════════════════════
# SIDEBAR — Navigation Component v7.0
# ════════════════════════════════════════════════════════════════

import streamlit as st

NAV_SECTIONS = {
    "🔍 Analisis Data": [
        "🏠 Overview",
        "📂 Dataset Overview",
        "🧹 Preprocessing",
    ],
    "⚗️ Augmentasi & Balancing": [
        "🔬 Augmentation Analysis",
        "⚖️ Balancing Analysis",
    ],
    "🧠 Model & Fitur": [
        "⚙️ Feature Extraction",
        "🧠 Training & Evaluation",
        "📊 Model Comparison",
    ],
    "🏆 Hasil Penelitian": [
        "🏆 Top Performing Models",
        "📈 Recall Improvement",
        "🤖 DistilBERT Analysis",
        "🔍 Error Analysis",
        "💡 Final Insights",
    ],
    "🎯 Aplikasi": [
        "🎯 Interactive Prediction",
        "ℹ️ About Project",
    ],
}

ALL_NAV_ITEMS = [item for items in NAV_SECTIONS.values() for item in items]


def render_sidebar():
    """Render the sidebar navigation with v7.0 sections."""
    with st.sidebar:
        st.markdown("""
<div style='text-align:center; padding:16px 0 6px;'>
<div style='font-size:1.8rem; margin-bottom:6px;'>🌾</div>
<div style='font-family:Sora; font-size:1.1rem; font-weight:700;'>Dashboard NLP</div>
<div style='font-size:0.65rem; color:rgba(255,255,255,0.5); margin-top:2px; letter-spacing:1px; text-transform:uppercase;'>Pertanian • v7.0 Final</div>
</div>
<hr>
""", unsafe_allow_html=True)

        # Use a single radio for all nav items
        menu = st.radio("Nav", ALL_NAV_ITEMS, label_visibility="collapsed")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""
<div style='text-align:center; padding:8px 0;'>
<div style='font-size:0.62rem; color:rgba(255,255,255,0.3); line-height:1.5;'>
Project v7 Final<br>
15 Skenario × 2 Dataset<br>
= 30 Eksperimen<br>
NB & DT + DistilBERT
</div>
</div>
""", unsafe_allow_html=True)

    return menu
