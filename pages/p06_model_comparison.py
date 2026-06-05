# ════════════════════════════════════════════════════════════════
# PAGE 06 — MODEL COMPARISON
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
from components.charts import plotly_ranking_bar, plotly_grouped_bar, plotly_radar


def render(ss):
    results = ss.get("results", {})
    best_name = ss.get("best_name", "")

    st.markdown("""
<div class='section-header'>
<div class='section-title'>📊 Model Comparison</div>
<div class='section-subtitle'>Perbandingan komprehensif seluruh 13 model yang dievaluasi</div>
</div>
""", unsafe_allow_html=True)

    if not results:
        st.warning("Hasil evaluasi belum tersedia.")
        return

    # Build comparison table
    table_data = []
    for name, r in results.items():
        table_data.append({
            "Model": name,
            "Accuracy (%)": round(r["accuracy"] * 100, 2),
            "Precision (%)": round(r["precision"] * 100, 2),
            "Recall (%)": round(r["recall"] * 100, 2),
            "F1-Score (%)": round(r["f1_score"] * 100, 2),
            "Inference Time (s)": round(r.get("inference_time", 0), 4),
        })

    df_comp = pd.DataFrame(table_data)
    df_comp = df_comp.sort_values("Accuracy (%)", ascending=False).reset_index(drop=True)
    df_comp.index = df_comp.index + 1
    df_comp.index.name = "Rank"

    # Best model highlight
    st.markdown(f"""
<div class='card-static' style='padding:18px 22px; border-left:4px solid var(--accent);'>
<div style='display:flex; align-items:center; gap:12px;'>
<span style='font-size:1.5rem;'>🏆</span>
<div>
<div style='font-family:Sora; font-weight:700; font-size:1rem;'>Model Terbaik: {best_name}</div>
<div style='font-size:0.85rem; color:var(--text-muted);'>Accuracy: {results[best_name]["accuracy"]*100:.2f}% | F1-Score: {results[best_name]["f1_score"]*100:.2f}%</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Comparison Table
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📋 Tabel Perbandingan</div>
<div class='section-subtitle'>Ranking semua model berdasarkan akurasi (tertinggi ke terendah)</div>
</div>
""", unsafe_allow_html=True)

    st.dataframe(df_comp, use_container_width=True)

    # Charts
    names = list(results.keys())
    accs = [results[n]["accuracy"] * 100 for n in names]
    precs = [results[n]["precision"] * 100 for n in names]
    recs = [results[n]["recall"] * 100 for n in names]
    f1s = [results[n]["f1_score"] * 100 for n in names]

    # Accuracy Ranking
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🏅 Ranking Akurasi</div>
</div>
""", unsafe_allow_html=True)

    fig_rank = plotly_ranking_bar(names, accs, "Ranking Model Berdasarkan Akurasi")
    st.plotly_chart(fig_rank, use_container_width=True)

    # Grouped comparison
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📈 Perbandingan Metrik</div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_acc = plotly_ranking_bar(names, accs, "Accuracy (%)")
        st.plotly_chart(fig_acc, use_container_width=True)
    with col2:
        fig_f1 = plotly_ranking_bar(names, f1s, "F1-Score (%)")
        st.plotly_chart(fig_f1, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig_prec = plotly_ranking_bar(names, precs, "Precision (%)")
        st.plotly_chart(fig_prec, use_container_width=True)
    with col4:
        fig_rec = plotly_ranking_bar(names, recs, "Recall (%)")
        st.plotly_chart(fig_rec, use_container_width=True)

    # Radar chart — Top 5
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🕸️ Radar Chart — Top 5 Model</div>
</div>
""", unsafe_allow_html=True)

    sorted_models = sorted(results.items(), key=lambda x: x[1]["accuracy"], reverse=True)
    top5 = sorted_models[:5]
    radar_data = {}
    for name, r in top5:
        radar_data[name] = [
            r["accuracy"] * 100,
            r["precision"] * 100,
            r["recall"] * 100,
            r["f1_score"] * 100,
        ]

    fig_radar = plotly_radar(radar_data, ["Accuracy", "Precision", "Recall", "F1-Score"], "Top 5 Model — Radar Chart")
    st.plotly_chart(fig_radar, use_container_width=True)
