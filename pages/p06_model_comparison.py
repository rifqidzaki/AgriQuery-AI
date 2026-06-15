# ════════════════════════════════════════════════════════════════
# PAGE 06 — MODEL COMPARISON (v7.0) — Original vs Augmented
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backend.research_data import SCENARIO_RESULTS


def render(ss):
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📊 Model Comparison</div>
<div class='section-subtitle'>Perbandingan komprehensif 15 skenario model — Dataset Original vs Augmented</div>
</div>
""", unsafe_allow_html=True)

    # ── Filters ──────────────────────────────────────────────────
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        dataset_filter = st.selectbox("📁 Dataset", ["Augmented", "Original", "Both (Perbandingan)"])
    with col_f2:
        metric_filter = st.selectbox("📐 Metric", ["Recall", "Accuracy", "F1-Score"])

    metric_key_map = {
        "Recall": ("orig_recall", "aug_recall"),
        "Accuracy": ("orig_acc", "aug_acc"),
        "F1-Score": ("orig_f1", "aug_f1"),
    }
    orig_key, aug_key = metric_key_map[metric_filter]

    # ── Comparison Table ─────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📋 Tabel Perbandingan 15 Skenario</div>
</div>
""", unsafe_allow_html=True)

    sorted_by = aug_key if dataset_filter != "Original" else orig_key
    sorted_results = sorted(SCENARIO_RESULTS, key=lambda x: x[sorted_by], reverse=True)

    table_data = []
    for rank, r in enumerate(sorted_results, 1):
        delta = (r[aug_key] - r[orig_key]) * 100
        delta_str = f"+{delta:.2f}%" if delta >= 0 else f"{delta:.2f}%"
        row = {
            "Rank": rank,
            "Model": r["name"],
            "Kelompok": r["group"],
            f"{metric_filter} (Original)": f"{r[orig_key]*100:.2f}%",
            f"{metric_filter} (Augmented)": f"{r[aug_key]*100:.2f}%",
            f"Δ {metric_filter}": delta_str,
        }
        table_data.append(row)

    df_comp = pd.DataFrame(table_data)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

    # ── Best Model Highlight ─────────────────────────────────────
    best = sorted_results[0]
    best_val = best[aug_key if dataset_filter != "Original" else orig_key] * 100
    dataset_label = "Augmented" if dataset_filter != "Original" else "Original"
    st.markdown(f"""
<div class='card-static' style='padding:18px 22px; border-left:4px solid var(--accent); margin-bottom:20px;'>
<div style='display:flex; align-items:center; gap:12px;'>
<span style='font-size:1.5rem;'>🏆</span>
<div>
<div style='font-family:Sora; font-weight:700; font-size:1rem;'>
Model Terbaik ({metric_filter} Tertinggi — {dataset_label}): {best['name']}
</div>
<div style='font-size:0.85rem; color:var(--text-muted);'>
{metric_filter}: {best_val:.2f}% | Kelompok: {best['group']}
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Chart ────────────────────────────────────────────────────
    names = [r["name"] for r in sorted_results]

    if dataset_filter == "Both (Perbandingan)":
        fig = go.Figure()
        orig_vals = [r[orig_key] * 100 for r in sorted_results]
        aug_vals = [r[aug_key] * 100 for r in sorted_results]
        fig.add_trace(go.Bar(
            name="Original", x=names, y=orig_vals,
            marker_color="#E74C3C",
            text=[f"{v:.2f}%" for v in orig_vals], textposition="outside",
        ))
        fig.add_trace(go.Bar(
            name="Augmented", x=names, y=aug_vals,
            marker_color="#1B5E20",
            text=[f"{v:.2f}%" for v in aug_vals], textposition="outside",
        ))
        fig.update_layout(barmode="group")
        title = f"{metric_filter} — Original vs Augmented"
    elif dataset_filter == "Augmented":
        aug_vals = [r[aug_key] * 100 for r in sorted_results]
        fig = go.Figure(go.Bar(
            x=names, y=aug_vals, marker_color="#1B5E20",
            text=[f"{v:.2f}%" for v in aug_vals], textposition="outside",
        ))
        title = f"{metric_filter} — Augmented Dataset"
    else:
        orig_vals = [r[orig_key] * 100 for r in sorted_results]
        fig = go.Figure(go.Bar(
            x=names, y=orig_vals, marker_color="#E74C3C",
            text=[f"{v:.2f}%" for v in orig_vals], textposition="outside",
        ))
        title = f"{metric_filter} — Original Dataset"

    fig.update_layout(
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickangle=-35),
        yaxis=dict(title=f"{metric_filter} (%)", range=[40, 106]),
        font=dict(family="Inter", size=11),
        legend=dict(orientation="h", yanchor="bottom", y=-0.4),
        height=480,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Group Summary ────────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📈 Rata-Rata per Kelompok (Augmented)</div>
</div>
""", unsafe_allow_html=True)

    groups = {}
    for r in SCENARIO_RESULTS:
        g = r["group"]
        if g not in groups:
            groups[g] = []
        groups[g].append(r)

    group_cols = st.columns(len(groups))
    for col, (gname, items) in zip(group_cols, groups.items()):
        avg_aug_recall = sum(r["aug_recall"] for r in items) / len(items) * 100
        avg_aug_acc = sum(r["aug_acc"] for r in items) / len(items) * 100
        with col:
            st.markdown(f"""
<div class='card' style='text-align:center;'>
<div style='font-family:Sora; font-weight:700; font-size:0.8rem; margin-bottom:12px; line-height:1.3;'>{gname}</div>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>Avg Accuracy</div>
<div style='font-weight:700; font-size:1.1rem; margin-bottom:6px;'>{avg_aug_acc:.2f}%</div>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase;'>Avg Recall</div>
<div style='font-weight:700; font-size:1.1rem; color:var(--primary);'>{avg_aug_recall:.2f}%</div>
<div style='font-size:0.7rem; color:var(--text-muted); margin-top:8px;'>{len(items)} model</div>
</div>
""", unsafe_allow_html=True)
