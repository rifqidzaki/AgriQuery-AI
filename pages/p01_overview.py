# ════════════════════════════════════════════════════════════════
# PAGE 01 — OVERVIEW
# ════════════════════════════════════════════════════════════════

import streamlit as st


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
pada Klasifikasi Query Pertanian menggunakan Decision Tree, Naive Bayes,
dan DistilBERT Fine-Tuning.
</div>
<div>
<span class='badge'>📄 Penelitian Final</span>
<span class='badge'>🌾 Agriculture & Horticulture</span>
<span class='badge'>🤖 13 Model Kombinasi</span>
</div>
</div>
""", unsafe_allow_html=True)

    # KPI Cards
    total_data = len(df_clean) if df_clean is not None else 0
    n_classes = len(le.classes_) if le is not None else 2
    n_models = len(results)
    best_acc = results[best_name]["accuracy"] * 100 if best_name in results else 0

    st.markdown(f"""
<div class='kpi-grid'>
<div class='kpi-card'>
<div class='kpi-icon'>📊</div>
<div class='kpi-label'>Total Data</div>
<div class='kpi-value'>{total_data:,}</div>
<div class='kpi-sub'>Baris data bersih</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>🏷️</div>
<div class='kpi-label'>Jumlah Kelas</div>
<div class='kpi-value'>{n_classes}</div>
<div class='kpi-sub'>Agriculture & Horticulture</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>🧠</div>
<div class='kpi-label'>Jumlah Model</div>
<div class='kpi-value'>{n_models}</div>
<div class='kpi-sub'>Kombinasi model dievaluasi</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>🏆</div>
<div class='kpi-label'>Akurasi Terbaik</div>
<div class='kpi-value'>{best_acc:.1f}%</div>
<div class='kpi-sub-green'>🥇 {best_name}</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Research Summary
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
Membandingkan efektivitas representasi fitur NLP klasik (Bag of Words, TF-IDF, N-Gram)
dengan representasi modern berbasis embedding (Word2Vec, GloVe, BERT) dan fine-tuning
transformer (DistilBERT) untuk klasifikasi query pertanian ke dalam dua kategori:
<b>Agriculture</b> dan <b>Horticulture</b>.
</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:10px;'>🔬 Metodologi</div>
<div style='font-size:0.88rem; color:var(--text-secondary); line-height:1.7;'>
Dataset <b>Kisan Query</b> diproses melalui pipeline NLP standar (case folding, stopword removal,
tokenization). Fitur diekstrak menggunakan 6 metode, lalu dilatih dengan 3 algoritma
(Decision Tree, Naive Bayes, DistilBERT), menghasilkan <b>13 kombinasi model</b>
yang dievaluasi secara komprehensif.
</div>
</div>
""", unsafe_allow_html=True)

    # Model groups overview
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🗂️ Kelompok Model</div>
<div class='section-subtitle'>13 kombinasi model yang dievaluasi dalam penelitian ini</div>
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
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; margin-bottom:8px;'>🧠 Semantic Embedding</div>
<div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.8;'>
7. DT + Word2Vec<br>8. NB + Word2Vec<br>9. DT + GloVe<br>10. NB + GloVe
</div>
</div>
""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; margin-bottom:8px;'>🔮 Contextual Embedding</div>
<div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.8;'>
11. DT + BERT<br>12. NB + BERT
</div>
</div>
""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; margin-bottom:8px;'>🚀 Transformer</div>
<div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.8;'>
13. DistilBERT<br>Fine-Tuning
</div>
</div>
""", unsafe_allow_html=True)
