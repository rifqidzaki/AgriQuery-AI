# ════════════════════════════════════════════════════════════════
# PAGE: BALANCING ANALYSIS
# ════════════════════════════════════════════════════════════════

import streamlit as st
import plotly.graph_objects as go
from backend.research_data import BALANCING_RESULTS


def render(ss):
    st.markdown("""
<div class='section-header'>
<div class='section-title'>⚖️ Balancing Analysis</div>
<div class='section-subtitle'>Perbandingan dampak teknik class balancing terhadap Accuracy, Recall, dan F1-Score</div>
</div>
""", unsafe_allow_html=True)

    # ── Info Banner ──────────────────────────────────────────────
    st.markdown("""
<div class='insight-card' style='margin-bottom:24px;'>
📌 <b>Konteks:</b> Teknik class balancing diterapkan pada <b>NB + TF-IDF dengan dataset Augmented</b> 
— model terbaik berdasarkan hasil keseluruhan eksperimen. Tujuannya adalah menganalisis apakah 
teknik balancing tambahan setelah augmentasi dapat lebih meningkatkan performa pada kelas minoritas (HORTICULTURE).
</div>
""", unsafe_allow_html=True)

    # ── Method Cards ─────────────────────────────────────────────
    cols = st.columns(3)
    for col, method in zip(cols, BALANCING_RESULTS):
        is_best = method["method"].startswith("Random")
        border_color = "var(--primary)" if is_best else method["color"]
        badge = "<span style='background:var(--primary); color:white; font-size:0.65rem; padding:2px 8px; border-radius:20px; margin-left:6px;'>BEST RECALL</span>" if is_best else ""

        with col:
            st.markdown(f"""
<div class='card' style='border-left:4px solid {border_color};'>
<div style='font-family:Sora; font-weight:700; font-size:0.95rem; margin-bottom:4px;'>
{method['icon']} {method['method']}{badge}
</div>
<div style='font-size:0.78rem; color:var(--text-muted); margin-bottom:16px; line-height:1.5;'>{method['desc']}</div>
<div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; text-align:center;'>
<div style='background:rgba(0,0,0,0.03); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>Accuracy</div>
<div style='font-family:Sora; font-weight:700; font-size:1.1rem;'>{method['accuracy']*100:.2f}%</div>
</div>
<div style='background:rgba(0,0,0,0.03); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>Recall</div>
<div style='font-family:Sora; font-weight:700; font-size:1.1rem; color:{border_color};'>{method['recall']*100:.2f}%</div>
</div>
<div style='background:rgba(0,0,0,0.03); padding:10px; border-radius:8px;'>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>F1-Score</div>
<div style='font-family:Sora; font-weight:700; font-size:1.1rem;'>{method['f1']*100:.2f}%</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Comparison Table ─────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📋 Tabel Perbandingan</div>
</div>
""", unsafe_allow_html=True)

    import pandas as pd
    table_data = []
    for m in BALANCING_RESULTS:
        table_data.append({
            "Metode": m["method"],
            "Accuracy (%)": f"{m['accuracy']*100:.2f}",
            "Recall (%)": f"{m['recall']*100:.2f}",
            "F1-Score (%)": f"{m['f1']*100:.2f}",
        })
    df_bal = pd.DataFrame(table_data)
    st.dataframe(df_bal, use_container_width=True, hide_index=True)

    # ── Grouped Bar Chart ────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📊 Visualisasi Perbandingan Metrik</div>
</div>
""", unsafe_allow_html=True)

    methods = [m["method"].split(" (")[0].split(" +")[0] for m in BALANCING_RESULTS]
    accs = [m["accuracy"] * 100 for m in BALANCING_RESULTS]
    recs = [m["recall"] * 100 for m in BALANCING_RESULTS]
    f1s = [m["f1"] * 100 for m in BALANCING_RESULTS]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Accuracy (%)", x=methods, y=accs,
                         marker_color="#2E7D32",
                         text=[f"{v:.2f}%" for v in accs], textposition="outside"))
    fig.add_trace(go.Bar(name="Recall (%)", x=methods, y=recs,
                         marker_color="#1565C0",
                         text=[f"{v:.2f}%" for v in recs], textposition="outside"))
    fig.add_trace(go.Bar(name="F1-Score (%)", x=methods, y=f1s,
                         marker_color="#6A1B9A",
                         text=[f"{v:.2f}%" for v in f1s], textposition="outside"))
    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(range=[85, 102], title="Nilai (%)"),
        font=dict(family="Inter", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Auto Insight ─────────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>💡 Insight Otomatis</div>
</div>
""", unsafe_allow_html=True)

    best_recall = max(BALANCING_RESULTS, key=lambda x: x["recall"])
    best_acc = max(BALANCING_RESULTS, key=lambda x: x["accuracy"])

    st.markdown(f"""
<div class='insight-card'>
🏆 <b>RandomOverSampler memberikan recall tertinggi ({best_recall['recall']*100:.2f}%)</b>, melampaui 
No Balancing ({BALANCING_RESULTS[0]['recall']*100:.2f}%) dan SMOTE ({BALANCING_RESULTS[2]['recall']*100:.2f}%). 
Peningkatan recall yang signifikan ini terjadi karena ROS menduplikasi sampel HORTICULTURE sehingga 
model mendapatkan lebih banyak "latihan" mengenali pola kelas minoritas.
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class='insight-card'>
⚠️ <b>Trade-off Accuracy vs Recall:</b> Teknik balancing (ROS & SMOTE) sedikit menurunkan akurasi keseluruhan 
karena model menjadi kurang "bias" ke kelas mayoritas. Namun dalam konteks penelitian ini, 
<b>recall yang tinggi lebih penting</b> — model harus bisa mengenali semua query HORTICULTURE 
meskipun sedikit lebih sering salah mengklasifikasi Agriculture.
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class='insight-card'>
🔬 <b>SMOTE vs ROS:</b> Walaupun SMOTE menggunakan interpolasi fitur yang lebih canggih 
(synthetic sampling), pada dataset teks ini ROS terbukti sedikit lebih efektif 
(Recall {BALANCING_RESULTS[1]['recall']*100:.2f}% vs {BALANCING_RESULTS[2]['recall']*100:.2f}%). 
Hal ini kemungkinan disebabkan oleh sifat representasi fitur TF-IDF yang sparse, 
sehingga interpolasi linier SMOTE tidak menghasilkan sampel sintetis yang representatif.
</div>
""", unsafe_allow_html=True)
