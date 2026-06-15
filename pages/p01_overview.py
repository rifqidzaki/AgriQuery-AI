# ════════════════════════════════════════════════════════════════
# PAGE 01 — OVERVIEW (v7.0 Final Research Edition)
# ════════════════════════════════════════════════════════════════

import streamlit as st
from backend.research_data import DATASET_ORIGINAL, DATASET_AUGMENTED, SCENARIO_RESULTS, TOP_MODELS


def render(ss):
    results = ss.get("results", {})
    df_clean = ss.get("df_clean")
    best_name = ss.get("best_name", "")
    le = ss.get("le")

    # Hero
    st.markdown("""
<div style='padding:10px 0 20px;'>
<div class='hero-title'>Dashboard NLP Pertanian</div>
<div class='hero-subtitle'>
Analisis Perbandingan Representasi Fitur NLP Klasik dan Modern
pada Klasifikasi Query Pertanian — Project v7 Final Research Edition
dengan 15 Skenario Model × 2 Dataset (Original & Augmented) = 30 Eksperimen.
</div>
<div>
<span class='badge'>📄 Project v7 Final</span>
<span class='badge'>🌾 Agriculture & Horticulture</span>
<span class='badge'>🤖 15 Skenario Model</span>
<span class='badge'>🔬 30 Eksperimen</span>
</div>
</div>
""", unsafe_allow_html=True)

    # ── KPI Cards Row 1 ──────────────────────────────────────────
    top = TOP_MODELS
    best_acc_val = top["best_accuracy"]["accuracy"] * 100
    best_rec_val = top["best_recall"]["recall"] * 100
    best_f1_val = top["best_f1"]["f1"] * 100
    imbalance_before = DATASET_ORIGINAL["imbalance_ratio"]
    imbalance_after = DATASET_AUGMENTED["imbalance_ratio"]
    imbalance_reduction = ((imbalance_before - imbalance_after) / imbalance_before) * 100

    st.markdown(f"""
<div class='kpi-grid'>
<div class='kpi-card'>
<div class='kpi-icon'>🏆</div>
<div class='kpi-label'>Best Accuracy</div>
<div class='kpi-value'>{best_acc_val:.2f}%</div>
<div class='kpi-sub-green'>🥇 {top["best_accuracy"]["name"]}</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>📡</div>
<div class='kpi-label'>Best Recall</div>
<div class='kpi-value'>{best_rec_val:.2f}%</div>
<div class='kpi-sub-green'>🏅 {top["best_recall"]["name"]}</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>⚡</div>
<div class='kpi-label'>Best F1-Score</div>
<div class='kpi-value'>{best_f1_val:.2f}%</div>
<div class='kpi-sub-green'>🎖️ {top["best_f1"]["name"]}</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>⚖️</div>
<div class='kpi-label'>Imbalance Reduction</div>
<div class='kpi-value'>{imbalance_reduction:.0f}%</div>
<div class='kpi-sub-green'>12.0:1 → 2.40:1</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Dataset Original vs Augmented ───────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📂 Dataset: Original vs Augmented</div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        orig = DATASET_ORIGINAL
        st.markdown(f"""
<div class='card' style='border-left:4px solid #E74C3C;'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:14px; color:#E74C3C;'>📁 Dataset Original</div>
<div style='display:grid; grid-template-columns:1fr 1fr; gap:10px;'>
<div style='background:rgba(0,0,0,0.04); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted);'>Total</div>
<div style='font-weight:700; font-size:1.1rem;'>{orig["total"]:,}</div>
</div>
<div style='background:rgba(0,0,0,0.04); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted);'>Imbalance</div>
<div style='font-weight:700; font-size:1.1rem; color:#E74C3C;'>{orig["imbalance_ratio"]:.1f}:1</div>
</div>
<div style='background:rgba(0,0,0,0.04); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted);'>Agriculture</div>
<div style='font-weight:700;'>{orig["agriculture"]:,}</div>
</div>
<div style='background:rgba(0,0,0,0.04); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted);'>Horticulture</div>
<div style='font-weight:700; color:#E74C3C;'>{orig["horticulture"]:,}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        aug = DATASET_AUGMENTED
        st.markdown(f"""
<div class='card' style='border-left:4px solid var(--primary);'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:14px; color:var(--primary);'>✅ Dataset Augmented</div>
<div style='display:grid; grid-template-columns:1fr 1fr; gap:10px;'>
<div style='background:rgba(27,94,32,0.06); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted);'>Total</div>
<div style='font-weight:700; font-size:1.1rem;'>{aug["total"]:,}</div>
</div>
<div style='background:rgba(27,94,32,0.06); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted);'>Imbalance</div>
<div style='font-weight:700; font-size:1.1rem; color:var(--primary);'>{aug["imbalance_ratio"]:.2f}:1 ↓</div>
</div>
<div style='background:rgba(27,94,32,0.06); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted);'>Agriculture</div>
<div style='font-weight:700;'>{aug["agriculture"]:,}</div>
</div>
<div style='background:rgba(27,94,32,0.06); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted);'>Horticulture</div>
<div style='font-weight:700; color:var(--primary);'>{aug["horticulture"]:,} ↑</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Research Summary ─────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📋 Ringkasan Penelitian</div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:10px;'>🎯 Tujuan Penelitian</div>
<div style='font-size:0.88rem; color:var(--text-secondary); line-height:1.7;'>
Membandingkan efektivitas representasi fitur NLP klasik (BoW, TF-IDF, N-Gram),
non-kontekstual (Word2Vec, FastText, GloVe), kontekstual (BERT), dan fine-tuning
transformer (DistilBERT) untuk klasifikasi query pertanian ke dalam dua kategori:
<b>Agriculture</b> dan <b>Horticulture</b>, serta menganalisis dampak augmentasi data
terhadap peningkatan performa pada kelas minoritas.
</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:10px;'>🔬 Metodologi</div>
<div style='font-size:0.88rem; color:var(--text-secondary); line-height:1.7;'>
Dataset <b>Kisan Query</b> (9.939 data) diaugmentasi menggunakan Synonym Replacement,
Contextual BERT, dan Back Translation (EN-ID-EN, EN-JA-EN) menjadi 13.003 data.
Class balancing menggunakan RandomOverSampler dan SMOTE. Evaluasi menggunakan
<b>15 skenario model</b> pada dataset original dan augmented
= <b>30 total eksperimen</b>.
</div>
</div>
""", unsafe_allow_html=True)

    # ── Model Groups ─────────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🗂️ Kelompok Model (15 Skenario)</div>
</div>
""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; margin-bottom:8px;'>📝 Classical NLP</div>
<div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.8;'>
1. DT + BoW<br>2. NB + BoW<br>3. DT + TF-IDF<br>4. NB + TF-IDF<br>5. DT + N-Gram<br>6. NB + N-Gram
</div>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; margin-bottom:8px;'>🧠 Non-Contextual Embedding</div>
<div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.8;'>
7. DT + Word2Vec<br>8. NB + Word2Vec<br>9. DT + FastText<br>10. NB + FastText<br>11. DT + GloVe<br>12. NB + GloVe
</div>
</div>
""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; margin-bottom:8px;'>🔮 Contextual Embedding</div>
<div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.8;'>
13. DT + BERT<br>14. NB + BERT
</div>
</div>
""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; margin-bottom:8px;'>🚀 Transformer</div>
<div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.8;'>
15. DistilBERT<br>Fine-Tuning
</div>
</div>
""", unsafe_allow_html=True)
