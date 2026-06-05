# ════════════════════════════════════════════════════════════════
# PAGE 05 — MODEL TRAINING
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
from components.metrics import render_metric_grid, render_section_header
from components.charts import plotly_bar, plotly_cm, plotly_grouped_bar, EMERALD_PALETTE
from backend.model_training import SCENARIO_NAMES, CLASSICAL_SCENARIOS, MODERN_SCENARIOS, COLORS


def render(ss):
    """Render the Model Training page."""
    results = ss.get("results", {})
    le = ss.get("le")
    best_name = ss.get("best_name", "")

    if not results:
        st.warning("Model belum dilatih.")
        return

    render_section_header(
        "Model Performance",
        "Model Training Results",
        "Evaluasi performa Decision Tree dan Naive Bayes pada setiap representasi fitur.",
        extra_badges=[{"text": f"Best: {best_name}", "type": "gold"}]
    )

    # ── Tabs: Decision Tree / Naive Bayes ──
    tab_dt, tab_nb = st.tabs(["🌳 Decision Tree", "📊 Naive Bayes"])

    for tab, model_prefix in [(tab_dt, "DT"), (tab_nb, "NB")]:
        with tab:
            model_scenarios = [s for s in results.keys() if s.startswith(model_prefix)]

            if not model_scenarios:
                st.info(f"Tidak ada model {model_prefix} yang tersedia.")
                continue

            model_name = "Decision Tree" if model_prefix == "DT" else "Naive Bayes"

            # ── Model Parameters Card ──
            if model_prefix == "DT":
                st.markdown(f"""
                <div class='glass-card' style='padding:20px 28px;'>
                    <div style='font-family:Sora; font-weight:700; margin-bottom:10px;'>⚙️ {model_name} Parameters</div>
                    <div style='display:flex; gap:24px; flex-wrap:wrap; font-size:0.88rem;'>
                        <div><strong>Criterion:</strong> Gini</div>
                        <div><strong>Max Depth:</strong> 20</div>
                        <div><strong>Min Samples Split:</strong> 5</div>
                        <div><strong>Min Samples Leaf:</strong> 2</div>
                        <div><strong>Random State:</strong> 42</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='glass-card' style='padding:20px 28px;'>
                    <div style='font-family:Sora; font-weight:700; margin-bottom:10px;'>⚙️ {model_name} Parameters</div>
                    <div style='display:flex; gap:24px; flex-wrap:wrap; font-size:0.88rem;'>
                        <div><strong>Classical (BoW/TF-IDF/N-Gram):</strong> MultinomialNB (α=1.0)</div>
                        <div><strong>Modern (Word2Vec/GloVe/BERT):</strong> GaussianNB</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── Sub-tabs for each feature ──
            feature_tabs = st.tabs([f"📌 {s.split(' + ')[1]}" for s in model_scenarios])

            for ftab, sc_name in zip(feature_tabs, model_scenarios):
                with ftab:
                    r = results[sc_name]
                    color = COLORS.get(sc_name, "#1F7A4D")
                    is_best = (sc_name == best_name)

                    if is_best:
                        st.markdown("<div class='ai-badge-gold'>🏆 Best Overall Model</div>", unsafe_allow_html=True)

                    # Metric cards
                    metrics_list = ["accuracy", "precision", "recall", "f1_score"]
                    metric_labels = ["Accuracy", "Precision", "Recall", "F1 Score"]
                    metric_icons = ["🎯", "🔍", "📡", "⚡"]

                    render_metric_grid([
                        {"icon": icon, "label": lbl, "value": f"{r[m]*100:.2f}", "unit": "%"}
                        for icon, lbl, m in zip(metric_icons, metric_labels, metrics_list)
                    ])

                    col1, col2 = st.columns(2)

                    with col1:
                        vals = [r[m] for m in metrics_list]
                        fig = plotly_bar(metric_labels, vals, f"Metrik Evaluasi — {sc_name}", [color]*4)
                        fig.update_layout(yaxis_range=[0, 1.15])
                        st.plotly_chart(fig, use_container_width=True)

                    with col2:
                        if le is not None:
                            fig_cm = plotly_cm(r["cm"], f"Confusion Matrix — {sc_name}", list(le.classes_))
                            st.plotly_chart(fig_cm, use_container_width=True)

                    # Model details
                    details_items = [
                        f"<div><strong>Training Time:</strong> {r['train_time']:.4f}s</div>"
                    ]
                    if model_prefix == "DT":
                        details_items.append(f"<div><strong>Tree Depth:</strong> {r.get('depth', 'N/A')}</div>")
                        details_items.append(f"<div><strong>Number of Leaves:</strong> {r.get('leaves', 'N/A')}</div>")

                    st.markdown(f"""
                    <div class='glass-card' style='padding:20px 28px;'>
                        <div style='font-family:Sora; font-weight:700; margin-bottom:10px;'>📋 Model Details — {sc_name}</div>
                        <div style='display:flex; gap:32px; flex-wrap:wrap; font-size:0.88rem; color:var(--text-secondary);'>
                            {"".join(details_items)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── Overall Summary Table ──
    st.markdown("---")
    render_section_header("Summary", "Training Summary", "Ringkasan performa semua kombinasi model.")

    summary_rows = []
    for sc_name in sorted(results.keys(), key=lambda x: results[x]["accuracy"], reverse=True):
        r = results[sc_name]
        is_best = sc_name == best_name
        summary_rows.append({
            "Rank": "",
            "Model": ("🏆 " if is_best else "") + sc_name,
            "Accuracy (%)": f"{r['accuracy']*100:.2f}",
            "Precision (%)": f"{r['precision']*100:.2f}",
            "Recall (%)": f"{r['recall']*100:.2f}",
            "F1 Score (%)": f"{r['f1_score']*100:.2f}",
            "Train Time (s)": f"{r['train_time']:.4f}",
        })

    for i, row in enumerate(summary_rows):
        row["Rank"] = f"#{i+1}"

    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)
