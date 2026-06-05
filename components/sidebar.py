# ════════════════════════════════════════════════════════════════
# SIDEBAR — Navigation Component v6.0
# ════════════════════════════════════════════════════════════════

import streamlit as st

NAV_ITEMS = [
    "🏠 Overview",
    "📂 Dataset Overview",
    "🧹 Preprocessing",
    "⚙️ Feature Extraction",
    "🧠 Training & Evaluation",
    "📊 Model Comparison",
    "🔍 Error Analysis",
    "🎯 Interactive Prediction",
    "ℹ️ About Project",
]


def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.markdown("""
<div style='text-align:center; padding:16px 0 6px;'>
<div style='font-size:1.8rem; margin-bottom:6px;'>🌾</div>
<div style='font-family:Sora; font-size:1.1rem; font-weight:700;'>Dashboard NLP</div>
<div style='font-size:0.65rem; color:rgba(255,255,255,0.5); margin-top:2px; letter-spacing:1px; text-transform:uppercase;'>Pertanian • v6.0 Final</div>
</div>
<hr>
""", unsafe_allow_html=True)

        menu = st.radio("Nav", NAV_ITEMS, label_visibility="collapsed")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("""
<div style='text-align:center; padding:8px 0;'>
<div style='font-size:0.62rem; color:rgba(255,255,255,0.3); line-height:1.5;'>
Analisis Perbandingan NLP<br>
Klasik vs Modern<br>
Decision Tree & Naive Bayes<br>
+ DistilBERT Fine-Tuning
</div>
</div>
""", unsafe_allow_html=True)

    return menu
