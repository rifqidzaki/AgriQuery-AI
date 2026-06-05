# ════════════════════════════════════════════════════════════════
# PAGE 04 — NLP MODERN (Word2Vec, GloVe, BERT)
# ════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
from components.metrics import render_metric_grid, render_section_header, render_explain_card
from components.charts import plotly_scatter_2d, EMERALD_PALETTE
from backend.modern_nlp import MODERN_EXPLANATIONS, TRANSFORMER_EXPLANATION, compute_similarity_demo


def render(ss):
    """Render the NLP Modern page."""
    vectorizers = ss.get("vectorizers", {})
    embedding_arrays = ss.get("embedding_arrays", {})
    le = ss.get("le")
    y_train = ss.get("y_train")
    y_test = ss.get("y_test")

    render_section_header(
        "Deep Learning",
        "NLP Modern Embeddings",
        "Representasi vektor teks menggunakan embedding modern: Word2Vec, GloVe, dan BERT Transformer.",
        extra_badges=[{"text": "Dense Representation", "type": "gold"}, {"text": "Pretrained Models"}]
    )

    # ── Embedding Overview Metrics ──
    available = []
    for name in ["Word2Vec", "GloVe", "BERT"]:
        if name in vectorizers:
            available.append(name)

    metrics = []
    for name in available:
        info = MODERN_EXPLANATIONS.get(name.lower().replace("2", "2"), {})
        dim = info.get("dim", "?")
        model_name = info.get("model", "?")
        metrics.append({"icon": "🧠", "label": f"{name} Dim", "value": str(dim), "sub": model_name})

    if metrics:
        render_metric_grid(metrics)

    # ── Explanation Cards ──
    cols = st.columns(3)
    for col, (key, info) in zip(cols, MODERN_EXPLANATIONS.items()):
        with col:
            points_html = "<br>".join([f"• {p}" for p in info["key_points"]])
            render_explain_card(
                info["title"].split(" ")[0],
                info["title"].split(" ", 1)[1] if " " in info["title"] else info["title"],
                f"{info['desc']}<br><br>{points_html}"
            )

    st.markdown("---")

    # ── Transformer / Attention Explanation ──
    render_section_header("Architecture", "Transformer & Self-Attention", "Konsep arsitektur di balik BERT embedding.")

    for key, info in TRANSFORMER_EXPLANATION.items():
        if key == "self_attention":
            render_explain_card("🔍", info["title"].replace("🔍 ", ""),
                                f"{info['desc']}<br><br><code>{info['formula']}</code>")
        elif key == "transformer_encoder":
            components_html = " → ".join([f"<code>{c}</code>" for c in info["components"]])
            render_explain_card("⚙️", info["title"].replace("⚙️ ", ""),
                                f"{info['desc']}<br><br>Pipeline: {components_html}")
        elif key == "contextual_vs_static":
            render_explain_card("🔄", info["title"].replace("🔄 ", ""), info["desc"])

    st.markdown("---")

    # ── Embedding Visualization (PCA/t-SNE) ──
    if embedding_arrays:
        render_section_header("Visualization", "Embedding Space Visualization", 
                              "Proyeksi 2D dari embedding menggunakan PCA untuk melihat separasi kelas.")

        tabs = st.tabs([f"🔮 {name}" for name in available if name in embedding_arrays])

        for tab, name in zip(tabs, [n for n in available if n in embedding_arrays]):
            with tab:
                emb_data = embedding_arrays[name]
                X_emb = emb_data["test"]  # Use test set for visualization
                y_labels = y_test

                if X_emb is not None and len(X_emb) > 0:
                    # PCA reduction
                    from sklearn.decomposition import PCA
                    n_samples = min(1000, len(X_emb))
                    X_sample = X_emb[:n_samples]
                    y_sample = y_labels[:n_samples]

                    pca = PCA(n_components=2, random_state=42)
                    X_2d = pca.fit_transform(X_sample)

                    # Map class labels to names
                    class_map = {0: "AGRICULTURE", 1: "HORTICULTURE"} if le is not None else {}
                    color_map = {0: "#0E4B2E", 1: "#5FAE6E"}

                    fig = plotly_scatter_2d(
                        X_2d[:, 0], X_2d[:, 1],
                        y_sample.tolist(),
                        f"PCA 2D Projection — {name} Embeddings (n={n_samples})",
                        color_map=color_map
                    )

                    # Update legend names
                    if le is not None:
                        for trace in fig.data:
                            class_idx = int(trace.name.split(" ")[-1])
                            if class_idx < len(le.classes_):
                                trace.name = le.classes_[class_idx]

                    explained = pca.explained_variance_ratio_
                    fig.update_layout(
                        xaxis_title=f"PC1 ({explained[0]*100:.1f}% variance)",
                        yaxis_title=f"PC2 ({explained[1]*100:.1f}% variance)",
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Embedding stats
                    col1, col2 = st.columns(2)
                    with col1:
                        render_metric_grid([
                            {"icon": "📐", "label": "Embedding Dim", "value": str(X_emb.shape[1])},
                            {"icon": "📊", "label": "Total Vectors", "value": f"{len(X_emb):,}"},
                        ])
                    with col2:
                        render_metric_grid([
                            {"icon": "🎯", "label": "PCA Variance (2D)", "value": f"{sum(explained)*100:.1f}", "unit": "%"},
                            {"icon": "📏", "label": "Mean Norm", "value": f"{np.linalg.norm(X_emb, axis=1).mean():.2f}"},
                        ])

    # ── Semantic Similarity Demo ──
    st.markdown("---")
    render_section_header("Demo", "Semantic Similarity", "Bandingkan kemiripan semantik antara kata-kata pertanian.")

    demo_words = ["rice", "wheat", "paddy", "mango", "banana", "crop", "fruit", "irrigation", "garden", "fertilizer"]

    if "Word2Vec" in vectorizers:
        st.markdown("**Word2Vec Similarity:**")
        try:
            w2v_model = vectorizers["Word2Vec"]
            sim_results = compute_similarity_demo(w2v_model, demo_words[:6], "word2vec")
            sim_df = pd.DataFrame(sim_results)
            sim_df["Similarity"] = sim_df["Similarity"].apply(lambda x: f"{x:.4f}" if x is not None else "N/A")
            st.dataframe(sim_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.info(f"Similarity demo unavailable: {e}")

    # ── Classical vs Modern Comparison ──
    st.markdown("---")
    st.markdown("""
    <div class='glass-card'>
        <div style='font-family:Sora; font-weight:700; font-size:1.15rem; margin-bottom:16px;'>🔄 Classical vs Modern — Key Differences</div>
        <table class='comparison-table' style='width:100%;'>
            <tr>
                <th>Aspect</th>
                <th>Classical (BoW/TF-IDF/N-Gram)</th>
                <th>Modern (Word2Vec/GloVe/BERT)</th>
            </tr>
            <tr>
                <td><strong>Representation</strong></td>
                <td>Sparse (high-dimensional)</td>
                <td>Dense (low-dimensional)</td>
            </tr>
            <tr>
                <td><strong>Semantic Understanding</strong></td>
                <td>❌ No semantic info</td>
                <td>✅ Captures semantic meaning</td>
            </tr>
            <tr>
                <td><strong>Context Awareness</strong></td>
                <td>❌ Context-independent</td>
                <td>✅ BERT: fully contextual</td>
            </tr>
            <tr>
                <td><strong>Vocabulary</strong></td>
                <td>Limited to training data</td>
                <td>Pretrained on massive corpora</td>
            </tr>
            <tr>
                <td><strong>Computation</strong></td>
                <td>⚡ Very fast</td>
                <td>🐢 Slower (especially BERT)</td>
            </tr>
            <tr>
                <td><strong>Interpretability</strong></td>
                <td>✅ Easy to interpret</td>
                <td>❌ Black box</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
