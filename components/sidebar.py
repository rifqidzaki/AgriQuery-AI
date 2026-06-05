# ════════════════════════════════════════════════════════════════
# SIDEBAR — Navigation Component
# ════════════════════════════════════════════════════════════════

import streamlit as st


NAV_ITEMS = [
    "✨ Overview",
    "🗄️ Dataset Analysis",
    "📝 NLP Classical",
    "🧠 NLP Modern",
    "📈 Model Training",
    "⚖️ Model Comparison",
    "🔍 Error Analysis",
    "💡 Explainability",
    "💬 Interactive Prediction",
    "📚 About Research",
]


def render_sidebar():
    """Render the premium sidebar navigation."""
    with st.sidebar:
        # Logo / Brand
        st.markdown("""
        <div style='text-align:center; padding:20px 0 8px;'>
            <div style='width:60px; height:60px; background:rgba(255,255,255,0.08); border-radius:18px;
                        display:inline-flex; align-items:center; justify-content:center; margin-bottom:10px;
                        backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,0.15);
                        box-shadow: 0 8px 32px rgba(0,0,0,0.1);'>
                <span style='font-size:1.8rem;'>🍃</span>
            </div>
            <div style='font-family:Sora; font-size:1.15rem; font-weight:700; letter-spacing:-0.02em;'>AgriMind AI</div>
            <div style='font-size:0.68rem; color:rgba(255,255,255,0.45); margin-top:4px; letter-spacing:1.5px; text-transform:uppercase;'>NLP Analytics Platform</div>
        </div>
        <hr>
        """, unsafe_allow_html=True)

        # Navigation
        menu = st.radio("Nav", NAV_ITEMS, label_visibility="collapsed")

        st.markdown("<hr>", unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div style='text-align:center; padding:12px 0;'>
            <div style='font-size:0.65rem; color:rgba(255,255,255,0.3); line-height:1.5;'>
                Perbandingan NLP Klasik vs Modern<br>
                Decision Tree & Naive Bayes<br>
                <span style='color:rgba(255,255,255,0.15);'>v5.0 • Research Edition</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    return menu
