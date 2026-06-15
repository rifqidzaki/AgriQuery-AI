# ════════════════════════════════════════════════════════════════
# PAGE: DISTILBERT ANALYSIS
# ════════════════════════════════════════════════════════════════

import streamlit as st
import plotly.graph_objects as go
from backend.research_data import DISTILBERT_RESULTS


def render(ss):
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🤖 DistilBERT Analysis</div>
<div class='section-subtitle'>Analisis mendalam performa DistilBERT Fine-Tuning pada dataset Original vs Augmented</div>
</div>
""", unsafe_allow_html=True)

    orig = DISTILBERT_RESULTS["original"]
    aug = DISTILBERT_RESULTS["augmented"]
    delta = DISTILBERT_RESULTS["delta"]

    # ── Comparison Cards ─────────────────────────────────────────
    c1, c2, c3 = st.columns([2, 2, 1])

    with c1:
        st.markdown(f"""
<div class='card' style='border-left:4px solid {orig["color"]};'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:16px; color:{orig["color"]};'>
📁 {orig["label"]}
</div>
<div style='font-size:0.75rem; color:var(--text-muted); margin-bottom:12px;'>Total Data: {orig["total_data"]:,} | Imbalance: 12.0:1</div>
<div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; text-align:center;'>
<div style='background:rgba(0,0,0,0.04); padding:14px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>Accuracy</div>
<div style='font-family:Sora; font-weight:700; font-size:1.4rem;'>{orig["accuracy"]*100:.2f}%</div>
</div>
<div style='background:rgba(0,0,0,0.04); padding:14px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>Recall</div>
<div style='font-family:Sora; font-weight:700; font-size:1.4rem;'>{orig["recall"]*100:.2f}%</div>
</div>
<div style='background:rgba(0,0,0,0.04); padding:14px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>F1-Score</div>
<div style='font-family:Sora; font-weight:700; font-size:1.4rem;'>{orig["f1"]*100:.2f}%</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
<div style='display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; padding:20px 0; text-align:center;'>
<div style='font-size:2.5rem; margin-bottom:8px;'>→</div>
<div style='font-size:0.75rem; color:var(--text-muted); margin-bottom:6px;'>Perubahan</div>
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; color:var(--primary);'>
Acc: <span style='color:{"var(--primary)" if delta["accuracy"]>=0 else "#E74C3C"};'>
{f"+{delta["accuracy"]*100:.2f}%" if delta["accuracy"]>=0 else f"{delta["accuracy"]*100:.2f}%"}
</span>
</div>
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; color:var(--primary); margin-top:6px;'>
Rec: <span style='color:{"var(--primary)" if delta["recall"]>=0 else "#E74C3C"};'>
{f"+{delta["recall"]*100:.2f}%" if delta["recall"]>=0 else f"{delta["recall"]*100:.2f}%"}
</span>
</div>
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; color:var(--primary); margin-top:6px;'>
F1: <span style='color:{"var(--primary)" if delta["f1"]>=0 else "#E74C3C"};'>
{f"+{delta["f1"]*100:.2f}%" if delta["f1"]>=0 else f"{delta["f1"]*100:.2f}%"}
</span>
</div>
</div>
""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
<div class='card' style='border-left:4px solid {aug["color"]};'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:16px; color:{aug["color"]};'>
✅ {aug["label"]}
</div>
<div style='font-size:0.75rem; color:var(--text-muted); margin-bottom:12px;'>Total Data: {aug["total_data"]:,} | Imbalance: 2.40:1</div>
<div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; text-align:center;'>
<div style='background:rgba(27,94,32,0.06); padding:14px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>Accuracy</div>
<div style='font-family:Sora; font-weight:700; font-size:1.4rem;'>{aug["accuracy"]*100:.2f}%</div>
</div>
<div style='background:rgba(27,94,32,0.06); padding:14px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>Recall</div>
<div style='font-family:Sora; font-weight:700; font-size:1.4rem; color:var(--primary);'>{aug["recall"]*100:.2f}%</div>
</div>
<div style='background:rgba(27,94,32,0.06); padding:14px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>F1-Score</div>
<div style='font-family:Sora; font-weight:700; font-size:1.4rem;'>{aug["f1"]*100:.2f}%</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Grouped Bar Chart ────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📊 Perbandingan Metrik: Original vs Augmented</div>
</div>
""", unsafe_allow_html=True)

    metrics = ["Accuracy", "Recall", "F1-Score"]
    orig_vals = [orig["accuracy"] * 100, orig["recall"] * 100, orig["f1"] * 100]
    aug_vals = [aug["accuracy"] * 100, aug["recall"] * 100, aug["f1"] * 100]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=f"Original ({orig['total_data']:,} data)",
        x=metrics,
        y=orig_vals,
        marker_color=orig["color"],
        text=[f"{v:.2f}%" for v in orig_vals],
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name=f"Augmented ({aug['total_data']:,} data)",
        x=metrics,
        y=aug_vals,
        marker_color=aug["color"],
        text=[f"{v:.2f}%" for v in aug_vals],
        textposition="outside",
    ))
    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(range=[92, 102], title="Nilai (%)"),
        font=dict(family="Inter", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        height=430,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Delta Summary Cards ──────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📐 Delta Peningkatan</div>
</div>
""", unsafe_allow_html=True)

    dc1, dc2, dc3 = st.columns(3)
    for col, metric, val in [
        (dc1, "Accuracy", delta["accuracy"]),
        (dc2, "Recall", delta["recall"]),
        (dc3, "F1-Score", delta["f1"]),
    ]:
        sign = "+" if val >= 0 else ""
        color = "var(--primary)" if val >= 0 else "#E74C3C"
        with col:
            st.markdown(f"""
<div class='card' style='text-align:center;'>
<div style='font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;'>Δ {metric}</div>
<div style='font-family:Sora; font-weight:800; font-size:2rem; color:{color};'>{sign}{val*100:.2f}%</div>
<div style='font-size:0.78rem; color:var(--text-secondary); margin-top:4px;'>
Augmented vs Original
</div>
</div>
""", unsafe_allow_html=True)

    # ── Insights ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
<div class='insight-card'>
🤖 <b>DistilBERT Fine-Tuning</b> berhasil meningkatkan semua metrik setelah augmentasi.
Recall meningkat dari <b>{orig['recall']*100:.2f}%</b> menjadi <b>{aug['recall']*100:.2f}%</b>
(+{delta['recall']*100:.2f}%), menunjukkan bahwa model Transformer pun mendapat manfaat dari 
distribusi data yang lebih seimbang meskipun model ini sudah dilengkapi dengan mekanisme 
<i>attention</i> yang mampu memahami konteks kalimat secara mendalam.
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class='insight-card'>
⚡ <b>Kesimpulan:</b> DistilBERT augmented (Acc: {aug['accuracy']*100:.2f}%, Recall: {aug['recall']*100:.2f}%) 
masih tertinggal dari NB + TF-IDF augmented (Acc: 99.20%, Recall: 97.78%) yang lebih sederhana.
Ini membuktikan bahwa untuk dataset teks pendek yang sudah memiliki pola kata yang jelas (agricultural terms), 
model probabilistik klasik dapat bersaing bahkan mengalahkan Transformer besar.
</div>
""", unsafe_allow_html=True)
