# ════════════════════════════════════════════════════════════════
# DATA LOADER — Dataset loading, cleaning, preprocessing
# ════════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import re
import streamlit as st
import nltk
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

STOP_WORDS = set(stopwords.words("english"))
TARGET_CLASSES = ["AGRICULTURE", "HORTICULTURE"]
N_ROWS = 2000


def clean_text(text: str) -> str:
    """Full text cleaning pipeline."""
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return " ".join([t for t in text.split() if t not in STOP_WORDS and len(t) > 1])


def preprocessing_steps(text: str) -> dict:
    """Step-by-step preprocessing for demonstration."""
    step0 = str(text)
    step1 = step0.lower()
    step2 = re.sub(r"[^a-z\s]", " ", step1)
    step3 = re.sub(r"\s+", " ", step2).strip()
    tokens = step3.split()
    step4 = " ".join([t for t in tokens if t not in STOP_WORDS and len(t) > 1])
    return {
        "original": step0,
        "lowercase": step1,
        "no_punct": step2,
        "normalized": step3,
        "clean": step4
    }


@st.cache_data(show_spinner=False)
def load_data(path: str, nrows: int = N_ROWS):
    """Load CSV data with caching."""
    import os
    if not os.path.exists(path):
        return None
    return pd.read_csv(path, nrows=nrows, encoding="utf-8", on_bad_lines="skip")


def prepare_data(df: pd.DataFrame):
    """Prepare dataset: filter classes, clean text, encode labels."""
    import os
    import joblib
    
    df2 = df[["QueryText", "Sector"]].dropna()
    df2 = df2[df2["Sector"].isin(TARGET_CLASSES)].copy()
    df2["Sector"] = df2["Sector"].str.strip().str.upper()
    df2["clean_text"] = df2["QueryText"].apply(clean_text)
    
    le_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "label_encoder.pkl")
    if os.path.exists(le_path):
        try:
            le = joblib.load(le_path)
            df2["label"] = le.transform(df2["Sector"])
        except Exception:
            le = LabelEncoder()
            df2["label"] = le.fit_transform(df2["Sector"])
    else:
        le = LabelEncoder()
        df2["label"] = le.fit_transform(df2["Sector"])
        
    return df2, le


def get_text_statistics(df: pd.DataFrame) -> dict:
    """Compute text statistics for dataset analysis."""
    raw_lens = df["QueryText"].astype(str).apply(lambda x: len(x.split()))
    clean_lens = df["clean_text"].astype(str).apply(lambda x: len(x.split()))
    char_lens = df["QueryText"].astype(str).apply(len)

    return {
        "raw_mean_tokens": raw_lens.mean(),
        "raw_median_tokens": raw_lens.median(),
        "raw_max_tokens": raw_lens.max(),
        "raw_min_tokens": raw_lens.min(),
        "clean_mean_tokens": clean_lens.mean(),
        "clean_median_tokens": clean_lens.median(),
        "clean_max_tokens": clean_lens.max(),
        "clean_min_tokens": clean_lens.min(),
        "mean_chars": char_lens.mean(),
        "total_rows": len(df),
        "agri_count": int((df["Sector"] == "AGRICULTURE").sum()),
        "horti_count": int((df["Sector"] == "HORTICULTURE").sum()),
    }


def get_word_frequency(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    """Get top word frequencies from clean text."""
    from collections import Counter
    all_words = " ".join(df["clean_text"].tolist()).split()
    freq = Counter(all_words).most_common(top_n)
    return pd.DataFrame(freq, columns=["Word", "Frequency"])
