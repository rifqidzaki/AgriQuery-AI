# ════════════════════════════════════════════════════════════════
# PAGE 07 — ERROR ANALYSIS
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
from components.metrics import render_metric_grid, render_section_header, render_explain_card
from components.charts import plotly_bar, plotly_pie, DUAL_COLORS
from backend.explainability import get_error_analysis, get_error_distribution
import plotly.graph_objects as go


def render(ss):
    """Render the Error Analysis page."""
    results = ss.get("results", {})
    le = ss.get("le")
    df_clean = ss.get("df_clean")
    X_test = ss.get("X_test")
    y_test = ss.get("y_test")

    if not results:
        st.warning("Model belum dilatih.")
        return

    render_section_header(
        "Error Analysis",
        "Misclassification Analysis",
        "Analisis mendalam tentang kesalahan prediksi model — mengapa model gagal dan pola error.",
        extra_badges=[{"text": "Diagnostic", "type": "gold"}]
    )

    # ── Model Selection ──
    model_names = list(results.keys())
    selected_model = st.selectbox("Pilih kombinasi model untuk analisis:", model_names, key="error_model_select")

    if selected_model and selected_model in results:
        r = results[selected_model]
        y_pred = r["y_pred"]

        # ── Error Distribution Metrics ──
        err_dist = get_error_distribution(y_test, y_pred, le)

        render_metric_grid([
            {"icon": "📊", "label": "Total Predictions", "value": f"{err_dist['total']:,}"},
            {"icon": "✅", "label": "Correct", "value": f"{err_dist['correct']:,}", "sub_green": f"{err_dist['accuracy']:.2f}%"},
            {"icon": "❌", "label": "Incorrect", "value": f"{err_dist['incorrect']:,}", "sub": f"{err_dist['error_rate']:.2f}% error rate"},
            {"icon": "🎯", "label": "Accuracy", "value": f"{err_dist['accuracy']:.2f}", "unit": "%"},
        ])

        # ── Error Distribution Charts ──
        col1, col2 = st.columns(2)

        with col1:
            # Correct vs Incorrect pie
            fig_pie = plotly_pie(
                ["Correct", "Incorrect"],
                [err_dist["correct"], err_dist["incorrect"]],
                f"Prediction Distribution — {selected_model}",
                colors=["#1F7A4D", "#EF4444"]
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Per-class error rate
            class_data = err_dist["by_class"]
            class_names_list = list(class_data.keys())
            error_rates = [class_data[c]["error_rate"] for c in class_names_list]

            fig_err = go.Figure(go.Bar(
                x=class_names_list, y=error_rates,
                marker_color=["#0E4B2E", "#5FAE6E"],
                text=[f"{e:.2f}%" for e in error_rates],
                textposition="outside"
            ))
            fig_err.update_layout(
                title=dict(text="Error Rate per Class", font=dict(family="Sora", size=14, color="#123524")),
                yaxis=dict(title="Error Rate (%)", gridcolor="rgba(31,122,77,0.05)"),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#4A5568"),
                margin=dict(t=50, b=30, l=30, r=30),
            )
            st.plotly_chart(fig_err, use_container_width=True)

        # ── Misclassification Table ──
        st.markdown("---")
        st.markdown("#### 📋 Misclassified Samples")
        st.markdown("Contoh query yang salah diklasifikasikan oleh model:")

        error_df = get_error_analysis(X_test, y_test, y_pred, le, df_clean, top_n=25)

        if not error_df.empty:
            display_df = error_df[["Query", "Actual", "Predicted", "Penyebab"]].copy()
            st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)

            # ── Error Reason Breakdown ──
            st.markdown("---")
            st.markdown("#### 🔍 Penyebab Error")

            reason_counts = error_df["Penyebab"].value_counts()

            fig_reason = go.Figure(go.Bar(
                x=reason_counts.values.tolist(),
                y=reason_counts.index.tolist(),
                orientation='h',
                marker_color=["#EF4444", "#F59E0B", "#3B82F6", "#8B5CF6"][:len(reason_counts)],
                text=[f"{v}" for v in reason_counts.values],
                textposition="outside"
            ))
            fig_reason.update_layout(
                title=dict(text="Distribusi Penyebab Error", font=dict(family="Sora", size=14, color="#123524")),
                xaxis_title="Jumlah",
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#4A5568"),
                margin=dict(t=50, b=30, l=30, r=30),
                height=300
            )
            st.plotly_chart(fig_reason, use_container_width=True)
        else:
            st.success("🎉 Tidak ada error ditemukan! Model ini sangat akurat.")

        # ── Why Model Fails ──
        st.markdown("---")
        render_section_header("Insights", "Why Models Fail", "Analisis penyebab umum kesalahan klasifikasi.")

        col1, col2 = st.columns(2)
        with col1:
            render_explain_card("🔄", "Query Ambigu",
                "Query mengandung kata-kata dari kedua kelas (Agriculture & Horticulture) sehingga model "
                "tidak dapat menentukan kelas yang tepat. Contoh: 'fruit crop management' mengandung "
                "kata 'fruit' (Horticulture) dan 'crop' (Agriculture).")

            render_explain_card("📏", "Query Terlalu Pendek",
                "Query dengan sedikit kata memberikan informasi yang terbatas untuk klasifikasi. "
                "Feature vector menjadi sangat sparse sehingga model tidak memiliki cukup sinyal.")

        with col2:
            render_explain_card("🔗", "Overlap Kata",
                "Banyak kata yang muncul di kedua kelas dengan frekuensi tinggi (seperti 'plant', 'disease', "
                "'management'). Kata-kata ini tidak diskriminatif dan membingungkan model.")

            render_explain_card("🧩", "Kurang Konteks",
                "Query tidak mengandung keyword yang jelas dari kelas manapun. Model kesulitan "
                "mengklasifikasikan query yang bersifat umum tanpa domain-specific vocabulary.")

        # ── Challenging Examples ──
        st.markdown("---")
        st.markdown("#### ⚠️ Contoh Query yang Sulit Diklasifikasikan")

        challenging_examples = [
            {"query": "How to manage plant disease in field?", "issue": "Kata 'plant' dan 'field' ambigu — bisa Agriculture atau Horticulture"},
            {"query": "What fertilizer to use?", "issue": "Terlalu umum — tidak ada keyword spesifik kelas"},
            {"query": "Pest control methods", "issue": "Berlaku untuk kedua kelas — tidak diskriminatif"},
            {"query": "Best irrigation technique", "issue": "Irrigation bisa untuk crop (Agriculture) atau garden (Horticulture)"},
        ]

        for ex in challenging_examples:
            st.markdown(f"""
            <div class='error-card'>
                <div style='font-family:JetBrains Mono; font-size:0.88rem; color:#1a1a1a; margin-bottom:6px;'>"{ex['query']}"</div>
                <div style='font-size:0.8rem; color:#EF4444;'>⚠️ {ex['issue']}</div>
            </div>
            """, unsafe_allow_html=True)
