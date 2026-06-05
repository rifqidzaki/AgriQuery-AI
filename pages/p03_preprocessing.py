# ════════════════════════════════════════════════════════════════
# PAGE 03 — PREPROCESSING
# ════════════════════════════════════════════════════════════════

import streamlit as st
from backend.data_loader import preprocessing_steps


def render(ss):
    df_clean = ss.get("df_clean")

    st.markdown("""
<div class='section-header'>
<div class='section-title'>🧹 Preprocessing Pipeline</div>
<div class='section-subtitle'>Visualisasi tahapan pembersihan teks dari data mentah hingga siap diproses</div>
</div>
""", unsafe_allow_html=True)

    # Pipeline Diagram
    st.markdown("""
<div class='card-static' style='text-align:center;'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:16px;'>📋 Alur Pipeline Preprocessing</div>
<div style='display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:8px; font-size:0.85rem;'>
<span class='badge' style='padding:8px 16px; font-size:0.78rem;'>📄 Raw Text</span>
<span style='color:var(--accent); font-size:1.2rem;'>→</span>
<span class='badge' style='padding:8px 16px; font-size:0.78rem;'>🔡 Case Folding</span>
<span style='color:var(--accent); font-size:1.2rem;'>→</span>
<span class='badge' style='padding:8px 16px; font-size:0.78rem;'>✂️ Punctuation Removal</span>
<span style='color:var(--accent); font-size:1.2rem;'>→</span>
<span class='badge' style='padding:8px 16px; font-size:0.78rem;'>🚫 Stopword Removal</span>
<span style='color:var(--accent); font-size:1.2rem;'>→</span>
<span class='badge' style='padding:8px 16px; font-size:0.78rem;'>🧹 Text Cleaning</span>
<span style='color:var(--accent); font-size:1.2rem;'>→</span>
<span class='badge-gold' style='padding:8px 16px; font-size:0.78rem;'>⚙️ Feature Extraction</span>
</div>
</div>
""", unsafe_allow_html=True)

    # Step explanations
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📖 Penjelasan Tiap Tahapan</div>
</div>
""", unsafe_allow_html=True)

    steps_info = [
        ("🔡", "Case Folding", "Mengubah seluruh huruf menjadi huruf kecil (lowercase) untuk memastikan konsistensi. Contoh: 'AGRICULTURE' → 'agriculture'."),
        ("✂️", "Punctuation Removal", "Menghapus semua karakter non-alfabet (angka, tanda baca, simbol khusus) sehingga hanya tersisa huruf dan spasi."),
        ("🚫", "Stopword Removal", "Menghapus kata-kata umum yang tidak memiliki makna signifikan (the, is, in, at, dll.) menggunakan pustaka NLTK."),
        ("🧹", "Normalisasi Spasi", "Menghapus spasi berlebih dan karakter pendek (≤1 huruf) untuk menghasilkan teks yang bersih dan terstruktur."),
    ]

    for icon, title, desc in steps_info:
        st.markdown(f"""
<div class='card' style='padding:18px 22px;'>
<div style='display:flex; align-items:flex-start; gap:14px;'>
<div style='font-size:1.4rem; min-width:36px; text-align:center;'>{icon}</div>
<div>
<div style='font-family:Sora; font-weight:700; font-size:0.92rem; margin-bottom:4px;'>{title}</div>
<div style='font-size:0.85rem; color:var(--text-secondary); line-height:1.6;'>{desc}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Interactive Demo
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🔬 Demo Transformasi Teks</div>
<div class='section-subtitle'>Masukkan teks untuk melihat hasil setiap tahapan preprocessing secara real-time</div>
</div>
""", unsafe_allow_html=True)

    # Default sample text
    sample_texts = []
    if df_clean is not None and len(df_clean) > 0:
        sample_texts = df_clean["QueryText"].head(5).tolist()

    default_text = sample_texts[0] if sample_texts else "What is the best FERTILIZER for growing Tomatoes in Summer?!"
    user_text = st.text_area("Masukkan teks untuk di-preprocessing:", value=default_text, height=80)

    if user_text:
        steps = preprocessing_steps(user_text)
        step_labels = [
            ("📄 TEKS ASLI", "original"),
            ("🔡 CASE FOLDING", "case_folding"),
            ("✂️ PUNCTUATION REMOVAL", "punctuation_removal"),
            ("🧹 NORMALISASI", "normalization"),
            ("🚫 STOPWORD REMOVAL", "stopword_removal"),
            ("✅ HASIL AKHIR", "final"),
        ]

        for label, key in step_labels:
            text_val = steps[key]
            token_count = len(text_val.split()) if text_val.strip() else 0
            st.markdown(f"""
<div class='step-card' style='background:{"rgba(102,187,106,0.06)" if key == "final" else "var(--bg-card)"};'>
<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>
<span class='step-label'>{label}</span>
<span class='step-token-badge'>{token_count} token</span>
</div>
<div class='step-text'>{text_val}</div>
</div>
""", unsafe_allow_html=True)

    # Sample from dataset
    if df_clean is not None and len(sample_texts) > 1:
        st.markdown("""
<div class='section-header'>
<div class='section-title'>📋 Contoh dari Dataset</div>
<div class='section-subtitle'>Perbandingan teks asli vs teks bersih dari dataset</div>
</div>
""", unsafe_allow_html=True)

        preview = df_clean[["QueryText", "Sector", "clean_text"]].head(5)
        preview.columns = ["Teks Asli", "Kategori", "Teks Bersih"]
        st.dataframe(preview, use_container_width=True)
