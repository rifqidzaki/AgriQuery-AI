# ════════════════════════════════════════════════════════════════
# MODERN NLP — Word2Vec, GloVe, BERT Embeddings
# ════════════════════════════════════════════════════════════════

import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings('ignore')


@st.cache_resource(show_spinner=False)
def load_word2vec_model():
    """Load pretrained Word2Vec model via gensim."""
    """Load pretrained Word2Vec model via gensim or local models directory."""
    import os
    from gensim.models import Word2Vec, KeyedVectors
    
    # Try local path first
    local_paths = [
        "models/word2vec_model.bin",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "word2vec_model.bin")
    ]
    for lp in local_paths:
        if os.path.exists(lp):
            try:
                # Try loading as full Word2Vec model
                w2v = Word2Vec.load(lp)
                if hasattr(w2v, "wv"):
                    return w2v.wv
                return w2v
            except Exception:
                try:
                    # Try loading as raw keyed vectors
                    return KeyedVectors.load_word2vec_format(lp, binary=True)
                except Exception:
                    pass
                    
    # Fallback to gensim downloader
    import gensim.downloader as api
    model = api.load("word2vec-google-news-300")
    return model


@st.cache_resource(show_spinner=False)
def load_glove_model():
    """Load pretrained GloVe model via gensim or local models directory."""
    import os
    from gensim.models import KeyedVectors
    
    # Try local path first
    local_paths = [
        "models/glove.6B.50d.txt",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "glove.6B.50d.txt")
    ]
    for lp in local_paths:
        if os.path.exists(lp):
            try:
                # Load standard GloVe txt format (no header)
                return KeyedVectors.load_word2vec_format(lp, binary=False, no_header=True)
            except Exception:
                pass
                
    # Fallback to gensim downloader
    import gensim.downloader as api
    model = api.load("glove-wiki-gigaword-100")
    return model


@st.cache_resource(show_spinner=False)
def load_bert_model():
    """Load pretrained BERT sentence transformer."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


def _average_word_vectors(texts, model, dim):
    """Average word vectors for each text."""
    embeddings = []
    for text in texts:
        words = str(text).lower().split()
        word_vecs = []
        for w in words:
            if w in model:
                word_vecs.append(model[w])
        if word_vecs:
            embeddings.append(np.mean(word_vecs, axis=0))
        else:
            embeddings.append(np.zeros(dim))
    return np.array(embeddings)


@st.cache_resource(show_spinner=False)
def _get_cached_w2v_embeddings(X_train_list, X_test_list):
    model = load_word2vec_model()
    dim = getattr(model, "vector_size", 300)
    Xtr = _average_word_vectors(X_train_list, model, dim)
    Xte = _average_word_vectors(X_test_list, model, dim)
    return model, Xtr, Xte, dim


def extract_word2vec(X_train, X_test, progress_callback=None):
    """Extract Word2Vec embeddings using pretrained model."""
    if progress_callback:
        progress_callback("Loading Word2Vec model...")
    return _get_cached_w2v_embeddings(X_train.tolist(), X_test.tolist())


@st.cache_resource(show_spinner=False)
def _get_cached_glove_embeddings(X_train_list, X_test_list):
    model = load_glove_model()
    dim = getattr(model, "vector_size", 100)
    Xtr = _average_word_vectors(X_train_list, model, dim)
    Xte = _average_word_vectors(X_test_list, model, dim)
    return model, Xtr, Xte, dim


def extract_glove(X_train, X_test, progress_callback=None):
    """Extract GloVe embeddings using pretrained model."""
    if progress_callback:
        progress_callback("Loading GloVe model...")
    return _get_cached_glove_embeddings(X_train.tolist(), X_test.tolist())


@st.cache_resource(show_spinner=False)
def _get_cached_bert_embeddings(X_train_list, X_test_list):
    model = load_bert_model()
    Xtr = model.encode(X_train_list, show_progress_bar=False, batch_size=64)
    Xte = model.encode(X_test_list, show_progress_bar=False, batch_size=64)
    dim = Xtr.shape[1]  # 384 for all-MiniLM-L6-v2
    return model, Xtr, Xte, dim


def extract_bert(X_train, X_test, progress_callback=None):
    """Extract BERT sentence embeddings using sentence-transformers."""
    if progress_callback:
        progress_callback("Loading BERT model (all-MiniLM-L6-v2)...")
    return _get_cached_bert_embeddings(X_train.tolist(), X_test.tolist())


def compute_similarity_demo(model, words, model_type="word2vec"):
    """Compute pairwise similarity between words for demonstration."""
    results = []
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            w1, w2 = words[i], words[j]
            try:
                if model_type == "bert":
                    emb = model.encode([w1, w2])
                    from numpy.linalg import norm
                    sim = float(np.dot(emb[0], emb[1]) / (norm(emb[0]) * norm(emb[1])))
                else:
                    if w1 in model and w2 in model:
                        sim = float(model.similarity(w1, w2))
                    else:
                        sim = None
                results.append({"Word 1": w1, "Word 2": w2, "Similarity": sim})
            except Exception:
                results.append({"Word 1": w1, "Word 2": w2, "Similarity": None})
    return results


MODERN_EXPLANATIONS = {
    "word2vec": {
        "title": "🧠 Word2Vec",
        "desc": "Model neural network yang mempelajari representasi vektor kata dari konteks. Menggunakan arsitektur Skip-gram atau CBOW untuk menangkap hubungan semantik antar kata.",
        "key_points": [
            "Dense vector (300 dimensi)",
            "Menangkap relasi semantik (king - man + woman = queen)",
            "Pretrained: Google News 300d (3 juta kata)",
            "Static embedding — satu kata = satu vektor tetap"
        ],
        "dim": 300,
        "model": "word2vec-google-news-300"
    },
    "glove": {
        "title": "🌐 GloVe (Global Vectors)",
        "desc": "Metode embedding yang menggabungkan matrix factorization global (seperti LSA) dengan konteks lokal (seperti Word2Vec). Menghasilkan representasi vektor yang menangkap statistik co-occurrence kata.",
        "key_points": [
            "Dense vector (100 dimensi)",
            "Berbasis global co-occurrence matrix",
            "Pretrained: Wikipedia + Gigaword (400K kata)",
            "Static embedding — konteks tidak mempengaruhi vektor"
        ],
        "dim": 100,
        "model": "glove-wiki-gigaword-100"
    },
    "bert": {
        "title": "🤖 BERT Embedding",
        "desc": "Bidirectional Encoder Representations from Transformers — model transformer yang memahami konteks bidirectional. Setiap kata mendapatkan vektor berbeda tergantung konteks kalimat.",
        "key_points": [
            "Dense vector (384 dimensi — MiniLM)",
            "Contextual embedding — vektor berubah sesuai konteks",
            "Self-attention mechanism untuk relasi antar kata",
            "Sentence-level encoding via pooling"
        ],
        "dim": 384,
        "model": "all-MiniLM-L6-v2"
    }
}

TRANSFORMER_EXPLANATION = {
    "self_attention": {
        "title": "🔍 Self-Attention Mechanism",
        "desc": "Setiap kata 'memperhatikan' semua kata lain dalam kalimat untuk memahami konteks. Attention score menentukan seberapa penting kata lain terhadap kata saat ini.",
        "formula": "Attention(Q,K,V) = softmax(QK^T / √d_k) × V"
    },
    "transformer_encoder": {
        "title": "⚙️ Transformer Encoder",
        "desc": "Terdiri dari Multi-Head Attention + Feed-Forward Network + Layer Normalization. Memproses seluruh input secara paralel (bukan sekuensial seperti RNN).",
        "components": ["Multi-Head Self-Attention", "Add & Layer Norm", "Feed-Forward Network", "Residual Connection"]
    },
    "contextual_vs_static": {
        "title": "🔄 Contextual vs Static Embedding",
        "desc": "Static (Word2Vec/GloVe): Kata 'bank' selalu punya vektor yang sama. Contextual (BERT): 'bank' di 'river bank' vs 'bank account' punya vektor berbeda."
    }
}
