# ════════════════════════════════════════════════════════════════
# PAGE: AUGMENTATION ANALYSIS
# ════════════════════════════════════════════════════════════════

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from backend.research_data import (
    DATASET_ORIGINAL, DATASET_AUGMENTED, AUGMENTATION_METHODS
)


def render(ss):
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🔬 Augmentation Analysis</div>
<div class='section-subtitle'>Analisis dampak data augmentasi terhadap distribusi kelas dan ketidakseimbangan data</div>
</div>
""", unsafe_allow_html=True)

    # ── Before / After Summary Cards ────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📊 Sebelum vs Sesudah Augmentasi</div>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        orig = DATASET_ORIGINAL
        st.markdown(f"""
<div class='card' style='border-left:4px solid #E74C3C;'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:16px; color:#E74C3C;'>
📁 Dataset Original
</div>
<div style='display:grid; grid-template-columns:1fr 1fr; gap:12px;'>
<div style='background:rgba(231,76,60,0.06); padding:12px; border-radius:8px;'>
<div style='font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;'>Total Data</div>
<div style='font-family:Sora; font-size:1.4rem; font-weight:700;'>{orig["total"]:,}</div>
</div>
<div style='background:rgba(231,76,60,0.06); padding:12px; border-radius:8px;'>
<div style='font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;'>Imbalance Ratio</div>
<div style='font-family:Sora; font-size:1.4rem; font-weight:700; color:#E74C3C;'>{orig["imbalance_ratio"]:.1f}:1</div>
</div>
<div style='background:rgba(231,76,60,0.06); padding:12px; border-radius:8px;'>
<div style='font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;'>Agriculture</div>
<div style='font-family:Sora; font-size:1.2rem; font-weight:700;'>{orig["agriculture"]:,}</div>
</div>
<div style='background:rgba(231,76,60,0.06); padding:12px; border-radius:8px;'>
<div style='font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;'>Horticulture</div>
<div style='font-family:Sora; font-size:1.2rem; font-weight:700; color:#E74C3C;'>{orig["horticulture"]:,}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        pct_change = ((DATASET_AUGMENTED["horticulture"] - DATASET_ORIGINAL["horticulture"])
                      / DATASET_ORIGINAL["horticulture"] * 100)
        st.markdown(f"""
<div style='display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; padding:20px 0;'>
<div style='font-size:2rem; margin-bottom:8px;'>→</div>
<div style='text-align:center;'>
<div style='font-size:0.75rem; color:var(--text-muted); margin-bottom:4px;'>Augmentasi</div>
<div style='font-family:Sora; font-weight:700; font-size:1.1rem; color:var(--primary);'>
HORTICULTURE<br>×5.0
</div>
<div style='font-size:0.75rem; color:var(--primary); margin-top:6px;'>+{pct_change:.0f}%</div>
</div>
</div>
""", unsafe_allow_html=True)

    with col3:
        aug = DATASET_AUGMENTED
        st.markdown(f"""
<div class='card' style='border-left:4px solid var(--primary);'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:16px; color:var(--primary);'>
✅ Dataset Augmented
</div>
<div style='display:grid; grid-template-columns:1fr 1fr; gap:12px;'>
<div style='background:rgba(27,94,32,0.06); padding:12px; border-radius:8px;'>
<div style='font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;'>Total Data</div>
<div style='font-family:Sora; font-size:1.4rem; font-weight:700;'>{aug["total"]:,}</div>
</div>
<div style='background:rgba(27,94,32,0.06); padding:12px; border-radius:8px;'>
<div style='font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;'>Imbalance Ratio</div>
<div style='font-family:Sora; font-size:1.4rem; font-weight:700; color:var(--primary);'>{aug["imbalance_ratio"]:.2f}:1</div>
</div>
<div style='background:rgba(27,94,32,0.06); padding:12px; border-radius:8px;'>
<div style='font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;'>Agriculture</div>
<div style='font-family:Sora; font-size:1.2rem; font-weight:700;'>{aug["agriculture"]:,}</div>
</div>
<div style='background:rgba(27,94,32,0.06); padding:12px; border-radius:8px;'>
<div style='font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;'>Horticulture</div>
<div style='font-family:Sora; font-size:1.2rem; font-weight:700; color:var(--primary);'>{aug["horticulture"]:,} ↑</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Pie Charts ───────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig_orig = go.Figure(go.Pie(
            labels=["AGRICULTURE", "HORTICULTURE"],
            values=[DATASET_ORIGINAL["agriculture"], DATASET_ORIGINAL["horticulture"]],
            hole=0.45,
            marker_colors=["#2E7D32", "#E74C3C"],
        ))
        fig_orig.update_layout(
            title="Distribusi Kelas — Original",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        )
        st.plotly_chart(fig_orig, use_container_width=True)

    with c2:
        fig_aug = go.Figure(go.Pie(
            labels=["AGRICULTURE", "HORTICULTURE"],
            values=[DATASET_AUGMENTED["agriculture"], DATASET_AUGMENTED["horticulture"]],
            hole=0.45,
            marker_colors=["#2E7D32", "#66BB6A"],
        ))
        fig_aug.update_layout(
            title="Distribusi Kelas — Augmented",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        )
        st.plotly_chart(fig_aug, use_container_width=True)

    # ── Bar Chart Comparison ─────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📈 Perbandingan Distribusi Kelas</div>
</div>
""", unsafe_allow_html=True)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Original",
        x=["AGRICULTURE", "HORTICULTURE"],
        y=[DATASET_ORIGINAL["agriculture"], DATASET_ORIGINAL["horticulture"]],
        marker_color=["#2E7D32", "#E74C3C"],
        text=[f"{DATASET_ORIGINAL['agriculture']:,}", f"{DATASET_ORIGINAL['horticulture']:,}"],
        textposition="outside",
    ))
    fig_bar.add_trace(go.Bar(
        name="Augmented",
        x=["AGRICULTURE", "HORTICULTURE"],
        y=[DATASET_AUGMENTED["agriculture"], DATASET_AUGMENTED["horticulture"]],
        marker_color=["#1B5E20", "#66BB6A"],
        text=[f"{DATASET_AUGMENTED['agriculture']:,}", f"{DATASET_AUGMENTED['horticulture']:,}"],
        textposition="outside",
    ))
    fig_bar.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Kelas"),
        yaxis=dict(title="Jumlah Data"),
        font=dict(family="Inter", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        height=400,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── Augmentation Methods ─────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🛠️ Metode Augmentasi yang Digunakan</div>
<div class='section-subtitle'>4 teknik augmentasi teks diterapkan secara bertahap pada kelas HORTICULTURE</div>
</div>
""", unsafe_allow_html=True)

    cols = st.columns(4)
    for col, method in zip(cols, AUGMENTATION_METHODS):
        with col:
            st.markdown(f"""
<div class='card' style='text-align:center; min-height:180px;'>
<div style='font-size:2rem; margin-bottom:10px;'>{method['icon']}</div>
<div style='font-family:Sora; font-weight:700; font-size:0.85rem; margin-bottom:8px; color:var(--primary);'>
{method['name']}
</div>
<div style='font-size:0.78rem; color:var(--text-secondary); line-height:1.6;'>{method['desc']}</div>
</div>
""", unsafe_allow_html=True)

    # ── Imbalance Ratio Reduction ────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
<div class='insight-card'>
✅ <b>Hasil Augmentasi:</b> Imbalance ratio berhasil diturunkan dari 
<b style='color:#E74C3C;'>12.0:1</b> menjadi <b style='color:var(--primary);'>2.40:1</b>.
Jumlah sampel HORTICULTURE meningkat <b>5×</b> dari 766 menjadi 3.830 data.
Total dataset bertambah dari <b>9.939</b> menjadi <b>13.003</b> baris.
</div>
""", unsafe_allow_html=True)
