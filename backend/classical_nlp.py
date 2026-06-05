import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


@st.cache_resource(show_spinner=False)
def _get_cached_bow(X_train_list, X_test_list, max_features=5000):
    vec = CountVectorizer(
        ngram_range=(1, 1),
        max_features=max_features,
        min_df=2
    )
    Xtr = vec.fit_transform(X_train_list)
    Xte = vec.transform(X_test_list)
    return vec, Xtr, Xte


def extract_bow(X_train, X_test, max_features=5000):
    """Extract Bag of Words features."""
    return _get_cached_bow(X_train.tolist(), X_test.tolist(), max_features)


@st.cache_resource(show_spinner=False)
def _get_cached_tfidf(X_train_list, X_test_list, max_features=5000):
    vec = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=max_features,
        sublinear_tf=True,
        min_df=2
    )
    Xtr = vec.fit_transform(X_train_list)
    Xte = vec.transform(X_test_list)
    return vec, Xtr, Xte


def extract_tfidf(X_train, X_test, max_features=5000):
    """Extract TF-IDF features."""
    return _get_cached_tfidf(X_train.tolist(), X_test.tolist(), max_features)


@st.cache_resource(show_spinner=False)
def _get_cached_ngram(X_train_list, X_test_list, max_features=5000):
    vec = CountVectorizer(
        ngram_range=(2, 3),
        max_features=max_features,
        min_df=2
    )
    Xtr = vec.fit_transform(X_train_list)
    Xte = vec.transform(X_test_list)
    return vec, Xtr, Xte


def extract_ngram(X_train, X_test, max_features=5000):
    """Extract N-Gram (bigram + trigram) features."""
    return _get_cached_ngram(X_train.tolist(), X_test.tolist(), max_features)


def get_feature_info(vectorizer) -> dict:
    """Get information about a fitted vectorizer."""
    features = vectorizer.get_feature_names_out()
    return {
        "vocab_size": len(features),
        "ngram_range": vectorizer.ngram_range,
        "max_features": vectorizer.max_features,
        "features": features
    }


def get_top_tokens(vectorizer, X_matrix, top_n=20):
    """Get top tokens by frequency from transformed matrix."""
    features = vectorizer.get_feature_names_out()
    freq_arr = np.asarray(X_matrix.sum(axis=0)).flatten()
    top_idx = freq_arr.argsort()[::-1][:top_n]
    top_tokens = [features[i] for i in top_idx]
    top_freqs = [float(freq_arr[i]) for i in top_idx]
    return top_tokens, top_freqs


def get_class_top_tokens(vectorizer, X_matrix, y, class_idx, top_n=10):
    """Get top tokens for a specific class."""
    features = vectorizer.get_feature_names_out()
    mask = (y == class_idx)

    if hasattr(X_matrix, 'toarray'):
        class_matrix = X_matrix[mask]
    else:
        class_matrix = X_matrix[mask]

    freq_arr = np.asarray(class_matrix.sum(axis=0)).flatten()
    top_idx = freq_arr.argsort()[::-1][:top_n]
    tokens = [features[i] for i in top_idx]
    freqs = [float(freq_arr[i]) for i in top_idx]
    return tokens, freqs


CLASSICAL_EXPLANATIONS = {
    "bow": {
        "title": "📦 Bag of Words (BoW)",
        "desc": "Representasi teks paling sederhana. Menghitung frekuensi kemunculan setiap kata dalam dokumen, mengabaikan urutan dan konteks.",
        "formula": "BoW(d) = [count(w₁), count(w₂), ..., count(wₙ)]",
        "pros": ["Mudah diimplementasi", "Cepat diproses", "Baseline yang baik"],
        "cons": ["Tidak menangkap urutan kata", "Sparse matrix (banyak nol)", "Tidak ada informasi semantik"]
    },
    "tfidf": {
        "title": "⚡ TF-IDF (Term Frequency–Inverse Document Frequency)",
        "desc": "Metode pembobotan yang mengukur pentingnya kata berdasarkan frekuensi dalam dokumen (TF) dan keunikan di seluruh corpus (IDF).",
        "formula": "TF-IDF(t,d) = TF(t,d) × log(N / DF(t))",
        "pros": ["Membobot kata penting lebih tinggi", "Mengurangi pengaruh common words", "Lebih informatif dari BoW"],
        "cons": ["Masih sparse representation", "Tidak menangkap konteks", "Kehilangan urutan kata"]
    },
    "ngram": {
        "title": "🔗 N-Gram",
        "desc": "Menangkap urutan N kata berurutan (bigram, trigram) untuk mempertahankan sebagian konteks lokal dari teks.",
        "formula": "Bigram: (wᵢ, wᵢ₊₁), Trigram: (wᵢ, wᵢ₊₁, wᵢ₊₂)",
        "pros": ["Menangkap konteks lokal", "Menangkap frasa penting", "Lebih kaya dari unigram"],
        "cons": ["Vocabulary sangat besar", "Lebih sparse dari BoW", "Curse of dimensionality"]
    }
}
