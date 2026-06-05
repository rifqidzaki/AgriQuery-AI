# ════════════════════════════════════════════════════════════════
# PAGE 08 — INTERACTIVE PREDICTION
# ════════════════════════════════════════════════════════════════

import streamlit as st
import time
from backend.data_loader import clean_text
from backend.model_loader import SCENARIO_NAMES, load_sklearn_model, _transform_classical, transform_modern
from backend.transformer_inference import predict_transformer, is_transformer_available


def render(ss):
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🎯 Interactive Prediction</div>
<div class='section-subtitle'>Uji coba prediksi sentimen query secara real-time dengan model pilihan</div>
</div>
""", unsafe_allow_html=True)

    results = ss.get("results", {})
    le = ss.get("le")

    if not results:
        st.warning("Model belum dimuat. Silakan tunggu di halaman Overview.")
        return

    available_models = list(results.keys())

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
<div class='card-static'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:12px;'>⚙️ Konfigurasi</div>
</div>
""", unsafe_allow_html=True)

        selected_model_name = st.selectbox("Pilih Model:", available_models)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
<div style='font-size:0.85rem; color:var(--text-secondary); line-height:1.6;'>
<b>Tips:</b>
<ul>
<li>Gunakan teks bahasa Inggris</li>
<li>Coba query terkait pupuk, cuaca, harga tanaman, atau hama</li>
</ul>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class='card-static'>
<div style='font-family:Sora; font-weight:700; font-size:1rem; margin-bottom:12px;'>📝 Input Teks</div>
</div>
""", unsafe_allow_html=True)

        user_text = st.text_area("Masukkan query pertanian:", height=100,
                                 placeholder="Contoh: What is the best fertilizer for growing tomatoes in summer?")

        if st.button("Prediksi Sekarang", type="primary", use_container_width=True):
            if not user_text.strip():
                st.warning("⚠️ Masukkan teks terlebih dahulu!")
            else:
                with st.spinner(f"Memproses dengan {selected_model_name}..."):
                    # Preprocessing
                    cleaned_text = clean_text(user_text)

                    # Model selection
                    r = results[selected_model_name]
                    model_type = r.get("model_type", "Unknown")
                    feature_type = r.get("feature_type", "Unknown")
                    is_transformer = (r.get("group") == "Transformer Fine-Tuning")

                    pred_class = None
                    pred_prob = None
                    inference_time = 0

                    try:
                        if is_transformer:
                            # Transformer Inference
                            res = predict_transformer(cleaned_text)
                            if res and "error" not in res:
                                pred_class = res["class_name"]
                                confidence = res["confidence"]
                                inference_time = res["inference_time"]
                            else:
                                st.error("Gagal melakukan prediksi dengan Transformer.")
                        else:
                            # Sklearn Inference
                            from backend.model_loader import SKLEARN_SCENARIOS
                            sc = next((s for s in SKLEARN_SCENARIOS if s["name"] == selected_model_name), None)
                            
                            if sc:
                                t0 = time.time()
                                model = load_sklearn_model(sc["model_file"])
                                
                                if sc["vec_file"]:
                                    X_trans, _ = _transform_classical([cleaned_text], sc["vec_file"])
                                else:
                                    X_trans = transform_modern([cleaned_text], sc["feature"])

                                if X_trans is not None and model is not None:
                                    # Predict
                                    pred_idx = model.predict(X_trans)[0]
                                    pred_class = le.classes_[pred_idx] if le else f"Class {pred_idx}"
                                    
                                    # Probability if available
                                    if hasattr(model, "predict_proba"):
                                        probs = model.predict_proba(X_trans)[0]
                                        confidence = max(probs) * 100
                                    else:
                                        confidence = 100.0  # fallback
                                        
                                    inference_time = time.time() - t0

                        # Render Results
                        if pred_class is not None:
                            st.markdown("""
<div class='section-header' style='padding-top:10px;'>
<div class='section-title'>📊 Hasil Prediksi</div>
</div>
""", unsafe_allow_html=True)

                            color = "var(--primary)" if pred_class == "AGRICULTURE" else "var(--secondary)"
                            
                            st.markdown(f"""
<div class='pred-result-card' style='border-color:{color};'>
<div style='font-size:0.9rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;'>KELAS PREDIKSI</div>
<div style='font-family:Sora; font-size:2.5rem; font-weight:800; color:{color}; margin-bottom:16px;'>{pred_class}</div>

<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;'>
<span style='font-size:0.85rem; font-weight:600;'>Confidence Level</span>
<span style='font-size:0.85rem; font-weight:700;'>{confidence:.1f}%</span>
</div>
<div class='confidence-bar-bg'>
<div class='confidence-bar-fill' style='width:{confidence}%;'></div>
</div>

<div style='display:flex; justify-content:space-between; margin-top:24px; padding-top:16px; border-top:1px solid var(--border);'>
<div style='text-align:left;'>
<div style='font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;'>Model</div>
<div style='font-weight:600; font-size:0.85rem;'>{selected_model_name}</div>
</div>
<div style='text-align:right;'>
<div style='font-size:0.7rem; color:var(--text-muted); text-transform:uppercase;'>Waktu Inferensi</div>
<div style='font-weight:600; font-size:0.85rem;'>{inference_time:.4f} detik</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

                            # Debug info
                            with st.expander("Tampilkan Debug Info"):
                                st.markdown(f"""
- **Raw Text**: `{user_text}`
- **Clean Text**: `{cleaned_text}`
- **Algorithm**: {model_type}
- **Feature Extraction**: {feature_type}
                                """)

                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat inferensi: {e}")
