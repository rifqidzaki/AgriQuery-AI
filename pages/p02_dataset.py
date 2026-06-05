# ════════════════════════════════════════════════════════════════
# PAGE 02 — DATASET OVERVIEW
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
from backend.data_loader import get_text_statistics, get_word_frequency
from components.charts import plotly_pie, plotly_bar, plotly_histogram


def render(ss):
    df_clean = ss.get("df_clean")
    df_raw = ss.get("df_raw")
    le = ss.get("le")

    st.markdown("""
<div class='section-header'>
<div class='section-title'>📂 Dataset Overview</div>
<div class='section-subtitle'>Eksplorasi dataset Kisan Query untuk klasifikasi pertanian</div>
</div>
""", unsafe_allow_html=True)

    if df_clean is None:
        st.warning("Data belum dimuat.")
        return

    stats = get_text_statistics(df_clean)

    # KPI Cards
    st.markdown(f"""
<div class='kpi-grid'>
<div class='kpi-card'>
<div class='kpi-icon'>📊</div>
<div class='kpi-label'>Total Data</div>
<div class='kpi-value'>{stats['total_rows']:,}</div>
<div class='kpi-sub'>Baris setelah filtering</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>📐</div>
<div class='kpi-label'>Jumlah Fitur</div>
<div class='kpi-value'>2</div>
<div class='kpi-sub'>QueryText & Sector</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>🏷️</div>
<div class='kpi-label'>Jumlah Kelas</div>
<div class='kpi-value'>{len(le.classes_) if le else 2}</div>
<div class='kpi-sub'>Target klasifikasi</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>📝</div>
<div class='kpi-label'>Rata-rata Token</div>
<div class='kpi-value'>{stats["clean_mean_tokens"]:.0f}</div>
<div class='kpi-sub'>Per dokumen (setelah cleaning)</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Distribution
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📈 Distribusi Kelas</div>
<div class='section-subtitle'>Proporsi kelas Agriculture dan Horticulture dalam dataset</div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_pie = plotly_pie(
            labels=["Agriculture", "Horticulture"],
            values=[stats["agri_count"], stats["horti_count"]],
            title="Proporsi Kelas"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_bar = plotly_bar(
            names=["Agriculture", "Horticulture"],
            values=[stats["agri_count"], stats["horti_count"]],
            title="Jumlah Data per Kelas",
            text_format=",d",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Word Length Distribution
    st.markdown(f"""
<div class='card-static'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:12px;'>📊 Statistik Teks</div>
<div style='display:grid; grid-template-columns:repeat(4,1fr); gap:16px;'>
<div><div class='kpi-label'>Token Rata-rata (Raw)</div><div style='font-size:1.1rem; font-weight:600;'>{stats["raw_mean_tokens"]:.1f}</div></div>
<div><div class='kpi-label'>Token Rata-rata (Clean)</div><div style='font-size:1.1rem; font-weight:600;'>{stats["clean_mean_tokens"]:.1f}</div></div>
<div><div class='kpi-label'>Token Maks</div><div style='font-size:1.1rem; font-weight:600;'>{stats["raw_max_tokens"]}</div></div>
<div><div class='kpi-label'>Karakter Rata-rata</div><div style='font-size:1.1rem; font-weight:600;'>{stats["mean_chars"]:.0f}</div></div>
</div>
</div>
""", unsafe_allow_html=True)

    # Top Words
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🔤 Kata Paling Sering Muncul</div>
</div>
""", unsafe_allow_html=True)

    word_freq = get_word_frequency(df_clean, top_n=20)
    fig_words = plotly_bar(
        names=word_freq["Word"].tolist(),
        values=word_freq["Frequency"].tolist(),
        title="Top 20 Kata dalam Dataset",
        text_format=",d"
    )
    st.plotly_chart(fig_words, use_container_width=True)

    # Dataset Preview
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🔍 Preview Dataset</div>
<div class='section-subtitle'>Menampilkan 10 baris pertama dari dataset yang sudah dibersihkan</div>
</div>
""", unsafe_allow_html=True)

    preview_cols = ["QueryText", "Sector", "clean_text"]
    available_cols = [c for c in preview_cols if c in df_clean.columns]
    st.dataframe(df_clean[available_cols].head(10), use_container_width=True)
