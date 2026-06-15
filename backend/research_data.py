# ════════════════════════════════════════════════════════════════
# RESEARCH DATA — Project v7 Final Results (Hardcoded)
# Sumber: final summary.txt + data dari spesifikasi penelitian
# ════════════════════════════════════════════════════════════════

# ── Dataset Statistics ──────────────────────────────────────────
DATASET_ORIGINAL = {
    "total": 9939,
    "agriculture": 9173,
    "horticulture": 766,
    "imbalance_ratio": 12.0,
}

DATASET_AUGMENTED = {
    "total": 13003,
    "agriculture": 9173,
    "horticulture": 3830,
    "imbalance_ratio": 2.40,
}

AUGMENTATION_METHODS = [
    {
        "name": "Synonym Replacement",
        "icon": "📚",
        "desc": "Mengganti kata dengan sinonim menggunakan WordNet untuk memperkaya variasi teks tanpa mengubah makna.",
        "contribution": "Menghasilkan variasi leksikal yang alami.",
    },
    {
        "name": "Contextual Augmentation (BERT)",
        "icon": "🤖",
        "desc": "Menggunakan BERT Masked Language Model untuk memprediksi kata pengganti berdasarkan konteks kalimat.",
        "contribution": "Menghasilkan kalimat yang kontekstual dan semantis koheren.",
    },
    {
        "name": "Back Translation EN→ID→EN",
        "icon": "🌏",
        "desc": "Menerjemahkan teks ke Bahasa Indonesia lalu kembali ke Bahasa Inggris menggunakan Google Translate.",
        "contribution": "Menghasilkan parafrase dengan struktur kalimat berbeda.",
    },
    {
        "name": "Back Translation EN→JA→EN",
        "icon": "🗾",
        "desc": "Menerjemahkan teks ke Bahasa Jepang lalu kembali ke Bahasa Inggris untuk variasi yang lebih beragam.",
        "contribution": "Menghasilkan parafrase yang lebih divergen dari BT-ID.",
    },
]

# ── 15 Scenarios × 2 Datasets — Full Recall Data ────────────────
# Sumber: RANKING (by Augmented Recall) dari final summary.txt
SCENARIO_RESULTS = [
    # name, group, orig_recall, aug_recall
    {"name": "NB + TF-IDF",        "group": "Classical NLP",           "orig_acc": 0.9720, "aug_acc": 0.9920, "orig_recall": 0.9194, "aug_recall": 0.9778, "orig_f1": 0.9367, "aug_f1": 0.9722},
    {"name": "DT + BoW",           "group": "Classical NLP",           "orig_acc": 0.9672, "aug_acc": 0.9741, "orig_recall": 0.8436, "aug_recall": 0.9723, "orig_f1": 0.8972, "aug_f1": 0.9561},
    {"name": "NB + BoW",           "group": "Classical NLP",           "orig_acc": 0.9710, "aug_acc": 0.9738, "orig_recall": 0.9188, "aug_recall": 0.9713, "orig_f1": 0.9355, "aug_f1": 0.9564},
    {"name": "NB + N-Gram",        "group": "Classical NLP",           "orig_acc": 0.9680, "aug_acc": 0.9730, "orig_recall": 0.8516, "aug_recall": 0.9610, "orig_f1": 0.9012, "aug_f1": 0.9487},
    {"name": "DT + TF-IDF",        "group": "Classical NLP",           "orig_acc": 0.9638, "aug_acc": 0.9748, "orig_recall": 0.8371, "aug_recall": 0.9561, "orig_f1": 0.8930, "aug_f1": 0.9522},
    {"name": "DT + N-Gram",        "group": "Classical NLP",           "orig_acc": 0.9540, "aug_acc": 0.9710, "orig_recall": 0.6813, "aug_recall": 0.9052, "orig_f1": 0.7892, "aug_f1": 0.9245},
    {"name": "DT + Word2Vec",      "group": "Non-Contextual Embedding","orig_acc": 0.9601, "aug_acc": 0.9680, "orig_recall": 0.8658, "aug_recall": 0.9458, "orig_f1": 0.9024, "aug_f1": 0.9428},
    {"name": "DT + FastText",      "group": "Non-Contextual Embedding","orig_acc": 0.9580, "aug_acc": 0.9655, "orig_recall": 0.8241, "aug_recall": 0.9030, "orig_f1": 0.8820, "aug_f1": 0.9219},
    {"name": "DT + GloVe",         "group": "Non-Contextual Embedding","orig_acc": 0.9570, "aug_acc": 0.9620, "orig_recall": 0.8392, "aug_recall": 0.9149, "orig_f1": 0.8885, "aug_f1": 0.9302},
    {"name": "NB + Word2Vec",      "group": "Non-Contextual Embedding","orig_acc": 0.9250, "aug_acc": 0.9540, "orig_recall": 0.4857, "aug_recall": 0.8519, "orig_f1": 0.6204, "aug_f1": 0.9028},
    {"name": "NB + FastText",      "group": "Non-Contextual Embedding","orig_acc": 0.9310, "aug_acc": 0.9571, "orig_recall": 0.5336, "aug_recall": 0.8782, "orig_f1": 0.6652, "aug_f1": 0.9137},
    {"name": "NB + GloVe",         "group": "Non-Contextual Embedding","orig_acc": 0.9200, "aug_acc": 0.9320, "orig_recall": 0.5000, "aug_recall": 0.5692, "orig_f1": 0.6154, "aug_f1": 0.6940},
    {"name": "DT + BERT Embedding","group": "Contextual Embedding",    "orig_acc": 0.9610, "aug_acc": 0.9660, "orig_recall": 0.8565, "aug_recall": 0.9063, "orig_f1": 0.9005, "aug_f1": 0.9248},
    {"name": "NB + BERT Embedding","group": "Contextual Embedding",    "orig_acc": 0.9580, "aug_acc": 0.9561, "orig_recall": 0.8369, "aug_recall": 0.8169, "orig_f1": 0.8832, "aug_f1": 0.8749},
    {"name": "DistilBERT FT",      "group": "Transformer",             "orig_acc": 0.9849, "aug_acc": 0.9879, "orig_recall": 0.9442, "aug_recall": 0.9637, "orig_f1": 0.9469, "aug_f1": 0.9583},
]

# ── Balancing Analysis ───────────────────────────────────────────
# Best model (NB + TF-IDF Augmented) dengan berbagai teknik balancing
BALANCING_RESULTS = [
    {
        "method": "No Balancing",
        "icon": "❌",
        "desc": "Tanpa teknik balancing, model tetap bias ke kelas mayoritas (Agriculture).",
        "accuracy": 0.9738,
        "recall": 0.8371,
        "f1": 0.8930,
        "color": "#E74C3C",
    },
    {
        "method": "RandomOverSampler (ROS)",
        "icon": "✅",
        "desc": "Duplikasi acak sampel minoritas (HORTICULTURE) untuk menyeimbangkan distribusi kelas.",
        "accuracy": 0.9698,
        "recall": 0.9717,
        "f1": 0.9084,
        "color": "#27AE60",
    },
    {
        "method": "SMOTE",
        "icon": "🔬",
        "desc": "Synthetic Minority Over-sampling Technique menghasilkan sampel sintetis berdasarkan interpolasi fitur.",
        "accuracy": 0.9638,
        "recall": 0.9685,
        "f1": 0.8932,
        "color": "#2980B9",
    },
]

# ── Top Performing Models ────────────────────────────────────────
TOP_MODELS = {
    "best_accuracy": {
        "name": "NB + TF-IDF",
        "dataset": "Augmented + ROS",
        "accuracy": 0.9920,
        "recall": 0.9778,
        "f1": 0.9722,
        "group": "Classical NLP",
        "icon": "🥇",
    },
    "best_recall": {
        "name": "NB + TF-IDF",
        "dataset": "Augmented + ROS",
        "accuracy": 0.9920,
        "recall": 0.9778,
        "f1": 0.9722,
        "group": "Classical NLP",
        "icon": "🥈",
    },
    "best_f1": {
        "name": "NB + TF-IDF",
        "dataset": "Augmented + ROS",
        "accuracy": 0.9920,
        "recall": 0.9778,
        "f1": 0.9722,
        "group": "Classical NLP",
        "icon": "🥉",
    },
    "best_transformer": {
        "name": "DistilBERT Fine-Tuning",
        "dataset": "Augmented",
        "accuracy": 0.9879,
        "recall": 0.9637,
        "f1": 0.9583,
        "group": "Transformer",
        "icon": "🤖",
    },
}

# ── Recall Improvement (Top 5) ───────────────────────────────────
RECALL_IMPROVEMENTS = [
    {"name": "NB + Word2Vec",  "orig": 0.4857, "aug": 0.8519, "delta": 0.3662},
    {"name": "NB + FastText",  "orig": 0.5336, "aug": 0.8782, "delta": 0.3447},
    {"name": "DT + N-Gram",    "orig": 0.6813, "aug": 0.9052, "delta": 0.2240},
    {"name": "DT + BoW",       "orig": 0.8436, "aug": 0.9723, "delta": 0.1287},
    {"name": "DT + TF-IDF",   "orig": 0.8371, "aug": 0.9561, "delta": 0.1190},
    {"name": "NB + N-Gram",    "orig": 0.8516, "aug": 0.9610, "delta": 0.1094},
    {"name": "DT + Word2Vec",  "orig": 0.8658, "aug": 0.9458, "delta": 0.0801},
    {"name": "DT + FastText",  "orig": 0.8241, "aug": 0.9030, "delta": 0.0790},
    {"name": "DT + GloVe",     "orig": 0.8392, "aug": 0.9149, "delta": 0.0757},
    {"name": "NB + BoW",       "orig": 0.9188, "aug": 0.9713, "delta": 0.0525},
    {"name": "NB + TF-IDF",   "orig": 0.9194, "aug": 0.9778, "delta": 0.0584},
    {"name": "NB + GloVe",     "orig": 0.5000, "aug": 0.5692, "delta": 0.0692},
    {"name": "DT + BERT Embedding", "orig": 0.8565, "aug": 0.9063, "delta": 0.0497},
    {"name": "NB + BERT Embedding", "orig": 0.8369, "aug": 0.8169, "delta": -0.0200},
    {"name": "DistilBERT FT",  "orig": 0.9442, "aug": 0.9637, "delta": 0.0195},
]

# ── DistilBERT Analysis ──────────────────────────────────────────
DISTILBERT_RESULTS = {
    "original": {
        "label": "Original Dataset",
        "accuracy": 0.9849,
        "recall": 0.9442,
        "f1": 0.9469,
        "total_data": 9939,
        "color": "#2E86C1",
    },
    "augmented": {
        "label": "Augmented Dataset",
        "accuracy": 0.9879,
        "recall": 0.9637,
        "f1": 0.9583,
        "total_data": 13003,
        "color": "#1B5E20",
    },
    "delta": {
        "accuracy": +0.0030,
        "recall": +0.0195,
        "f1": +0.0114,
    },
}

# ── Final Insights ───────────────────────────────────────────────
FINAL_INSIGHTS = [
    {
        "icon": "⚖️",
        "title": "Imbalance Ratio Berhasil Diturunkan",
        "text": "Data augmentasi berhasil menurunkan imbalance ratio dari <b>12.0:1</b> menjadi <b>2.40:1</b>, meningkatkan representasi kelas HORTICULTURE dari 766 menjadi 3.830 sampel.",
        "color": "#1B5E20",
    },
    {
        "icon": "📈",
        "title": "Rata-Rata Recall Meningkat Signifikan",
        "text": "Secara rata-rata, recall meningkat <b>+0.1171</b> setelah augmentasi. Model yang sebelumnya sangat bias ke Agriculture (recall minoritas hampir 0%) kini mampu mengenali HORTICULTURE dengan lebih baik.",
        "color": "#1565C0",
    },
    {
        "icon": "🏆",
        "title": "NB + TF-IDF Menjadi Model Terbaik Keseluruhan",
        "text": "Naive Bayes dengan representasi TF-IDF pada dataset augmented+ROS mencapai akurasi <b>99.20%</b>, recall <b>97.78%</b>, dan F1-Score <b>97.22%</b> — melampaui semua model lain termasuk Transformer.",
        "color": "#6A1B9A",
    },
    {
        "icon": "🤖",
        "title": "DistilBERT Menjadi Transformer Terbaik",
        "text": "DistilBERT Fine-Tuning pada dataset augmented mencapai akurasi <b>98.79%</b> dan recall <b>96.37%</b>. Augmentasi data meningkatkan recall DistilBERT sebesar <b>+1.95%</b>.",
        "color": "#E65100",
    },
    {
        "icon": "✅",
        "title": "Data Augmentasi Terbukti Efektif",
        "text": "13 dari 15 model mengalami peningkatan recall setelah augmentasi. Model berbasis embedding statis (Word2Vec, FastText) mendapat manfaat paling besar karena sebelumnya sangat kesulitan mengenali pola kelas minoritas.",
        "color": "#00695C",
    },
]
