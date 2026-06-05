# ════════════════════════════════════════════════════════════════
# PAGE 01 — OVERVIEW / HERO
# ════════════════════════════════════════════════════════════════

import streamlit as st
from components.metrics import render_metric_grid, render_section_header
from components.charts import plotly_bar, plotly_cm, EMERALD_PALETTE


def render(ss):
    """Render the Overview page."""
    results = ss.get("results", {})
    best_name = ss.get("best_name", "")
    df_clean = ss.get("df_clean")
    le = ss.get("le")

    # ── Hero Section ──
    st.markdown("""
<div style='padding:40px 0 24px 0;'>
<div class='ai-badge'>v5.0 Research Edition</div>
<div class='ai-badge'>Decision Tree + Naive Bayes</div>
<div class='ai-badge-gold'>🏆 Classical vs Modern NLP</div>
<div class='hero-title'>Agricultural Query<br>Intelligence Platform.</div>
<div class='hero-subtitle'>
Platform NLP analytics yang membandingkan representasi fitur klasik (BoW, TF-IDF, N-Gram) dengan embedding modern (Word2Vec, GloVe, BERT) untuk klasifikasi query pertanian menggunakan Decision Tree dan Naive Bayes.
</div>
</div>
""", unsafe_allow_html=True)

    if not results:
        st.info("⏳ Memuat data dan melatih model... Silakan tunggu.")
        return

    # ── Key Metrics ──
    best_r = results[best_name]
    acc = best_r['accuracy'] * 100
    n_data = f"{len(df_clean):,}" if df_clean is not None else "—"

    # Count available scenarios
    n_models = 2  # DT + NB
    n_classical = 3  # BoW, TF-IDF, N-Gram
    n_modern = sum(1 for k in ["Word2Vec", "GloVe", "BERT"] if any(k in s for s in results.keys()))
    total_combos = len(results)

    render_metric_grid([
        {"icon": "🎯", "label": "Best Accuracy", "value": f"{acc:.2f}", "unit": "%", "sub_green": best_name},
        {"icon": "🗄️", "label": "Dataset Size", "value": n_data, "sub": "Processed queries"},
        {"icon": "🤖", "label": "ML Models", "value": str(n_models), "sub": "Decision Tree + Naive Bayes"},
        {"icon": "📝", "label": "Classical Features", "value": str(n_classical), "sub": "BoW, TF-IDF, N-Gram"},
        {"icon": "🧠", "label": "Modern Embeddings", "value": str(n_modern), "sub": "Word2Vec, GloVe, BERT"},
        {"icon": "⚡", "label": "Total Combinations", "value": str(total_combos), "sub": "Model × Feature"},
    ])

    # ── Research Summary ──
    st.markdown("""
<div class='glass-card'>
<div style='display:flex; align-items:center; gap:12px; margin-bottom:16px;'>
<div style='width:42px; height:42px; background:linear-gradient(135deg, rgba(31,122,77,0.1), rgba(95,174,110,0.1)); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:1.2rem;'>📋</div>
<div style='font-family:Sora; font-weight:700; font-size:1.1rem; color:var(--text-main);'>Research Summary</div>
</div>
<div style='font-size:0.9rem; color:var(--text-secondary); line-height:1.8;'>
<strong>Judul:</strong> Analisis Perbandingan Representasi Fitur NLP Klasik dan Modern pada Klasifikasi Query Pertanian Menggunakan Decision Tree dan Naive Bayes<br><br>
<strong>Dataset:</strong> Kisan Query Analysis Dataset — berisi pertanyaan petani dari Kisan Call Centre (KCC) India<br><br>
<strong>Task:</strong> Binary Text Classification — membedakan query sektor <strong>Agriculture</strong> dan <strong>Horticulture</strong><br><br>
<strong>Tujuan:</strong> Membandingkan efektivitas representasi fitur NLP klasik (BoW, TF-IDF, N-Gram) vs embedding modern (Word2Vec, GloVe, BERT) dalam mengklasifikasikan query pertanian menggunakan dua algoritma machine learning.
</div>
</div>
""", unsafe_allow_html=True)

    # ── Quick Comparison Charts ──
    col1, col2 = st.columns(2)

    with col1:
        # Best accuracy per feature type
        feature_types = []
        feature_accs = []
        feature_colors = []
        for feat_name in ["BoW", "TF-IDF", "N-Gram", "Word2Vec", "GloVe", "BERT"]:
            matching = {k: v for k, v in results.items() if feat_name in k}
            if matching:
                best_feat = max(matching, key=lambda x: matching[x]["accuracy"])
                feature_types.append(feat_name)
                feature_accs.append(matching[best_feat]["accuracy"] * 100)
                feature_colors.append(EMERALD_PALETTE[len(feature_types) - 1] if len(feature_types) <= len(EMERALD_PALETTE) else "#5FAE6E")

        fig = plotly_bar(feature_types, feature_accs, "Best Accuracy per Feature Type", feature_colors)
        fig.update_layout(yaxis=dict(range=[0, 110]))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Best model confusion matrix
        if le is not None:
            fig_cm = plotly_cm(best_r["cm"], f"Confusion Matrix — {best_name}", list(le.classes_))
            st.plotly_chart(fig_cm, use_container_width=True)

    # ── Quick Stats Cards ──
    st.markdown("""
<div class='glass-card' style='display:flex; gap:40px; flex-wrap:wrap; justify-content:center;'>
<div style='text-align:center;'>
<div style='font-size:2.5rem;'>🌾</div>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-top:6px;'>Agriculture</div>
<div style='font-size:0.8rem; color:var(--text-muted);'>Crop cultivation, farming</div>
</div>
<div style='text-align:center;'>
<div style='font-size:2.5rem;'>🌿</div>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-top:6px;'>Horticulture</div>
<div style='font-size:0.8rem; color:var(--text-muted);'>Fruits, vegetables, flowers</div>
</div>
<div style='text-align:center;'>
<div style='font-size:2.5rem;'>🧪</div>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-top:6px;'>6 Features</div>
<div style='font-size:0.8rem; color:var(--text-muted);'>3 Classical + 3 Modern</div>
</div>
<div style='text-align:center;'>
<div style='font-size:2.5rem;'>📊</div>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-top:6px;'>12 Models</div>
<div style='font-size:0.8rem; color:var(--text-muted);'>2 ML × 6 features</div>
</div>
</div>
""", unsafe_allow_html=True)
