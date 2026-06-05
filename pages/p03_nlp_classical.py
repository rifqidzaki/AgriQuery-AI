# ════════════════════════════════════════════════════════════════
# PAGE 03 — NLP CLASSICAL (BoW, TF-IDF, N-Gram)
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
from components.metrics import render_metric_grid, render_section_header, render_explain_card, render_pros_cons
from components.charts import plotly_horizontal_bar, plotly_grouped_bar, plotly_heatmap, EMERALD_PALETTE
from backend.classical_nlp import get_feature_info, get_top_tokens, get_class_top_tokens, CLASSICAL_EXPLANATIONS
import plotly.graph_objects as go


def render(ss):
    """Render the NLP Classical page."""
    vectorizers = ss.get("vectorizers", {})
    df_clean = ss.get("df_clean")
    classical_data = ss.get("classical_data", {})
    y_train = ss.get("y_train")
    le = ss.get("le")

    if not vectorizers or df_clean is None:
        st.warning("Data belum dimuat.")
        return

    render_section_header(
        "Feature Engineering",
        "NLP Classical Features",
        "Analisis representasi vektor teks menggunakan metode klasik: Bag of Words, TF-IDF, dan N-Gram.",
        extra_badges=[{"text": "Sparse Representation", "type": "gold"}]
    )

    # ── Explanation Cards ──
    cols = st.columns(3)
    for col, (key, info) in zip(cols, CLASSICAL_EXPLANATIONS.items()):
        with col:
            render_explain_card(
                info["title"].split(" ")[0],  # emoji
                info["title"].split(" ", 1)[1] if " " in info["title"] else info["title"],
                f"{info['desc']}<br><br><code>{info['formula']}</code>"
            )

    st.markdown("---")

    # ── Tabs for each method ──
    classical_features = ["BoW", "TF-IDF", "N-Gram"]
    available_features = [f for f in classical_features if f in vectorizers]

    if not available_features:
        st.warning("Tidak ada vectorizer classical yang tersedia.")
        return

    tabs = st.tabs([f"📌 {f}" for f in available_features])

    for tab, feat_name in zip(tabs, available_features):
        with tab:
            vec = vectorizers[feat_name]
            info = get_feature_info(vec)

            # Metrics
            render_metric_grid([
                {"icon": "📚", "label": "Vocabulary Size", "value": f"{info['vocab_size']:,}"},
                {"icon": "🔢", "label": "N-gram Range", "value": str(info['ngram_range'])},
                {"icon": "⚙️", "label": "Max Features", "value": f"{info['max_features']:,}"},
            ])

            # Transform full dataset for analysis
            X_mat = vec.transform(df_clean["clean_text"])

            col1, col2 = st.columns(2)

            with col1:
                # Top tokens
                top_tokens, top_freqs = get_top_tokens(vec, X_mat, top_n=20)
                fig = plotly_horizontal_bar(top_tokens, top_freqs, f"Top 20 Token — {feat_name}")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Per-class top tokens
                if le is not None:
                    class_names = list(le.classes_)
                    fig_cls = go.Figure()

                    for cls_idx, cls_name in enumerate(class_names):
                        tokens, freqs = get_class_top_tokens(vec, X_mat, df_clean["label"].values, cls_idx, top_n=10)
                        color = "#0E4B2E" if cls_idx == 0 else "#5FAE6E"
                        fig_cls.add_trace(go.Bar(
                            name=cls_name,
                            x=tokens, y=freqs,
                            marker_color=color
                        ))

                    fig_cls.update_layout(
                        barmode="group",
                        title=dict(text=f"Top 10 Token per Kelas — {feat_name}",
                                   font=dict(family="Sora", size=14, color="#123524")),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Inter", color="#4A5568"),
                        margin=dict(t=50, b=30, l=30, r=30),
                        height=450
                    )
                    st.plotly_chart(fig_cls, use_container_width=True)

            # Sparse matrix visualization
            st.markdown(f"**🔬 Sparse Matrix Visualization (Sample 10×20) — {feat_name}**")
            sample_matrix = X_mat[:10, :20]
            if hasattr(sample_matrix, 'toarray'):
                sample_array = sample_matrix.toarray()
            else:
                sample_array = np.array(sample_matrix)

            sample_features = info["features"][:20]
            fig_heat = plotly_heatmap(
                sample_array,
                [str(f) for f in sample_features],
                [f"Doc {i+1}" for i in range(10)],
                f"Feature Matrix Heatmap — {feat_name}"
            )
            fig_heat.update_layout(height=350)
            st.plotly_chart(fig_heat, use_container_width=True)

            # Vocabulary sample
            st.markdown(f"**📖 Sample Vocabulary ({feat_name}) — 100 token pertama**")
            vocab_df = pd.DataFrame({"Token": info["features"][:100], "Index": range(min(100, len(info["features"])))})
            st.dataframe(vocab_df, use_container_width=True, height=200, hide_index=True)

    # ── Pros & Cons Section ──
    st.markdown("---")
    render_section_header("Analysis", "Perbandingan Metode Classical", "Kelebihan dan kekurangan setiap metode classical NLP.")

    for key, info in CLASSICAL_EXPLANATIONS.items():
        st.markdown(f"#### {info['title']}")
        render_pros_cons(info["pros"], info["cons"])

    # ── Comparison Summary ──
    st.markdown("---")
    comparison_data = []
    for feat_name in available_features:
        vec = vectorizers[feat_name]
        finfo = get_feature_info(vec)
        comparison_data.append({
            "Method": feat_name,
            "Vocabulary Size": f"{finfo['vocab_size']:,}",
            "N-gram Range": str(finfo['ngram_range']),
            "Representation": "Sparse (Frequency)" if feat_name != "TF-IDF" else "Sparse (Weighted)",
            "Captures Order": "❌" if feat_name == "BoW" else ("✅ Local" if feat_name == "N-Gram" else "✅ Partial"),
            "Semantic Info": "❌ None",
        })

    st.markdown("**📋 Feature Comparison Table**")
    st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)
