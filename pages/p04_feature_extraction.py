# ════════════════════════════════════════════════════════════════
# PAGE 04 — FEATURE EXTRACTION
# Merged: Classical NLP + Semantic Embedding + Contextual
# ════════════════════════════════════════════════════════════════

import streamlit as st
from backend.classical_nlp import CLASSICAL_EXPLANATIONS, get_feature_info, get_top_tokens
from backend.model_loader import load_vectorizer
from components.charts import plotly_horizontal_bar


def render(ss):
    st.markdown("""
<div class='section-header'>
<div class='section-title'>⚙️ Feature Extraction</div>
<div class='section-subtitle'>Metode representasi fitur yang digunakan dalam penelitian ini</div>
</div>
""", unsafe_allow_html=True)

    tabs = st.tabs([
        "📝 Classical NLP",
        "🧠 Semantic Embedding",
        "🔮 Contextual Embedding"
    ])

    # ── TAB 1: Classical NLP ──
    with tabs[0]:
        st.markdown("""
<div class='card-static'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:6px;'>📝 Classical NLP Features</div>
<div style='font-size:0.85rem; color:var(--text-secondary); line-height:1.6;'>
Representasi fitur berbasis frekuensi kata yang mengubah teks menjadi vektor numerik menggunakan
penghitungan statistik sederhana. Metode ini cepat dan mudah diimplementasi.
</div>
</div>
""", unsafe_allow_html=True)

        for key, info in CLASSICAL_EXPLANATIONS.items():
            with st.expander(info["title"], expanded=False):
                st.markdown(f"""
<div style='font-size:0.88rem; color:var(--text-secondary); line-height:1.7; margin-bottom:12px;'>{info["desc"]}</div>
<div style='margin-bottom:12px;'>
<span class='kpi-label'>FORMULA</span><br>
<code style='font-size:0.82rem;'>{info["formula"]}</code>
</div>
""", unsafe_allow_html=True)

                col_p, col_c = st.columns(2)
                with col_p:
                    st.markdown("<div style='font-weight:600; font-size:0.82rem; color:var(--secondary); margin-bottom:6px;'>✅ Kelebihan</div>", unsafe_allow_html=True)
                    for p in info["pros"]:
                        st.markdown(f"<div style='font-size:0.82rem; padding:2px 0;'>• {p}</div>", unsafe_allow_html=True)
                with col_c:
                    st.markdown("<div style='font-weight:600; font-size:0.82rem; color:#C0392B; margin-bottom:6px;'>⚠️ Kekurangan</div>", unsafe_allow_html=True)
                    for c in info["cons"]:
                        st.markdown(f"<div style='font-size:0.82rem; padding:2px 0;'>• {c}</div>", unsafe_allow_html=True)

                # Show top tokens if vectorizer available
                vec_map = {"bow": "vectorizer_bow.pkl", "tfidf": "vectorizer_tfidf.pkl", "ngram": "vectorizer_ngram.pkl"}
                vec_file = vec_map.get(key)
                if vec_file:
                    vec = load_vectorizer(vec_file)
                    if vec is not None:
                        feat_info = get_feature_info(vec)
                        st.markdown(f"""
<div style='margin-top:12px;'>
<span class='badge'>Vocabulary: {feat_info['vocab_size']:,} fitur</span>
<span class='badge'>N-Gram Range: {feat_info['ngram_range']}</span>
</div>
""", unsafe_allow_html=True)

    # ── TAB 2: Semantic Embedding ──
    with tabs[1]:
        st.markdown("""
<div class='card-static'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:6px;'>🧠 Semantic Embedding</div>
<div style='font-size:0.85rem; color:var(--text-secondary); line-height:1.6;'>
Representasi dense vector yang menangkap hubungan semantik antar kata.
Setiap kata direpresentasikan sebagai vektor kontinu dalam ruang berdimensi tinggi.
</div>
</div>
""", unsafe_allow_html=True)

        embed_info = [
            {
                "title": "🧠 Word2Vec",
                "desc": "Model neural network yang mempelajari representasi vektor kata dari konteks menggunakan arsitektur Skip-gram atau CBOW.",
                "points": [
                    "Dense vector (300 dimensi)",
                    "Menangkap relasi semantik (king - man + woman ≈ queen)",
                    "Static embedding — satu kata = satu vektor tetap",
                    "Model lokal: word2vec_model.bin"
                ]
            },
            {
                "title": "🌐 GloVe (Global Vectors)",
                "desc": "Menggabungkan matrix factorization global dengan konteks lokal. Menghasilkan vektor yang menangkap statistik co-occurrence kata.",
                "points": [
                    "Dense vector (50 dimensi)",
                    "Berbasis global co-occurrence matrix",
                    "Pretrained: Wikipedia + Gigaword",
                    "Model lokal: glove.6B.50d.txt"
                ]
            }
        ]

        for info in embed_info:
            st.markdown(f"""
<div class='card' style='padding:22px;'>
<div style='font-family:Sora; font-weight:700; font-size:0.95rem; margin-bottom:8px;'>{info["title"]}</div>
<div style='font-size:0.85rem; color:var(--text-secondary); line-height:1.6; margin-bottom:10px;'>{info["desc"]}</div>
<div>{"".join([f"<span class='badge'>{p}</span>" for p in info["points"]])}</div>
</div>
""", unsafe_allow_html=True)

    # ── TAB 3: Contextual Embedding ──
    with tabs[2]:
        st.markdown("""
<div class='card-static'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:6px;'>🔮 Contextual Embedding (BERT)</div>
<div style='font-size:0.85rem; color:var(--text-secondary); line-height:1.6;'>
Bidirectional Encoder Representations from Transformers — model yang memahami konteks
bidirectional. Setiap kata mendapatkan vektor berbeda tergantung konteks kalimatnya.
</div>
</div>
""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:0.92rem; margin-bottom:8px;'>🤖 BERT Embedding (all-MiniLM-L6-v2)</div>
<div style='font-size:0.85rem; color:var(--text-secondary); line-height:1.7;'>
Menggunakan Sentence Transformer untuk menghasilkan embedding tingkat kalimat (384 dimensi).
Model ini lebih ringan dari BERT-base namun tetap menangkap konteks kalimat secara efektif.
</div>
<div style='margin-top:10px;'>
<span class='badge'>384 dimensi</span>
<span class='badge'>Contextual</span>
<span class='badge'>Sentence-level</span>
</div>
</div>
""", unsafe_allow_html=True)

        with col2:
            st.markdown("""
<div class='card'>
<div style='font-family:Sora; font-weight:700; font-size:0.92rem; margin-bottom:8px;'>🚀 DistilBERT Fine-Tuning</div>
<div style='font-size:0.85rem; color:var(--text-secondary); line-height:1.7;'>
Model DistilBERT yang di-fine-tune secara khusus pada dataset Kisan Query.
Tidak menggunakan fitur terpisah, melainkan end-to-end learning dari teks ke kelas.
</div>
<div style='margin-top:10px;'>
<span class='badge'>768 dimensi (internal)</span>
<span class='badge'>End-to-end</span>
<span class='badge'>Fine-tuned</span>
</div>
</div>
""", unsafe_allow_html=True)

        # Static vs Contextual comparison
        st.markdown("""
<div class='card-static'>
<div style='font-family:Sora; font-weight:700; font-size:0.92rem; margin-bottom:10px;'>🔄 Static vs Contextual Embedding</div>
<div style='display:grid; grid-template-columns:1fr 1fr; gap:16px;'>
<div style='background:rgba(27,94,32,0.04); border-radius:10px; padding:16px;'>
<div style='font-weight:700; font-size:0.82rem; margin-bottom:6px;'>Static (Word2Vec / GloVe)</div>
<div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.6;'>
Kata "bank" selalu memiliki vektor yang sama, baik dalam konteks "river bank" maupun "bank account".
</div>
</div>
<div style='background:rgba(102,187,106,0.06); border-radius:10px; padding:16px;'>
<div style='font-weight:700; font-size:0.82rem; margin-bottom:6px;'>Contextual (BERT)</div>
<div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.6;'>
Kata "bank" di "river bank" dan "bank account" menghasilkan vektor yang berbeda sesuai konteks kalimat.
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)
