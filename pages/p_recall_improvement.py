# ════════════════════════════════════════════════════════════════
# PAGE: RECALL IMPROVEMENT ANALYSIS
# ════════════════════════════════════════════════════════════════

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from backend.research_data import RECALL_IMPROVEMENTS


def render(ss):
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📈 Recall Improvement Analysis</div>
<div class='section-subtitle'>Perbandingan peningkatan recall pada setiap model setelah augmentasi data</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class='insight-card' style='margin-bottom:24px;'>
📌 <b>Metrik Utama: Recall</b> — Recall dipilih sebagai metrik utama evaluasi karena 
pada kasus <b>class imbalance</b> seperti ini (12:1), akurasi bisa menyesatkan 
(model yang selalu prediksi "Agriculture" pun bisa memiliki akurasi >90%). 
Recall mengukur kemampuan model mendeteksi kelas minoritas (HORTICULTURE) yang menjadi fokus peningkatan.
</div>
""", unsafe_allow_html=True)

    sorted_data = sorted(RECALL_IMPROVEMENTS, key=lambda x: x["delta"], reverse=True)

    # ── Top 5 Highlight Cards ────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🚀 Top 5 Peningkatan Recall Terbesar</div>
</div>
""", unsafe_allow_html=True)

    top5 = sorted_data[:5]
    cols = st.columns(5)
    for col, item in zip(cols, top5):
        delta_pct = item["delta"] * 100
        with col:
            st.markdown(f"""
<div class='card' style='text-align:center; border-top:4px solid var(--primary);'>
<div style='font-family:Sora; font-weight:700; font-size:0.85rem; margin-bottom:12px; line-height:1.3;'>{item['name']}</div>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>Original</div>
<div style='font-weight:600;'>{item['orig']*100:.2f}%</div>
<div style='font-size:1.2rem; color:var(--primary); margin:6px 0;'>↑</div>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>Augmented</div>
<div style='font-weight:600;'>{item['aug']*100:.2f}%</div>
<div style='background:var(--primary); color:white; border-radius:8px; padding:8px; margin-top:10px;'>
<div style='font-size:0.65rem; opacity:0.8;'>Peningkatan</div>
<div style='font-family:Sora; font-weight:800; font-size:1.3rem;'>+{delta_pct:.2f}%</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Full Horizontal Bar Chart ────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📊 Recall Improvement — Seluruh 15 Model</div>
<div class='section-subtitle'>Delta recall (Augmented − Original). Positif = meningkat, Negatif = menurun</div>
</div>
""", unsafe_allow_html=True)

    names = [r["name"] for r in sorted_data]
    deltas = [r["delta"] * 100 for r in sorted_data]
    bar_colors = ["#E74C3C" if d < 0 else "#1B5E20" for d in deltas]

    fig = go.Figure(go.Bar(
        x=deltas,
        y=names,
        orientation="h",
        marker_color=bar_colors,
        text=[f"{'+' if d >= 0 else ''}{d:.2f}%" for d in deltas],
        textposition="outside",
    ))
    fig.add_vline(x=0, line_width=1.5, line_color="#999", line_dash="dash")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Delta Recall (%)"),
        yaxis=dict(autorange="reversed"),
        font=dict(family="Inter", size=11),
        height=500,
        margin=dict(l=190, r=80, t=20, b=60),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Before vs After Chart ────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📉📈 Recall Sebelum vs Sesudah Augmentasi</div>
</div>
""", unsafe_allow_html=True)

    names_all = [r["name"] for r in sorted_data]
    orig_vals = [r["orig"] * 100 for r in sorted_data]
    aug_vals = [r["aug"] * 100 for r in sorted_data]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=names_all, y=orig_vals,
        mode="markers+lines",
        name="Original",
        marker=dict(color="#E74C3C", size=9),
        line=dict(color="#E74C3C", width=2, dash="dot"),
    ))
    fig2.add_trace(go.Scatter(
        x=names_all, y=aug_vals,
        mode="markers+lines",
        name="Augmented",
        marker=dict(color="#1B5E20", size=9),
        line=dict(color="#1B5E20", width=2),
    ))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickangle=-35),
        yaxis=dict(title="Recall (%)", range=[40, 105]),
        font=dict(family="Inter", size=11),
        legend=dict(orientation="h", yanchor="bottom", y=-0.4),
        height=420,
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Full Table ───────────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📋 Tabel Lengkap Recall Improvement</div>
</div>
""", unsafe_allow_html=True)

    table = []
    for r in sorted_data:
        delta_str = f"+{r['delta']*100:.2f}%" if r["delta"] >= 0 else f"{r['delta']*100:.2f}%"
        table.append({
            "Model": r["name"],
            "Recall Original (%)": f"{r['orig']*100:.2f}",
            "Recall Augmented (%)": f"{r['aug']*100:.2f}",
            "Delta (%)": delta_str,
        })
    df_table = pd.DataFrame(table)
    st.dataframe(df_table, use_container_width=True, hide_index=True)

    # ── Auto Insights ────────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>💡 Insight Otomatis</div>
</div>
""", unsafe_allow_html=True)

    best = sorted_data[0]
    worst = sorted_data[-1]
    avg_delta = sum(r["delta"] for r in sorted_data) / len(sorted_data) * 100
    improved = sum(1 for r in sorted_data if r["delta"] > 0)

    st.markdown(f"""
<div class='insight-card'>
🚀 <b>{best['name']}</b> mengalami peningkatan recall terbesar sebesar 
<b>+{best['delta']*100:.2f}%</b> (dari {best['orig']*100:.2f}% menjadi {best['aug']*100:.2f}%). 
Model berbasis embedding statis seperti Word2Vec mendapat manfaat terbesar karena sebelumnya 
sangat kesulitan mengenali pola kelas minoritas HORTICULTURE dengan distribusi data yang sangat timpang.
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class='insight-card'>
📊 Secara rata-rata, augmentasi data meningkatkan recall sebesar <b>+{avg_delta:.2f}%</b>. 
Sebanyak <b>{improved} dari {len(sorted_data)} model</b> mengalami peningkatan recall, 
membuktikan bahwa data augmentasi efektif mengatasi masalah class imbalance pada dataset teks pertanian ini.
</div>
""", unsafe_allow_html=True)

    if worst["delta"] < 0:
        st.markdown(f"""
<div class='insight-card'>
⚠️ <b>{worst['name']}</b> merupakan satu-satunya model yang mengalami penurunan recall 
(<b>{worst['delta']*100:.2f}%</b>). Hal ini kemungkinan disebabkan oleh distribusi embedding BERT 
yang sudah cukup kompak sehingga data augmentasi justru menambah noise ke dalam distribusi fitur.
</div>
""", unsafe_allow_html=True)
