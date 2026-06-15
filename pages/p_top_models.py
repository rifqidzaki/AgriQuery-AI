# ════════════════════════════════════════════════════════════════
# PAGE: TOP PERFORMING MODELS — Leaderboard Style
# ════════════════════════════════════════════════════════════════

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from backend.research_data import TOP_MODELS, SCENARIO_RESULTS


def render(ss):
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🏆 Top Performing Models</div>
<div class='section-subtitle'>Model terbaik berdasarkan hasil seluruh 30 eksperimen (15 skenario × Original + Augmented)</div>
</div>
""", unsafe_allow_html=True)

    # ── Leaderboard Podium ───────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🎖️ Podium Terbaik</div>
</div>
""", unsafe_allow_html=True)

    top = TOP_MODELS
    c1, c2, c3, c4 = st.columns(4)

    def metric_card(col, data, label, metric_key, metric_label):
        val = data[metric_key] * 100
        with col:
            st.markdown(f"""
<div class='card' style='text-align:center; border-top:4px solid var(--primary);'>
<div style='font-size:2.5rem; margin-bottom:6px;'>{data['icon']}</div>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px;'>{label}</div>
<div style='font-family:Sora; font-weight:800; font-size:1.1rem; color:var(--primary); margin-bottom:12px;'>{data['name']}</div>
<div style='font-size:0.7rem; color:var(--text-muted); margin-bottom:2px;'>Dataset</div>
<div style='font-size:0.8rem; font-weight:600; margin-bottom:14px;'>{data['dataset']}</div>
<div style='background:var(--primary); color:white; border-radius:8px; padding:10px;'>
<div style='font-size:0.65rem; text-transform:uppercase; margin-bottom:4px; opacity:0.8;'>{metric_label}</div>
<div style='font-family:Sora; font-weight:800; font-size:1.8rem;'>{val:.2f}%</div>
</div>
<div style='display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:10px;'>
<div style='background:rgba(27,94,32,0.06); padding:8px; border-radius:6px;'>
<div style='font-size:0.6rem; color:var(--text-muted);'>Accuracy</div>
<div style='font-weight:700; font-size:0.85rem;'>{data['accuracy']*100:.2f}%</div>
</div>
<div style='background:rgba(27,94,32,0.06); padding:8px; border-radius:6px;'>
<div style='font-size:0.6rem; color:var(--text-muted);'>Recall</div>
<div style='font-weight:700; font-size:0.85rem;'>{data['recall']*100:.2f}%</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    metric_card(c1, top["best_accuracy"], "BEST ACCURACY", "accuracy", "Accuracy")
    metric_card(c2, top["best_recall"], "BEST RECALL", "recall", "Recall")
    metric_card(c3, top["best_f1"], "BEST F1-SCORE", "f1", "F1-Score")
    metric_card(c4, top["best_transformer"], "BEST TRANSFORMER", "accuracy", "Accuracy")

    # ── Full Leaderboard Table ───────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📋 Leaderboard Augmented Dataset</div>
<div class='section-subtitle'>Ranking berdasarkan recall tertinggi pada dataset augmented</div>
</div>
""", unsafe_allow_html=True)

    sorted_results = sorted(SCENARIO_RESULTS, key=lambda x: x["aug_recall"], reverse=True)
    table_data = []
    for rank, r in enumerate(sorted_results, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else str(rank)
        table_data.append({
            "Rank": medal,
            "Model": r["name"],
            "Kelompok": r["group"],
            "Acc (Orig)": f"{r['orig_acc']*100:.2f}%",
            "Recall (Orig)": f"{r['orig_recall']*100:.2f}%",
            "F1 (Orig)": f"{r['orig_f1']*100:.2f}%",
            "Acc (Aug)": f"{r['aug_acc']*100:.2f}%",
            "Recall (Aug)": f"{r['aug_recall']*100:.2f}%",
            "F1 (Aug)": f"{r['aug_f1']*100:.2f}%",
        })

    df_lb = pd.DataFrame(table_data)
    st.dataframe(df_lb, use_container_width=True, hide_index=True)

    # ── Group Comparison Bar ─────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📊 Perbandingan Augmented Recall per Model</div>
</div>
""", unsafe_allow_html=True)

    names = [r["name"] for r in sorted_results]
    aug_recalls = [r["aug_recall"] * 100 for r in sorted_results]
    colors = []
    for r in sorted_results:
        if r["group"] == "Classical NLP":
            colors.append("#2E7D32")
        elif r["group"] == "Non-Contextual Embedding":
            colors.append("#1565C0")
        elif r["group"] == "Contextual Embedding":
            colors.append("#6A1B9A")
        else:
            colors.append("#E65100")

    fig = go.Figure(go.Bar(
        x=aug_recalls,
        y=names,
        orientation="h",
        marker_color=colors,
        text=[f"{v:.2f}%" for v in aug_recalls],
        textposition="outside",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Recall (%)", range=[40, 105]),
        yaxis=dict(autorange="reversed"),
        font=dict(family="Inter", size=11),
        height=520,
        margin=dict(l=180, r=60, t=20, b=60),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Legend ───────────────────────────────────────────────────
    st.markdown("""
<div style='display:flex; gap:16px; flex-wrap:wrap; justify-content:center; padding:12px;'>
<span style='display:flex; align-items:center; gap:6px; font-size:0.8rem;'>
<span style='width:14px; height:14px; background:#2E7D32; border-radius:3px; display:inline-block;'></span>Classical NLP
</span>
<span style='display:flex; align-items:center; gap:6px; font-size:0.8rem;'>
<span style='width:14px; height:14px; background:#1565C0; border-radius:3px; display:inline-block;'></span>Non-Contextual Embedding
</span>
<span style='display:flex; align-items:center; gap:6px; font-size:0.8rem;'>
<span style='width:14px; height:14px; background:#6A1B9A; border-radius:3px; display:inline-block;'></span>Contextual Embedding
</span>
<span style='display:flex; align-items:center; gap:6px; font-size:0.8rem;'>
<span style='width:14px; height:14px; background:#E65100; border-radius:3px; display:inline-block;'></span>Transformer
</span>
</div>
""", unsafe_allow_html=True)
