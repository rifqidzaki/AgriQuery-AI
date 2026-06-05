# ════════════════════════════════════════════════════════════════
# PAGE 02 — DATASET ANALYSIS
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
from components.metrics import render_metric_grid, render_section_header
from components.charts import plotly_pie, plotly_histogram, plotly_horizontal_bar, DUAL_COLORS
from backend.data_loader import preprocessing_steps, get_text_statistics, get_word_frequency


def render(ss):
    """Render the Dataset Analysis page."""
    df_raw = ss.get("df_raw")
    df_clean = ss.get("df_clean")

    if df_raw is None or df_clean is None:
        st.warning("Data belum dimuat.")
        return

    render_section_header(
        "Raw Data",
        "Dataset Explorer",
        "Eksplorasi dataset Kisan Query, distribusi label, panjang teks, dan frekuensi kata."
    )

    # ── Metrics ──
    stats = get_text_statistics(df_clean)
    total_raw = len(df_raw)
    missing = int(df_raw[["QueryText", "Sector"]].isnull().sum().sum())

    render_metric_grid([
        {"icon": "📦", "label": "Total Raw Rows", "value": f"{total_raw:,}"},
        {"icon": "✅", "label": "Clean Rows", "value": f"{stats['total_rows']:,}"},
        {"icon": "🌾", "label": "Agriculture", "value": f"{stats['agri_count']:,}"},
        {"icon": "🌿", "label": "Horticulture", "value": f"{stats['horti_count']:,}"},
        {"icon": "⚠️", "label": "Missing Values", "value": f"{missing:,}"},
        {"icon": "📏", "label": "Avg Text Length", "value": f"{stats['mean_chars']:.0f}", "unit": " chars"},
    ])

    # ── Charts Row ──
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("**📋 Sample Data (50 rows)**")
        show_cols = [c for c in ["QueryText", "Sector", "clean_text"] if c in df_clean.columns]
        st.dataframe(df_clean[show_cols].head(50), use_container_width=True, height=320)

    with col2:
        sector_counts = df_clean["Sector"].value_counts()
        fig_pie = plotly_pie(
            sector_counts.index.tolist(),
            sector_counts.values.tolist(),
            "Distribusi Label Sektor"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Text Length Distribution ──
    df_temp = df_clean.copy()
    df_temp["text_len"] = df_temp["QueryText"].astype(str).apply(len)
    fig_hist = plotly_histogram(
        df_temp, "text_len", "Sector",
        "Distribusi Panjang Teks per Sektor",
        nbins=60
    )
    fig_hist.update_layout(
        xaxis_title="Panjang Query (karakter)",
        yaxis_title="Jumlah"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # ── Word Frequency ──
    col3, col4 = st.columns(2)

    with col3:
        word_freq = get_word_frequency(df_clean, top_n=25)
        fig_wf = plotly_horizontal_bar(
            word_freq["Word"].tolist(),
            word_freq["Frequency"].tolist(),
            "Top 25 Kata Paling Sering"
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    with col4:
        # Token statistics comparison
        st.markdown("**📊 Statistik Token Sebelum & Sesudah Preprocessing**")
        stats_table = pd.DataFrame({
            "Statistik": ["Rata-rata token", "Median token", "Max token", "Min token"],
            "Sebelum (Raw)": [
                f"{stats['raw_mean_tokens']:.1f}",
                f"{stats['raw_median_tokens']:.1f}",
                f"{stats['raw_max_tokens']}",
                f"{stats['raw_min_tokens']}"
            ],
            "Sesudah (Clean)": [
                f"{stats['clean_mean_tokens']:.1f}",
                f"{stats['clean_median_tokens']:.1f}",
                f"{stats['clean_max_tokens']}",
                f"{stats['clean_min_tokens']}"
            ]
        })
        st.dataframe(stats_table, use_container_width=True, hide_index=True)

        # Number of classes
        st.markdown(f"""
<div class='glass-card' style='margin-top:16px; padding:20px;'>
<div style='font-family:Sora; font-weight:700; margin-bottom:8px;'>📊 Ringkasan Dataset</div>
<div style='font-size:0.88rem; color:var(--text-secondary); line-height:1.8;'>
• <strong>Jumlah Kelas:</strong> 2 (Agriculture, Horticulture)<br>
• <strong>Dataset Source:</strong> Kisan Call Centre (KCC)<br>
• <strong>Task Type:</strong> Binary Text Classification<br>
• <strong>Split Ratio:</strong> 80% Train / 20% Test
</div>
</div>
""", unsafe_allow_html=True)

    # ── Preprocessing Demo ──
    st.markdown("---")
    render_section_header("NLP Pipeline", "Preprocessing Demo", "Lihat tahap-tahap pembersihan teks secara interaktif.")

    sample_texts = df_clean["QueryText"].dropna().sample(5, random_state=7).tolist()
    sample_labels = [f"Contoh {i+1}: {t[:60]}..." for i, t in enumerate(sample_texts)]
    sample_labels.insert(0, "✏️ Ketik teks sendiri")

    choice = st.selectbox("Pilih contoh teks:", sample_labels, key="ds_prep_select")
    if choice.startswith("✏️"):
        input_text = st.text_area("Masukkan teks:", height=80,
                                  placeholder="Example: My rice plant leaves are turning yellow...",
                                  key="ds_prep_input")
    else:
        idx = sample_labels.index(choice) - 1
        input_text = sample_texts[idx]
        st.text_area("Teks input:", value=input_text, height=60, key="ds_prep_display", disabled=True)

    if input_text and input_text.strip():
        steps = preprocessing_steps(input_text)
        step_configs = [
            ("1️⃣ Original", "original", "#F3F4F6"),
            ("2️⃣ Lowercase", "lowercase", "#ECFDF5"),
            ("3️⃣ Hapus Tanda Baca", "no_punct", "#FEF3C7"),
            ("4️⃣ Normalisasi Spasi", "normalized", "#EDE9FE"),
            ("5️⃣ Stopword Removal + Filter", "clean", "#D1FAE5"),
        ]
        for label, key, bg in step_configs:
            val = steps[key]
            n_tokens = len(val.split()) if val else 0
            st.markdown(f"""
<div class='step-card' style='background:{bg};'>
<div class='step-label'>
{label} &nbsp;<span class='step-token-badge'>{n_tokens} token</span>
</div>
<div class='step-text'>{val}</div>
</div>
""", unsafe_allow_html=True)
