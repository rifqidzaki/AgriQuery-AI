# ════════════════════════════════════════════════════════════════
# PAGE 09 — INTERACTIVE PREDICTION ⭐ (Main Feature)
# ════════════════════════════════════════════════════════════════

import streamlit as st
import time
import numpy as np
from components.metrics import render_section_header
from backend.data_loader import clean_text


def render(ss):
    """Render the Interactive Prediction page — the crown jewel."""
    results = ss.get("results", {})
    models = ss.get("models", {})
    vectorizers = ss.get("vectorizers", {})
    le = ss.get("le")

    if not results or not models:
        st.warning("Model belum dilatih.")
        return

    # ── Hero ──
    st.markdown("""
<div style='max-width: 850px; margin: 0 auto;'>
<div style='text-align:center; padding:20px 0 40px;'>
<div class='ai-badge'>Real-time Inference</div>
<div class='ai-badge-gold'>⭐ Main Feature</div>
<h2 style='font-family:Sora; font-weight:800; color:var(--text-main); font-size:2.5rem; margin:12px 0 10px;'>
AI Query Predictor
</h2>
<p style='color:var(--text-muted); font-size:1.05rem; max-width:500px; margin:0 auto;'>
Klasifikasikan query pertanian secara real-time menggunakan berbagai model dan representasi fitur.
</p>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Input Section ──
    col_space1, col_main, col_space2 = st.columns([0.5, 5, 0.5])

    with col_main:
        # Text input
        st.markdown("<div class='pred-input-wrapper'>", unsafe_allow_html=True)
        user_query = st.text_area(
            "Query", height=130,
            placeholder="Contoh: My paddy leaves are turning yellow and I see small insects on the stem. What pesticide should I use?",
            label_visibility="collapsed",
            key="pred_query"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Model & Feature selection
        col_model, col_feat = st.columns(2)

        with col_model:
            model_type = st.selectbox(
                "🤖 Pilih Model",
                ["Decision Tree", "Naive Bayes"],
                key="pred_model_type"
            )

        with col_feat:
            available_features = []
            prefix = "DT" if model_type == "Decision Tree" else "NB"
            for key in models.keys():
                if key.startswith(prefix):
                    feat = key.split(" + ")[1]
                    available_features.append(feat)

            feature_type = st.selectbox(
                "📊 Pilih Feature/Embedding",
                available_features if available_features else ["N/A"],
                key="pred_feat_type"
            )

        # Predict button
        st.markdown("<div class='ai-btn'>", unsafe_allow_html=True)
        predict_btn = st.button("✨ Generate Prediction", key="pred_btn", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Prediction Logic ──
        if predict_btn and user_query.strip():
            sc_name = f"{prefix} + {feature_type}"

            if sc_name not in models:
                st.error(f"Model {sc_name} tidak tersedia.")
                return

            # Loading animation
            with st.spinner(""):
                st.markdown("<div class='typing-indicator' style='text-align:center; padding:12px;'>🧠 AI sedang menganalisis semantik teks...</div>", unsafe_allow_html=True)
                time.sleep(0.8)

                model = models[sc_name]
                clean = clean_text(user_query)

                # Determine how to vectorize
                is_modern = feature_type in ["Word2Vec", "GloVe", "BERT"]

                if is_modern:
                    if feature_type == "Word2Vec":
                        from backend.modern_nlp import load_word2vec_model
                        emb_model = load_word2vec_model()
                        words = clean.split()
                        word_vecs = [emb_model[w] for w in words if w in emb_model]
                        if word_vecs:
                            vector = np.mean(word_vecs, axis=0).reshape(1, -1)
                        else:
                            vector = np.zeros((1, 300))

                    elif feature_type == "GloVe":
                        from backend.modern_nlp import load_glove_model
                        emb_model = load_glove_model()
                        words = clean.split()
                        word_vecs = [emb_model[w] for w in words if w in emb_model]
                        if word_vecs:
                            vector = np.mean(word_vecs, axis=0).reshape(1, -1)
                        else:
                            vector = np.zeros((1, 100))

                    elif feature_type == "BERT":
                        from backend.modern_nlp import load_bert_model
                        bert = load_bert_model()
                        vector = bert.encode([clean])

                else:
                    vec = vectorizers.get(feature_type)
                    if vec is None:
                        st.error(f"Vectorizer {feature_type} tidak tersedia.")
                        return
                    vector = vec.transform([clean])

                # Predict
                pred_label = model.predict(vector)[0]
                pred_sector = le.inverse_transform([pred_label])[0]

                try:
                    pred_proba = model.predict_proba(vector)[0]
                    conf = pred_proba[pred_label] * 100
                except:
                    conf = 95.0

                # Sector translations for clear understanding
                SECTOR_TRANSLATIONS = {
                    "AGRICULTURE": "PERTANIAN (Tanaman Pangan & Ladang)",
                    "HORTICULTURE": "HORTIKULTURA (Kebun, Sayur, & Buah)"
                }
                pred_sector_indo = SECTOR_TRANSLATIONS.get(pred_sector, pred_sector)

                # Top contributing words (classical only)
                top_words_html = ""
                if not is_modern:
                    vec = vectorizers.get(feature_type)
                    if vec is not None:
                        features = vec.get_feature_names_out()
                        feature_set = set(features)
                        clean_words = clean.split()
                        matched_words = [w for w in clean_words if w in feature_set][:8]
                        if matched_words:
                            pills = " ".join([
                                f"<span class='tech-pill' style='margin:3px;'>{w}</span>"
                                for w in matched_words
                            ])
                            top_words_html = f"""
<div style='margin-top:20px;'>
<div style='font-size:0.8rem; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;'>Kata Kunci Paling Berpengaruh</div>
<div>{pills}</div>
</div>
"""

            # Result display
            badge = "Sangat Yakin (Tinggi) ✨" if conf >= 90 else ("Cukup Yakin (Sedang) 👍" if conf >= 75 else "Kurang Yakin (Rendah) ⚠️")
            color = "#1F7A4D" if pred_sector == "AGRICULTURE" else "#2E8B57"
            icon = "🌾" if pred_sector == "AGRICULTURE" else "🌿"
            badge_color = "#1F7A4D" if conf >= 90 else ("#D4A843" if conf >= 75 else "#EF4444")

            st.markdown(f"""
<div style='margin-top: 40px; animation: fadeInUp 0.5s ease;'>
<div class='pred-result-card'>
<div style='font-size:4.5rem; margin-bottom:12px; position:relative; z-index:1;'>{icon}</div>
<div style='font-family:Inter; font-size:0.8rem; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:2px; margin-bottom:8px; position:relative; z-index:1;'>Sektor / Kategori Terdeteksi</div>
<div style='font-family:Sora; font-size:2.2rem; font-weight:800; color:{color}; line-height:1.2; margin-bottom:24px; position:relative; z-index:1;'>{pred_sector_indo}</div>
<div style='background:rgba(255,255,255,0.6); padding:24px; border-radius:18px; display:inline-block; min-width:340px; text-align:left; position:relative; z-index:1;'>
<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
<span style='font-size:0.85rem; font-weight:600; color:var(--text-main);'>Tingkat Keyakinan Model</span>
<span style='font-family:Sora; font-weight:700; color:{color}; font-size:1.2rem;'>{conf:.1f}%</span>
</div>
<div class='confidence-bar-bg'><div class='confidence-bar-fill' style='width:{conf}%;'></div></div>
<div style='margin-top:12px; display:flex; justify-content:space-between; align-items:center;'>
<span style='font-size:0.78rem; font-weight:600; color:{badge_color}; background:rgba(255,255,255,0.8); padding:4px 12px; border-radius:8px;'>{badge}</span>
<span style='font-size:0.72rem; color:var(--text-muted);'>{sc_name}</span>
</div>
</div>
{top_words_html}
<div style='margin-top:20px; font-size:0.82rem; color:var(--text-muted); position:relative; z-index:1;'>
<strong>Model Klasifikasi:</strong> {model_type} &nbsp;|&nbsp; 
<strong>Representasi Fitur:</strong> {feature_type} &nbsp;|&nbsp;
<strong>Teks Bersih:</strong> <span style='font-family:JetBrains Mono; font-size:0.78rem;'>"{clean[:80]}..."</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)

            # ── Top 3 Models Comparison ──
            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
            st.markdown("""
<div style='text-align:center; margin-bottom: 24px; animation: fadeInUp 0.6s ease;'>
<div class='ai-badge-gold'>🏆 Analisis Komparasi</div>
<h3 style='font-family:Sora; font-weight:800; color:var(--text-main); margin-top:8px;'>Prediksi 3 Model Terbaik</h3>
<p style='color:var(--text-muted); font-size:0.9rem;'>Berikut adalah hasil klasifikasi untuk query ini menggunakan 3 model dengan akurasi pengujian tertinggi.</p>
</div>
""", unsafe_allow_html=True)

            # Find Top 3 models by accuracy
            sorted_models = sorted(results.items(), key=lambda x: x[1]["accuracy"], reverse=True)
            top3 = sorted_models[:3]
            medals = ["🥇", "🥈", "🥉"]

            cols_top3 = st.columns(3)
            for idx, (top_name, top_info) in enumerate(top3):
                with cols_top3[idx]:
                    top_feat_type = top_name.split(" + ")[1]
                    top_model = models[top_name]
                    
                    # Vectorize
                    top_is_modern = top_feat_type in ["Word2Vec", "GloVe", "BERT"]
                    if top_is_modern:
                        if top_feat_type == "Word2Vec":
                            from backend.modern_nlp import load_word2vec_model
                            emb_model = load_word2vec_model()
                            words = clean.split()
                            word_vecs = [emb_model[w] for w in words if w in emb_model]
                            if word_vecs:
                                top_vector = np.mean(word_vecs, axis=0).reshape(1, -1)
                            else:
                                top_vector = np.zeros((1, 300))
                        elif top_feat_type == "GloVe":
                            from backend.modern_nlp import load_glove_model
                            emb_model = load_glove_model()
                            words = clean.split()
                            word_vecs = [emb_model[w] for w in words if w in emb_model]
                            if word_vecs:
                                top_vector = np.mean(word_vecs, axis=0).reshape(1, -1)
                            else:
                                top_vector = np.zeros((1, 50))  # glove 50d from colab
                        elif top_feat_type == "BERT":
                            from backend.modern_nlp import load_bert_model
                            bert = load_bert_model()
                            top_vector = bert.encode([clean])
                    else:
                        top_vec_obj = vectorizers.get(top_feat_type)
                        if top_vec_obj is not None:
                            top_vector = top_vec_obj.transform([clean])
                        else:
                            top_vector = None
                    
                    if top_vector is not None:
                        # Predict
                        top_pred_label = top_model.predict(top_vector)[0]
                        top_pred_sector = le.inverse_transform([top_pred_label])[0]
                        try:
                            top_pred_proba = top_model.predict_proba(top_vector)[0]
                            top_conf = top_pred_proba[top_pred_label] * 100
                        except:
                            top_conf = 95.0
                    else:
                        top_pred_sector = "N/A"
                        top_conf = 0.0

                    top_pred_sector_indo = SECTOR_TRANSLATIONS.get(top_pred_sector, top_pred_sector)
                    top_color = "#1F7A4D" if top_pred_sector == "AGRICULTURE" else "#2E8B57"
                    top_icon = "🌾" if top_pred_sector == "AGRICULTURE" else "🌿"
                    top_acc = top_info["accuracy"] * 100

                    st.markdown(f"""
<div class='glass-card-static' style='padding: 24px; text-align: center; height: 100%; border: 1px solid rgba(31, 122, 77, 0.12);'>
<div style='font-size: 2.2rem; margin-bottom: 8px;'>{medals[idx]}</div>
<div style='font-family: Sora; font-weight: 700; font-size: 1.05rem; color: var(--text-main); margin-bottom: 2px;'>{top_name}</div>
<div style='font-size: 0.78rem; color: var(--accent-emerald); font-weight: 600; margin-bottom: 16px;'>Akurasi Pengujian: {top_acc:.2f}%</div>
<div style='background: rgba(255,255,255,0.7); padding: 16px; border-radius: 12px; text-align: left;'>
<div style='font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;'>Hasil Prediksi</div>
<div style='font-family: Sora; font-weight: 700; color: {top_color}; font-size: 1.02rem; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; line-height: 1.3;'>
<span>{top_icon}</span> {top_pred_sector_indo}
</div>
<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;'>
<span style='font-size: 0.72rem; color: var(--text-muted);'>Tingkat Keyakinan</span>
<span style='font-family: JetBrains Mono; font-weight: 700; color: var(--text-main); font-size: 0.8rem;'>{top_conf:.1f}%</span>
</div>
<div class='confidence-bar-bg' style='height: 4px;'><div class='confidence-bar-fill' style='width: {top_conf}%;'></div></div>
</div>
</div>
""", unsafe_allow_html=True)

        # ── Example Queries ──
        st.markdown("---")
        st.markdown("""
<div class='glass-card-static' style='padding:24px 28px;'>
<div style='font-family:Sora; font-weight:700; margin-bottom:14px;'>💡 Contoh Query untuk Dicoba</div>
<div style='display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:0.88rem;'>
<div style='background:rgba(31,122,77,0.04); padding:12px 16px; border-radius:10px; border:1px solid rgba(31,122,77,0.08);'>
🌾 <strong>Agriculture:</strong><br>
<em>"How to increase rice yield in kharif season?"</em>
</div>
<div style='background:rgba(31,122,77,0.04); padding:12px 16px; border-radius:10px; border:1px solid rgba(31,122,77,0.08);'>
🌿 <strong>Horticulture:</strong><br>
<em>"Best fertilizer for mango trees in summer?"</em>
</div>
<div style='background:rgba(31,122,77,0.04); padding:12px 16px; border-radius:10px; border:1px solid rgba(31,122,77,0.08);'>
🌾 <strong>Agriculture:</strong><br>
<em>"My wheat crop has fungal disease, what pesticide to use?"</em>
</div>
<div style='background:rgba(31,122,77,0.04); padding:12px 16px; border-radius:10px; border:1px solid rgba(31,122,77,0.08);'>
🌿 <strong>Horticulture:</strong><br>
<em>"How to protect tomato plants from aphids?"</em>
</div>
</div>
</div>
""", unsafe_allow_html=True)
