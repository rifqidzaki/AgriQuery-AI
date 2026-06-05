# ════════════════════════════════════════════════════════════════
# PAGE 10 — ABOUT RESEARCH
# ════════════════════════════════════════════════════════════════

import streamlit as st
from components.metrics import render_section_header, render_explain_card


def render(ss):
    """Render the About Research page."""

    render_section_header(
        "Research",
        "About This Research",
        "Informasi lengkap tentang penelitian, metodologi, dan kontribusi.",
        extra_badges=[{"text": "Academic Paper", "type": "gold"}]
    )

    # ── Research Objective ──
    st.markdown("""
<div class='research-card'>
<div class='research-card-title'>🎯 Tujuan Penelitian</div>
<div class='research-card-body'>
<ol style='padding-left:20px; line-height:2;'>
<li>Menganalisis dan membandingkan efektivitas representasi fitur <strong>NLP Klasik</strong> (Bag of Words, TF-IDF, N-Gram) dengan <strong>NLP Modern</strong> (Word2Vec, GloVe, BERT) dalam konteks klasifikasi teks.</li>
<li>Mengevaluasi performa dua algoritma machine learning — <strong>Decision Tree</strong> dan <strong>Multinomial Naive Bayes</strong> — pada dataset query pertanian.</li>
<li>Memberikan rekomendasi kombinasi <strong>model + representasi fitur terbaik</strong> untuk klasifikasi query pertanian.</li>
<li>Menganalisis <strong>error patterns</strong> dan memberikan insight tentang tantangan klasifikasi teks di domain pertanian.</li>
</ol>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Methodology ──
    st.markdown("""
<div class='research-card'>
<div class='research-card-title'>📐 Metodologi Penelitian</div>
<div class='research-card-body'>
<div style='display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px; margin-top:12px;'>
<div style='background:rgba(31,122,77,0.05); padding:16px; border-radius:12px; text-align:center;'>
<div style='font-size:1.5rem; margin-bottom:8px;'>1️⃣</div>
<div style='font-weight:700; font-size:0.88rem;'>Data Collection</div>
<div style='font-size:0.8rem; color:var(--text-muted); margin-top:4px;'>Kisan Query Analysis Dataset</div>
</div>
<div style='background:rgba(31,122,77,0.05); padding:16px; border-radius:12px; text-align:center;'>
<div style='font-size:1.5rem; margin-bottom:8px;'>2️⃣</div>
<div style='font-weight:700; font-size:0.88rem;'>Preprocessing</div>
<div style='font-size:0.8rem; color:var(--text-muted); margin-top:4px;'>Lowercase, punctuation, stopwords</div>
</div>
<div style='background:rgba(31,122,77,0.05); padding:16px; border-radius:12px; text-align:center;'>
<div style='font-size:1.5rem; margin-bottom:8px;'>3️⃣</div>
<div style='font-weight:700; font-size:0.88rem;'>Feature Extraction</div>
<div style='font-size:0.8rem; color:var(--text-muted); margin-top:4px;'>6 methods (3 classic + 3 modern)</div>
</div>
<div style='background:rgba(31,122,77,0.05); padding:16px; border-radius:12px; text-align:center;'>
<div style='font-size:1.5rem; margin-bottom:8px;'>4️⃣</div>
<div style='font-weight:700; font-size:0.88rem;'>Model Training</div>
<div style='font-size:0.8rem; color:var(--text-muted); margin-top:4px;'>DT + NB × 6 features = 12 models</div>
</div>
<div style='background:rgba(31,122,77,0.05); padding:16px; border-radius:12px; text-align:center;'>
<div style='font-size:1.5rem; margin-bottom:8px;'>5️⃣</div>
<div style='font-weight:700; font-size:0.88rem;'>Evaluation</div>
<div style='font-size:0.8rem; color:var(--text-muted); margin-top:4px;'>Accuracy, Precision, Recall, F1</div>
</div>
<div style='background:rgba(31,122,77,0.05); padding:16px; border-radius:12px; text-align:center;'>
<div style='font-size:1.5rem; margin-bottom:8px;'>6️⃣</div>
<div style='font-weight:700; font-size:0.88rem;'>Analysis</div>
<div style='font-size:0.8rem; color:var(--text-muted); margin-top:4px;'>Error analysis + Explainability</div>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── NLP Classic vs Modern ──
    st.markdown("---")
    st.markdown("""
<div class='glass-card'>
<div style='font-family:Sora; font-weight:700; font-size:1.15rem; margin-bottom:16px;'>🔄 NLP Klasik vs Modern — Ringkasan</div>
<table class='comparison-table' style='width:100%;'>
<tr><th>Aspek</th><th>NLP Klasik</th><th>NLP Modern</th></tr>
<tr>
<td><strong>Metode</strong></td>
<td>BoW, TF-IDF, N-Gram</td>
<td>Word2Vec, GloVe, BERT</td>
</tr>
<tr>
<td><strong>Representasi</strong></td>
<td>Sparse, high-dimensional</td>
<td>Dense, low-dimensional</td>
</tr>
<tr>
<td><strong>Semantic</strong></td>
<td>❌ Tidak ada</td>
<td>✅ Menangkap makna semantik</td>
</tr>
<tr>
<td><strong>Context</strong></td>
<td>❌ Context-free</td>
<td>✅ BERT: Contextual</td>
</tr>
<tr>
<td><strong>Training</strong></td>
<td>Dari dataset saja</td>
<td>Pretrained + Transfer Learning</td>
</tr>
<tr>
<td><strong>Kecepatan</strong></td>
<td>⚡ Sangat cepat</td>
<td>🐢 Lebih lambat</td>
</tr>
<tr>
<td><strong>Interpretability</strong></td>
<td>✅ Mudah diinterpretasi</td>
<td>❌ Black box</td>
</tr>
<tr>
<td><strong>Scalability</strong></td>
<td>⚠️ Curse of dimensionality</td>
<td>✅ Fixed dimensionality</td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)

    # ── Contributions ──
    st.markdown("""
<div class='research-card'>
<div class='research-card-title'>🏆 Kontribusi Penelitian</div>
<div class='research-card-body'>
<div style='display:grid; grid-template-columns:1fr 1fr; gap:16px;'>
<div style='background:rgba(31,122,77,0.04); padding:16px; border-radius:12px; border:1px solid rgba(31,122,77,0.08);'>
<div style='font-weight:700; margin-bottom:6px;'>📊 Comparative Analysis</div>
<div style='font-size:0.85rem; color:var(--text-secondary);'>Perbandingan komprehensif 12 kombinasi model-fitur pada domain pertanian.</div>
</div>
<div style='background:rgba(31,122,77,0.04); padding:16px; border-radius:12px; border:1px solid rgba(31,122,77,0.08);'>
<div style='font-weight:700; margin-bottom:6px;'>🔍 Error Insight</div>
<div style='font-size:0.85rem; color:var(--text-secondary);'>Analisis mendalam tentang pola error dan query yang sulit diklasifikasikan.</div>
</div>
<div style='background:rgba(31,122,77,0.04); padding:16px; border-radius:12px; border:1px solid rgba(31,122,77,0.08);'>
<div style='font-weight:700; margin-bottom:6px;'>💡 Explainable NLP</div>
<div style='font-size:0.85rem; color:var(--text-secondary);'>Feature importance dan keyword contribution analysis untuk interpretabilitas model.</div>
</div>
<div style='background:rgba(31,122,77,0.04); padding:16px; border-radius:12px; border:1px solid rgba(31,122,77,0.08);'>
<div style='font-weight:700; margin-bottom:6px;'>🚀 Interactive Dashboard</div>
<div style='font-size:0.85rem; color:var(--text-secondary);'>Platform visualisasi interaktif untuk eksplorasi dan presentasi hasil penelitian.</div>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Future Work ──
    st.markdown("""
<div class='research-card'>
<div class='research-card-title'>🔮 Future Work</div>
<div class='research-card-body' style='line-height:2;'>
<div>1. 🧪 <strong>Fine-tuning BERT</strong> — Melatih model BERT khusus domain pertanian untuk meningkatkan akurasi embedding.</div>
<div>2. 🌐 <strong>Multilingual Support</strong> — Menambahkan dukungan untuk query dalam bahasa regional India (Hindi, Tamil, dll).</div>
<div>3. 📊 <strong>Multi-class Classification</strong> — Memperluas ke lebih banyak sektor pertanian (Fisheries, Animal Husbandry, dll).</div>
<div>4. 🤖 <strong>Deep Learning Models</strong> — Membandingkan dengan LSTM, CNN, dan Transformer-based classifiers.</div>
<div>5. 🔍 <strong>Full SHAP Analysis</strong> — Implementasi SHAP values untuk explainability yang lebih mendalam.</div>
<div>6. 📱 <strong>Mobile Deployment</strong> — Deploy model terbaik sebagai chatbot mobile untuk petani.</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Tech Stack ──
    st.markdown("---")
    render_section_header("Stack", "Technology Stack", "Tools dan library yang digunakan dalam penelitian ini.")

    tech_items = [
        ("🐍", "Python", "Core language"),
        ("📊", "Streamlit", "Dashboard framework"),
        ("📈", "Plotly", "Interactive visualization"),
        ("🤖", "Scikit-learn", "ML models"),
        ("📝", "NLTK", "Text preprocessing"),
        ("🧠", "Gensim", "Word2Vec & GloVe"),
        ("🤗", "Sentence Transformers", "BERT embeddings"),
        ("🔥", "HuggingFace", "Pretrained models"),
        ("🐼", "Pandas", "Data manipulation"),
        ("🔢", "NumPy", "Numerical computing"),
    ]

    pills_html = " ".join([
        f"<span class='tech-pill'>{icon} {name}</span>"
        for icon, name, desc in tech_items
    ])
    st.markdown(f"<div style='margin:16px 0;'>{pills_html}</div>", unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("""
<div style='text-align:center; padding:40px 0 20px; color:var(--text-muted); font-size:0.82rem;'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; color:var(--text-main); margin-bottom:8px;'>AgriMind AI — NLP Analytics Platform</div>
<div>Analisis Perbandingan Representasi Fitur NLP Klasik dan Modern</div>
<div>pada Klasifikasi Query Pertanian Menggunakan Decision Tree dan Naive Bayes</div>
<div style='margin-top:12px; color:var(--text-muted); opacity:0.5;'>v5.0 Research Edition • 2025</div>
</div>
""", unsafe_allow_html=True)
