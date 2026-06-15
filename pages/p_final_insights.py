# ════════════════════════════════════════════════════════════════
# PAGE: FINAL INSIGHTS — Research Conclusions
# ════════════════════════════════════════════════════════════════

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from backend.research_data import FINAL_INSIGHTS, SCENARIO_RESULTS, TOP_MODELS


def render(ss):
    st.markdown("""
<div class='section-header'>
<div class='section-title'>💡 Final Insights</div>
<div class='section-subtitle'>Kesimpulan penelitian dan rekomendasi berdasarkan hasil 30 eksperimen Project v7</div>
</div>
""", unsafe_allow_html=True)

    # ── Research Summary Banner ──────────────────────────────────
    st.markdown("""
<div class='card' style='background:linear-gradient(135deg, rgba(27,94,32,0.08) 0%, rgba(102,187,106,0.04) 100%);
border:1px solid rgba(27,94,32,0.15); padding:24px; margin-bottom:24px;'>
<div style='font-family:Sora; font-weight:700; font-size:1.1rem; margin-bottom:16px; color:var(--primary);'>
🌾 Ringkasan Penelitian — Project v7 Final
</div>
<div style='display:grid; grid-template-columns:repeat(4,1fr); gap:16px; text-align:center;'>
<div>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase; margin-bottom:4px;'>Total Skenario</div>
<div style='font-family:Sora; font-size:1.8rem; font-weight:800; color:var(--primary);'>15</div>
</div>
<div>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase; margin-bottom:4px;'>Total Eksperimen</div>
<div style='font-family:Sora; font-size:1.8rem; font-weight:800; color:var(--primary);'>30</div>
</div>
<div>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase; margin-bottom:4px;'>Best Model</div>
<div style='font-family:Sora; font-size:0.95rem; font-weight:800; color:var(--primary); margin-top:8px;'>NB + TF-IDF</div>
</div>
<div>
<div style='font-size:0.65rem; color:var(--text-muted); text-transform:uppercase; margin-bottom:4px;'>Best Accuracy</div>
<div style='font-family:Sora; font-size:1.8rem; font-weight:800; color:var(--primary);'>99.20%</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Insight Cards ────────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🔑 Temuan Utama Penelitian</div>
</div>
""", unsafe_allow_html=True)

    for insight in FINAL_INSIGHTS:
        st.markdown(f"""
<div class='card' style='border-left:4px solid {insight["color"]}; margin-bottom:16px;'>
<div style='display:flex; gap:16px; align-items:flex-start;'>
<div style='font-size:2rem; min-width:40px;'>{insight["icon"]}</div>
<div>
<div style='font-family:Sora; font-weight:700; font-size:1rem; color:{insight["color"]}; margin-bottom:6px;'>
{insight["title"]}
</div>
<div style='font-size:0.88rem; color:var(--text-secondary); line-height:1.7;'>{insight["text"]}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Final Comparison Table: All 15 × 2 ──────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>📊 Ringkasan 30 Eksperimen</div>
<div class='section-subtitle'>Accuracy, Recall, F1 — Original vs Augmented untuk seluruh 15 skenario</div>
</div>
""", unsafe_allow_html=True)

    table = []
    sorted_by_aug = sorted(SCENARIO_RESULTS, key=lambda x: x["aug_recall"], reverse=True)
    for rank, r in enumerate(sorted_by_aug, 1):
        delta_recall = r["aug_recall"] - r["orig_recall"]
        delta_str = f"+{delta_recall*100:.2f}%" if delta_recall >= 0 else f"{delta_recall*100:.2f}%"
        table.append({
            "Rank": rank,
            "Model": r["name"],
            "Kelompok": r["group"],
            "Acc Orig": f"{r['orig_acc']*100:.2f}%",
            "Recall Orig": f"{r['orig_recall']*100:.2f}%",
            "F1 Orig": f"{r['orig_f1']*100:.2f}%",
            "Acc Aug": f"{r['aug_acc']*100:.2f}%",
            "Recall Aug": f"{r['aug_recall']*100:.2f}%",
            "F1 Aug": f"{r['aug_f1']*100:.2f}%",
            "Δ Recall": delta_str,
        })
    df_final = pd.DataFrame(table)
    st.dataframe(df_final, use_container_width=True, hide_index=True)

    # ── Recommendations ──────────────────────────────────────────
    st.markdown("""
<div class='section-header'>
<div class='section-title'>🎯 Rekomendasi untuk Praktisi</div>
</div>
""", unsafe_allow_html=True)

    recs = [
        {
            "title": "Untuk Produksi (Akurasi & Efisiensi Tinggi)",
            "model": "NB + TF-IDF + Augmented + ROS",
            "reason": "Akurasi tertinggi (99.20%), waktu inferensi sangat cepat, tidak memerlukan GPU, mudah diinterpretasi.",
            "icon": "🏭",
        },
        {
            "title": "Untuk Kasus Recall-Critical (Minoritas Penting)",
            "model": "NB + TF-IDF + Augmented + ROS",
            "reason": "Recall tertinggi (97.78%). Paling direkomendasikan ketika TIDAK BOLEH ada query HORTICULTURE yang terlewat.",
            "icon": "🎯",
        },
        {
            "title": "Untuk Aplikasi Deep Learning / Transfer Learning",
            "model": "DistilBERT Fine-Tuning + Augmented",
            "reason": "Model Transformer terbaik. Cocok untuk aplikasi yang membutuhkan pemahaman kontekstual dan dapat di-deploy di cloud.",
            "icon": "🤖",
        },
        {
            "title": "Untuk Resource Terbatas (CPU Only, RAM < 4GB)",
            "model": "NB + BoW atau NB + TF-IDF (Original)",
            "reason": "Tidak memerlukan embedding model besar. Kecil, cepat, dan masih memberikan akurasi >97%.",
            "icon": "💡",
        },
    ]

    c1, c2 = st.columns(2)
    for i, rec in enumerate(recs):
        col = c1 if i % 2 == 0 else c2
        with col:
            st.markdown(f"""
<div class='card' style='margin-bottom:12px;'>
<div style='font-size:1.5rem; margin-bottom:8px;'>{rec['icon']}</div>
<div style='font-family:Sora; font-weight:700; font-size:0.9rem; margin-bottom:4px;'>{rec['title']}</div>
<div style='background:rgba(27,94,32,0.06); border-radius:6px; padding:8px; margin-bottom:8px;'>
<span style='font-size:0.75rem; font-weight:700; color:var(--primary);'>✅ {rec['model']}</span>
</div>
<div style='font-size:0.8rem; color:var(--text-secondary); line-height:1.6;'>{rec['reason']}</div>
</div>
""", unsafe_allow_html=True)
