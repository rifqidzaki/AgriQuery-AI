# ════════════════════════════════════════════════════════════════
# PAGE 06 — MODEL COMPARISON
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
from components.metrics import render_metric_grid, render_section_header
from components.charts import (plotly_grouped_bar, plotly_radar, plotly_ranking_bar,
                                plotly_heatmap, plotly_bar, EMERALD_PALETTE)
from backend.model_training import COLORS
import plotly.graph_objects as go


def render(ss):
    """Render the Model Comparison page."""
    results = ss.get("results", {})
    best_name = ss.get("best_name", "")

    if not results:
        st.warning("Model belum dilatih.")
        return

    render_section_header(
        "Model Comparison",
        "Comprehensive Comparison",
        "Perbandingan lengkap performa semua model dan representasi fitur.",
        extra_badges=[{"text": f"🏆 Best: {best_name}", "type": "gold"}]
    )

    # ── Top 3 Best Models ──
    sorted_models = sorted(results.items(), key=lambda x: x[1]["accuracy"], reverse=True)
    top3 = sorted_models[:3]
    medals = ["🥇", "🥈", "🥉"]

    render_metric_grid([
        {"icon": medals[i], "label": f"Rank #{i+1}", "value": f"{r['accuracy']*100:.2f}", "unit": "%", "sub_green": name}
        for i, (name, r) in enumerate(top3)
    ])

    # ── Tab Views ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overall Ranking",
        "🌳 DT vs NB",
        "📝 Classical vs Modern",
        "🔥 Performance Heatmap"
    ])

    # ── TAB 1: Overall Ranking ──
    with tab1:
        all_names = [name for name, _ in sorted_models]
        all_accs = [r["accuracy"] * 100 for _, r in sorted_models]

        fig = plotly_ranking_bar(all_names, all_accs, "Ranking Akurasi — Semua Kombinasi Model")
        st.plotly_chart(fig, use_container_width=True)

        # Summary table
        st.markdown("**📋 Detailed Ranking Table**")
        rank_rows = []
        for i, (name, r) in enumerate(sorted_models):
            rank_rows.append({
                "Rank": f"#{i+1}",
                "Model": name,
                "Accuracy (%)": f"{r['accuracy']*100:.2f}",
                "Precision (%)": f"{r['precision']*100:.2f}",
                "Recall (%)": f"{r['recall']*100:.2f}",
                "F1 (%)": f"{r['f1_score']*100:.2f}",
                "Time (s)": f"{r['train_time']:.4f}",
                "Type": "Classical" if any(c in name for c in ["BoW", "TF-IDF", "N-Gram"]) else "Modern"
            })
        st.dataframe(pd.DataFrame(rank_rows), use_container_width=True, hide_index=True)

    # ── TAB 2: DT vs NB ──
    with tab2:
        dt_models = {k: v for k, v in results.items() if k.startswith("DT")}
        nb_models = {k: v for k, v in results.items() if k.startswith("NB")}

        metric_labels = ["Accuracy", "Precision", "Recall", "F1 Score"]
        metrics_keys = ["accuracy", "precision", "recall", "f1_score"]

        # Get feature names common to both
        dt_features = [k.split(" + ")[1] for k in dt_models.keys()]
        nb_features = [k.split(" + ")[1] for k in nb_models.keys()]
        common_features = [f for f in dt_features if f in nb_features]

        if common_features:
            # Grouped comparison per feature
            series_dt = {}
            series_nb = {}
            for feat in common_features:
                dt_key = f"DT + {feat}"
                nb_key = f"NB + {feat}"
                if dt_key in results and nb_key in results:
                    series_dt[feat] = results[dt_key]["accuracy"] * 100
                    series_nb[feat] = results[nb_key]["accuracy"] * 100

            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Decision Tree", x=list(series_dt.keys()), y=list(series_dt.values()),
                marker_color="#0E4B2E", text=[f"{v:.2f}%" for v in series_dt.values()], textposition="outside"
            ))
            fig.add_trace(go.Bar(
                name="Naive Bayes", x=list(series_nb.keys()), y=list(series_nb.values()),
                marker_color="#5FAE6E", text=[f"{v:.2f}%" for v in series_nb.values()], textposition="outside"
            ))
            fig.update_layout(
                barmode="group",
                title=dict(text="Decision Tree vs Naive Bayes — Accuracy per Feature",
                           font=dict(family="Sora", size=15, color="#123524")),
                yaxis=dict(range=[0, 115], title="Accuracy (%)", gridcolor="rgba(31,122,77,0.05)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#4A5568"),
                margin=dict(t=50, b=30, l=30, r=30),
            )
            st.plotly_chart(fig, use_container_width=True)

        # Radar comparison
        col1, col2 = st.columns(2)
        with col1:
            if dt_models:
                radar_data = {}
                for name, r in dt_models.items():
                    radar_data[name] = [r[m]*100 for m in metrics_keys]
                fig_radar = plotly_radar(radar_data, metric_labels, "Radar — Decision Tree Models")
                st.plotly_chart(fig_radar, use_container_width=True)

        with col2:
            if nb_models:
                radar_data = {}
                for name, r in nb_models.items():
                    radar_data[name] = [r[m]*100 for m in metrics_keys]
                fig_radar = plotly_radar(radar_data, metric_labels, "Radar — Naive Bayes Models")
                st.plotly_chart(fig_radar, use_container_width=True)

    # ── TAB 3: Classical vs Modern ──
    with tab3:
        classical_names = [k for k in results.keys() if any(c in k for c in ["BoW", "TF-IDF", "N-Gram"])]
        modern_names = [k for k in results.keys() if any(c in k for c in ["Word2Vec", "GloVe", "BERT"])]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📝 Classical NLP")
            if classical_names:
                best_classical = max(classical_names, key=lambda x: results[x]["accuracy"])
                render_metric_grid([
                    {"icon": "🏆", "label": "Best Classical", "value": f"{results[best_classical]['accuracy']*100:.2f}",
                     "unit": "%", "sub_green": best_classical},
                    {"icon": "📊", "label": "Avg Accuracy", "value": f"{np.mean([results[n]['accuracy']*100 for n in classical_names]):.2f}", "unit": "%"},
                ])

                for name in sorted(classical_names, key=lambda x: results[x]["accuracy"], reverse=True):
                    r = results[name]
                    st.markdown(f"""
                    <div class='explain-card' style='padding:16px 20px;'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div style='font-weight:600;'>{name}</div>
                            <div style='font-family:Sora; font-weight:700; color:var(--accent-emerald);'>{r['accuracy']*100:.2f}%</div>
                        </div>
                        <div class='confidence-bar-bg' style='margin-top:8px;'>
                            <div class='confidence-bar-fill' style='width:{r["accuracy"]*100}%;'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🧠 Modern NLP")
            if modern_names:
                best_modern = max(modern_names, key=lambda x: results[x]["accuracy"])
                render_metric_grid([
                    {"icon": "🏆", "label": "Best Modern", "value": f"{results[best_modern]['accuracy']*100:.2f}",
                     "unit": "%", "sub_green": best_modern},
                    {"icon": "📊", "label": "Avg Accuracy", "value": f"{np.mean([results[n]['accuracy']*100 for n in modern_names]):.2f}", "unit": "%"},
                ])

                for name in sorted(modern_names, key=lambda x: results[x]["accuracy"], reverse=True):
                    r = results[name]
                    st.markdown(f"""
                    <div class='explain-card' style='padding:16px 20px;'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div style='font-weight:600;'>{name}</div>
                            <div style='font-family:Sora; font-weight:700; color:var(--accent-emerald);'>{r['accuracy']*100:.2f}%</div>
                        </div>
                        <div class='confidence-bar-bg' style='margin-top:8px;'>
                            <div class='confidence-bar-fill' style='width:{r["accuracy"]*100}%;'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Overall winner
        if classical_names and modern_names:
            best_c_acc = results[best_classical]["accuracy"] * 100
            best_m_acc = results[best_modern]["accuracy"] * 100
            winner = "Classical NLP" if best_c_acc > best_m_acc else "Modern NLP"
            winner_model = best_classical if best_c_acc > best_m_acc else best_modern

            st.markdown(f"""
            <div class='glass-card' style='text-align:center; padding:28px;'>
                <div style='font-size:2rem; margin-bottom:8px;'>🏆</div>
                <div style='font-family:Sora; font-weight:800; font-size:1.3rem; color:var(--accent-emerald);'>
                    {winner} Wins!
                </div>
                <div style='font-size:0.9rem; color:var(--text-muted); margin-top:8px;'>
                    Best Model: <strong>{winner_model}</strong> ({max(best_c_acc, best_m_acc):.2f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 4: Performance Heatmap ──
    with tab4:
        features_list = ["BoW", "TF-IDF", "N-Gram", "Word2Vec", "GloVe", "BERT"]
        models_list = ["DT", "NB"]

        heatmap_data = []
        actual_features = []
        for feat in features_list:
            row = []
            has_data = False
            for model in models_list:
                key = f"{model} + {feat}"
                if key in results:
                    row.append(results[key]["accuracy"] * 100)
                    has_data = True
                else:
                    row.append(0)
            if has_data:
                heatmap_data.append(row)
                actual_features.append(feat)

        if heatmap_data:
            fig = plotly_heatmap(
                np.array(heatmap_data),
                ["Decision Tree", "Naive Bayes"],
                actual_features,
                "Performance Heatmap — Accuracy (%)"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Training time comparison
        st.markdown("**⏱️ Training Time Comparison**")
        time_names = list(results.keys())
        time_vals = [results[n]["train_time"] for n in time_names]

        fig_time = go.Figure(go.Bar(
            x=time_names, y=time_vals,
            marker_color=[COLORS.get(n, "#5FAE6E") for n in time_names],
            text=[f"{t:.4f}s" for t in time_vals],
            textposition="outside"
        ))
        fig_time.update_layout(
            title=dict(text="Training Time (seconds)", font=dict(family="Sora", size=15, color="#123524")),
            yaxis=dict(title="Seconds", gridcolor="rgba(31,122,77,0.05)"),
            xaxis=dict(tickangle=45),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#4A5568"),
            margin=dict(t=50, b=80, l=30, r=30),
        )
        st.plotly_chart(fig_time, use_container_width=True)
