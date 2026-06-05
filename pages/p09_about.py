# ════════════════════════════════════════════════════════════════
# PAGE 09 — ABOUT PROJECT
# ════════════════════════════════════════════════════════════════

import streamlit as st


def render(ss):
    st.markdown("""
<div class='section-header'>
<div class='section-title'>ℹ️ About Project</div>
<div class='section-subtitle'>Informasi detail mengenai penelitian dan metodologi yang digunakan</div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
<div class='card-static'>
<div style='font-family:Sora; font-weight:700; font-size:1.1rem; margin-bottom:12px; color:var(--primary);'>
Analisis Perbandingan Representasi Fitur NLP Klasik dan Modern pada Klasifikasi Query Pertanian
</div>
<div style='font-size:0.9rem; color:var(--text-main); line-height:1.7; margin-bottom:20px;'>
Penelitian ini bertujuan untuk mengevaluasi dan membandingkan performa berbagai teknik representasi fitur teks (Natural Language Processing) dalam mengklasifikasikan pertanyaan (query) pertanian ke dalam dua kategori utama: <b>Agriculture</b> dan <b>Horticulture</b>.
</div>

<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:8px;'>🎯 Metodologi Penelitian</div>
<ol style='font-size:0.9rem; color:var(--text-secondary); line-height:1.7; margin-bottom:20px;'>
<li><b>Pengumpulan Data:</b> Menggunakan dataset Kisan Query berbahasa Inggris.</li>
<li><b>Preprocessing:</b> Membersihkan teks melalui proses case folding, punctuation removal, normalisasi, dan stopword removal.</li>
<li><b>Ekstraksi Fitur (Classical NLP):</b> Mengubah teks menjadi vektor numerik menggunakan metode berbasis frekuensi (BoW, TF-IDF, N-Gram).</li>
<li><b>Word Embedding (Modern NLP):</b> Memanfaatkan model pre-trained (Word2Vec, GloVe, BERT) untuk menangkap konteks semantik kata.</li>
<li><b>Pemodelan:</b> Melatih algoritma <i>Decision Tree</i> dan <i>Naive Bayes</i> untuk setiap representasi fitur.</li>
<li><b>Fine-Tuning:</b> Melatih model <i>DistilBERT</i> secara <i>end-to-end</i> sebagai pembanding transformer modern.</li>
<li><b>Evaluasi:</b> Membandingkan performa menggunakan metrik Accuracy, Precision, Recall, F1-Score, dan Inference Time.</li>
</ol>

<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:8px;'>📈 Kesimpulan Utama</div>
<div style='font-size:0.9rem; color:var(--text-secondary); line-height:1.7;'>
Dari hasil evaluasi 13 model, terlihat bahwa pemilihan representasi fitur sangat mempengaruhi performa algoritma klasifikasi. Representasi kontekstual (BERT dan DistilBERT) umumnya menghasilkan performa terbaik dalam menangani nuansa bahasa, sementara model klasik (TF-IDF) menawarkan baseline yang kuat dengan waktu komputasi yang jauh lebih efisien.
</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class='card'>
<div style='text-align:center; padding:10px 0;'>
<div style='font-size:3rem; margin-bottom:10px;'>🎓</div>
<div style='font-family:Sora; font-weight:700; font-size:1.1rem; margin-bottom:4px;'>Proyek Akhir / Skripsi</div>
<div style='font-size:0.85rem; color:var(--text-muted); margin-bottom:20px;'>Dashboard NLP Pertanian v6.0</div>

<div style='text-align:left; background:rgba(27,94,32,0.04); padding:16px; border-radius:10px; margin-bottom:16px;'>
<div style='font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; font-weight:600; margin-bottom:4px;'>Dataset</div>
<div style='font-size:0.85rem; font-weight:600;'>Kisan Query Dataset</div>
<div style='font-size:0.8rem; color:var(--text-secondary);'>5,000 baris (subset)</div>
</div>

<div style='text-align:left; background:rgba(27,94,32,0.04); padding:16px; border-radius:10px; margin-bottom:16px;'>
<div style='font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; font-weight:600; margin-bottom:4px;'>Teknologi</div>
<div style='font-size:0.85rem; font-weight:600;'>Python, Streamlit</div>
<div style='font-size:0.8rem; color:var(--text-secondary);'>Scikit-learn, Gensim, Transformers (Hugging Face), Plotly</div>
</div>

<div style='text-align:left; background:rgba(27,94,32,0.04); padding:16px; border-radius:10px;'>
<div style='font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; font-weight:600; margin-bottom:4px;'>Domain</div>
<div style='font-size:0.85rem; font-weight:600;'>Pertanian (Agriculture)</div>
<div style='font-size:0.8rem; color:var(--text-secondary);'>Klasifikasi sentimen & sektor</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)
