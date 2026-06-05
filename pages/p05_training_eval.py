# ════════════════════════════════════════════════════════════════
# PAGE 05 — TRAINING & EVALUATION
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
from components.charts import plotly_cm, plotly_bar
from backend.model_loader import SCENARIO_NAMES


def render(ss):
    results = ss.get("results", {})
    le = ss.get("le")

    st.markdown("""
<div class='section-header'>
<div class='section-title'>🧠 Training & Evaluation</div>
<div class='section-subtitle'>Detail evaluasi per model — pilih model untuk melihat metrik lengkap</div>
</div>
""", unsafe_allow_html=True)

    if not results:
        st.warning("Hasil evaluasi belum tersedia.")
        return

    available_models = [n for n in SCENARIO_NAMES if n in results]
    selected = st.selectbox("Pilih Model:", available_models, index=0)

    if selected not in results:
        st.warning(f"Model {selected} belum dievaluasi.")
        return

    r = results[selected]

    # Metrics Cards
    acc = r["accuracy"] * 100
    prec = r["precision"] * 100
    rec = r["recall"] * 100
    f1 = r["f1_score"] * 100
    inf_time = r.get("inference_time", 0)

    st.markdown(f"""
<div class='kpi-grid'>
<div class='kpi-card'>
<div class='kpi-icon'>🎯</div>
<div class='kpi-label'>Accuracy</div>
<div class='kpi-value'>{acc:.2f}%</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>📌</div>
<div class='kpi-label'>Precision</div>
<div class='kpi-value'>{prec:.2f}%</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>🔁</div>
<div class='kpi-label'>Recall</div>
<div class='kpi-value'>{rec:.2f}%</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>⚖️</div>
<div class='kpi-label'>F1-Score</div>
<div class='kpi-value'>{f1:.2f}%</div>
</div>
<div class='kpi-card'>
<div class='kpi-icon'>⏱️</div>
<div class='kpi-label'>Waktu Inferensi</div>
<div class='kpi-value'>{inf_time:.3f}s</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Model info
    model_type = r.get("model_type", "N/A")
    feature_type = r.get("feature_type", "N/A")
    group = r.get("group", "N/A")

    st.markdown(f"""
<div class='card-static' style='padding:18px 22px;'>
<span class='badge'>Algoritma: {model_type}</span>
<span class='badge'>Fitur: {feature_type}</span>
<span class='badge'>Kelompok: {group}</span>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Confusion Matrix
    with col1:
        st.markdown("""
<div class='section-header'>
<div class='section-title'>📊 Confusion Matrix</div>
</div>
""", unsafe_allow_html=True)
        cm = r.get("cm")
        if cm is not None:
            labels = list(le.classes_) if le is not None else ["Class 0", "Class 1"]
            fig = plotly_cm(cm, f"Confusion Matrix — {selected}", labels)
            st.plotly_chart(fig, use_container_width=True)

    # Metric Bar Chart
    with col2:
        st.markdown("""
<div class='section-header'>
<div class='section-title'>📈 Perbandingan Metrik</div>
</div>
""", unsafe_allow_html=True)
        fig = plotly_bar(
            names=["Accuracy", "Precision", "Recall", "F1-Score"],
            values=[acc, prec, rec, f1],
            title=f"Metrik Evaluasi — {selected}",
            text_format=".2f"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Classification Report
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📋 Classification Report</div>
</div>
""", unsafe_allow_html=True)

    report = r.get("report", {})
    if report:
        report_data = []
        labels = list(le.classes_) if le is not None else []
        for label in labels:
            label_key = str(label)
            if label_key in report:
                rr = report[label_key]
                report_data.append({
                    "Kelas": label,
                    "Precision": f"{rr.get('precision', 0)*100:.2f}%",
                    "Recall": f"{rr.get('recall', 0)*100:.2f}%",
                    "F1-Score": f"{rr.get('f1-score', 0)*100:.2f}%",
                    "Support": int(rr.get('support', 0))
                })

        if report_data:
            st.dataframe(pd.DataFrame(report_data), use_container_width=True, hide_index=True)
