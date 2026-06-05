# ════════════════════════════════════════════════════════════════
# PAGE 08 — EXPLAINABILITY
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
from components.metrics import render_metric_grid, render_section_header, render_explain_card
from components.charts import plotly_horizontal_bar, EMERALD_PALETTE
from backend.explainability import get_dt_feature_importance, get_keyword_contribution, get_top_words_per_class
import plotly.graph_objects as go


def render(ss):
    """Render the Explainability page."""
    results = ss.get("results", {})
    vectorizers = ss.get("vectorizers", {})
    models = ss.get("models", {})
    le = ss.get("le")
    df_clean = ss.get("df_clean")
    classical_data = ss.get("classical_data", {})
    y_train = ss.get("y_train")

    if not results:
        st.warning("Model belum dilatih.")
        return

    render_section_header(
        "Explainable AI",
        "Model Interpretability",
        "Memahami bagaimana model mengambil keputusan — feature importance, keyword contribution, dan class discrimination.",
        extra_badges=[{"text": "XAI", "type": "gold"}]
    )

    # ── How Models Decide ──
    st.markdown("""
    <div class='glass-card'>
        <div style='font-family:Sora; font-weight:700; font-size:1.15rem; margin-bottom:16px;'>🧠 Bagaimana Model Mengambil Keputusan</div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:20px;'>
            <div style='background:rgba(31,122,77,0.04); border-radius:16px; padding:20px; border:1px solid rgba(31,122,77,0.08);'>
                <div style='font-family:Sora; font-weight:700; margin-bottom:8px;'>🌳 Decision Tree</div>
                <div style='font-size:0.88rem; color:var(--text-secondary); line-height:1.7;'>
                    Membuat keputusan berdasarkan <strong>aturan if-then</strong> dari fitur. Setiap node memilih 
                    fitur terbaik untuk membagi data. Feature importance dihitung dari total penurunan impurity 
                    (Gini) yang disebabkan oleh setiap fitur.
                </div>
            </div>
            <div style='background:rgba(31,122,77,0.04); border-radius:16px; padding:20px; border:1px solid rgba(31,122,77,0.08);'>
                <div style='font-family:Sora; font-weight:700; margin-bottom:8px;'>📊 Naive Bayes</div>
                <div style='font-size:0.88rem; color:var(--text-secondary); line-height:1.7;'>
                    Menghitung <strong>probabilitas posterior</strong> setiap kelas berdasarkan Bayes' theorem. 
                    Setiap kata/fitur berkontribusi terhadap log-probability kelas. Kata yang lebih sering 
                    muncul di satu kelas memiliki kontribusi lebih besar.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Feature Importance (Decision Tree only) ──
    dt_classical = [k for k in results.keys() if k.startswith("DT") and any(c in k for c in ["BoW", "TF-IDF", "N-Gram"])]

    if dt_classical:
        render_section_header("Feature Importance", "Decision Tree — Top Features",
                              "Fitur paling penting menurut Decision Tree (berdasarkan Gini impurity decrease).")

        tabs = st.tabs([f"📌 {name}" for name in dt_classical])

        for tab, sc_name in zip(tabs, dt_classical):
            with tab:
                model = models.get(sc_name)
                feat_name = sc_name.split(" + ")[1]
                vec = vectorizers.get(feat_name)

                if model is not None and vec is not None and hasattr(model, 'feature_importances_'):
                    features = vec.get_feature_names_out()
                    top_features, top_importances = get_dt_feature_importance(model, features, top_n=25)

                    col1, col2 = st.columns([2, 1])

                    with col1:
                        fig = plotly_horizontal_bar(
                            top_features, top_importances,
                            f"Top 25 Feature Importance — {sc_name}"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    with col2:
                        st.markdown("**📋 Top Features Table**")
                        imp_df = pd.DataFrame({
                            "Rank": [f"#{i+1}" for i in range(len(top_features))],
                            "Feature": top_features,
                            "Importance": [f"{v:.6f}" for v in top_importances]
                        })
                        st.dataframe(imp_df, use_container_width=True, hide_index=True, height=500)

    # ── Top Discriminative Words per Class ──
    st.markdown("---")
    render_section_header("Class Discrimination", "Kata Diskriminatif per Kelas",
                          "Kata-kata yang paling membedakan antara Agriculture dan Horticulture.")

    classical_feats = [f for f in ["BoW", "TF-IDF", "N-Gram"] if f in vectorizers]

    if classical_feats and df_clean is not None and le is not None:
        sel_feat = st.selectbox("Pilih feature:", classical_feats, key="explain_feat_select")
        vec = vectorizers[sel_feat]
        X_full = vec.transform(df_clean["clean_text"])
        y_full = df_clean["label"].values

        disc_words = get_top_words_per_class(vec, X_full, y_full, list(le.classes_), top_n=15)

        cols = st.columns(len(disc_words))
        for col, (cls_name, data) in zip(cols, disc_words.items()):
            with col:
                st.markdown(f"**{'🌾' if 'AGRI' in cls_name else '🌿'} {cls_name}**")

                fig = go.Figure(go.Bar(
                    x=data["scores"][::-1],
                    y=data["words"][::-1],
                    orientation='h',
                    marker_color="#0E4B2E" if "AGRI" in cls_name else "#5FAE6E",
                    text=[f"{s:.6f}" for s in data["scores"][::-1]],
                    textposition="outside"
                ))
                fig.update_layout(
                    title=dict(text=f"Discriminative Words — {cls_name}",
                               font=dict(family="Sora", size=13, color="#123524")),
                    xaxis_title="Score",
                    height=450,
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter", color="#4A5568"),
                    margin=dict(t=50, b=30, l=30, r=30),
                )
                st.plotly_chart(fig, use_container_width=True)

    # ── Keyword Contribution Demo ──
    st.markdown("---")
    render_section_header("Demo", "Keyword Contribution Analysis",
                          "Lihat kontribusi setiap kata terhadap prediksi model.")

    col_feat, col_model = st.columns(2)
    with col_feat:
        avail_feats = [f for f in ["BoW", "TF-IDF", "N-Gram"] if f in vectorizers]
        if avail_feats:
            demo_feat = st.selectbox("Feature:", avail_feats, key="explain_demo_feat")
        else:
            demo_feat = None
    with col_model:
        if demo_feat:
            demo_model_key = f"DT + {demo_feat}"
            st.text_input("Model:", value=demo_model_key, disabled=True, key="explain_demo_model")
        else:
            demo_model_key = None

    demo_text = st.text_area(
        "Masukkan query untuk analisis:",
        value="My rice paddy leaves are turning yellow and I see insects on the stem",
        height=80, key="explain_demo_text"
    )

    if demo_text and demo_feat and demo_model_key and demo_model_key in models:
        if st.button("🔍 Analyze Keywords", key="explain_analyze_btn"):
            vec = vectorizers[demo_feat]
            model = models[demo_model_key]

            contributions, pred_label, pred_proba = get_keyword_contribution(
                demo_text, vec, model, le, top_n=15
            )

            if le is not None and pred_label is not None:
                pred_class = le.inverse_transform([pred_label])[0]
                confidence = pred_proba[pred_label] * 100 if pred_proba is not None else 0

                st.markdown(f"""
<div class='glass-card' style='text-align:center; padding:24px;'>
<div style='font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px;'>Prediction</div>
<div style='font-family:Sora; font-size:1.8rem; font-weight:800; color:var(--accent-emerald);'>{pred_class}</div>
<div style='font-size:0.9rem; color:var(--text-muted);'>Confidence: {confidence:.1f}%</div>
</div>
""", unsafe_allow_html=True)

            # Show contributions
            if contributions:
                st.markdown("**🔑 Keyword Contributions:**")
                for c in contributions:
                    if c["in_vocab"]:
                        bar_width = min(abs(c["contribution"]) * 500, 100)
                        color = "#1F7A4D" if c["contribution"] > 0 else "#EF4444"
                        direction = "+" if c["contribution"] > 0 else ""
                        st.markdown(f"""
<div style='display:flex; align-items:center; gap:12px; margin:4px 0; padding:8px 12px; background:rgba(255,255,255,0.5); border-radius:10px;'>
<div style='font-family:JetBrains Mono; font-weight:600; min-width:120px;'>{c['word']}</div>
<div style='flex:1; height:6px; background:rgba(0,0,0,0.04); border-radius:4px; overflow:hidden;'>
<div style='width:{bar_width}%; height:100%; background:{color}; border-radius:4px;'></div>
</div>
<div style='font-family:JetBrains Mono; font-size:0.8rem; color:{color}; min-width:80px; text-align:right;'>
{direction}{c['contribution']:.4f}
</div>
</div>
""", unsafe_allow_html=True)

    # ── Interpretability Comparison ──
    st.markdown("---")
    st.markdown("""
<div class='glass-card'>
<div style='font-family:Sora; font-weight:700; font-size:1.15rem; margin-bottom:16px;'>📊 Interpretability Comparison</div>
<table class='comparison-table' style='width:100%;'>
<tr>
<th>Aspect</th>
<th>Decision Tree</th>
<th>Naive Bayes</th>
</tr>
<tr>
<td><strong>Interpretability</strong></td>
<td>⭐⭐⭐⭐⭐ Sangat tinggi</td>
<td>⭐⭐⭐⭐ Tinggi</td>
</tr>
<tr>
<td><strong>Decision Process</strong></td>
<td>If-then rules (tree path)</td>
<td>Probabilistic (Bayes' theorem)</td>
</tr>
<tr>
<td><strong>Feature Importance</strong></td>
<td>✅ Built-in (Gini importance)</td>
<td>✅ Log-probability contributions</td>
</tr>
<tr>
<td><strong>Visualization</strong></td>
<td>✅ Tree diagram</td>
<td>⚠️ Probability distribution</td>
</tr>
<tr>
<td><strong>Explainability Type</strong></td>
<td>Inherently interpretable</td>
<td>Probabilistic model</td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)
