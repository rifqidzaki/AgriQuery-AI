# AgriMind AI — NLP Analytics Platform

![AgriMind AI Version](https://img.shields.io/badge/Version-v5.0_Research_Edition-emerald)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

**AgriMind AI** adalah platform analitik Natural Language Processing (NLP) tingkat lanjut yang dibangun untuk membandingkan kinerja **NLP Klasik** (BoW, TF-IDF, N-Gram) dengan **Embedding Modern** (Word2Vec, GloVe, BERT) dalam melakukan klasifikasi query pertanian. Dashboard ini membandingkan dua algoritma Machine Learning: **Decision Tree** dan **Naive Bayes**.

---

## ✨ Fitur Utama

- **🚀 Real-time Inference:** Lakukan prediksi klasifikasi query teks secara instan dan lihat tingkat keyakinan (confidence score) dari berbagai kombinasi model.
- **🏆 Model Comparison:** Bandingkan performa 12 kombinasi model dan representasi fitur secara berdampingan.
- **💡 Explainable AI (XAI):** Pahami bagaimana model mengambil keputusan menggunakan analisis Feature Importance dan Keyword Contribution.
- **🔍 Error Analysis:** Analisis dan temukan pola dari kesalahan klasifikasi model melalui visualisasi Confusion Matrix yang interaktif.
- **📊 Dataset Explorer:** Eksplorasi dataset Kisan Query secara visual, lengkap dengan simulasi pipeline NLP interaktif (Stopword removal, tokenization).

## 🛠️ Teknologi yang Digunakan
- **Core:** Python, Streamlit, Pandas, NumPy
- **Visualisasi:** Plotly
- **Machine Learning:** Scikit-learn
- **NLP Klasik:** NLTK
- **NLP Modern:** Gensim (Word2Vec, GloVe), Sentence-Transformers (BERT)

---

## ⚙️ Cara Instalasi & Menjalankan Dashboard

1. **Buka Terminal / Command Prompt** dan masuk ke dalam direktori proyek ini:
   ```bash
   cd "d:\SEMESTER 6\Pemrosesan Bahasa Alami (NLP)\New Dasboard"
   ```

2. **Buat Virtual Environment (Sangat Direkomendasikan)**
   ```bash
   python -m venv .venv
   
   # Aktivasi di Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   
   # Aktivasi di Windows (Command Prompt):
   .\.venv\Scripts\activate.bat
   ```

3. **Install Dependensi**
   Pastikan Anda menginstal semua dependensi yang diperlukan.
   ```bash
   pip install -r requirements.txt
   ```
   *(Jika file `requirements.txt` belum lengkap, Anda bisa menginstal paket-paket ini secara manual: `pip install streamlit pandas numpy plotly scikit-learn nltk gensim sentence-transformers transformers`)*

4. **Pastikan File Model Lokal Tersedia (Penting)**
   Dashboard ini dioptimalkan untuk memuat model dari Google Colab Anda agar tidak perlu mengunduh data besar. Pastikan struktur berikut tersedia:
   - `models/` berisi file `model_dt__*.pkl`, `model_nb__*.pkl`, `vectorizer_*.pkl`, dan `label_encoder.pkl`.
   - `models/` atau `embeddings/` berisi embedding lokal seperti `word2vec_model.bin` dan `glove.6B.50d.txt`.
   
   *Catatan: Jika file tidak ditemukan, sistem memiliki sistem fallback yang akan melatih ulang model secara otomatis (bisa memakan waktu beberapa menit).*

5. **Jalankan Aplikasi Streamlit**
   ```bash
   streamlit run app.py
   ```

6. **Buka di Browser**
   Buka URL `http://localhost:8501` di web browser Anda.

---

## 📚 Struktur Direktori
- `app.py`: File utama untuk menjalankan aplikasi Streamlit.
- `backend/`: Script logika utama untuk ekstraksi fitur, pemuatan model, pelatihan, dan metrik NLP.
- `components/`: Kumpulan modul komponen UI yang dapat digunakan ulang (kartu, grafik, sidebar).
- `pages/`: Halaman-halaman terpisah untuk setiap fitur pada dashboard (Overview, Dataset, Model Training, dsb.).
- `models/`: Penyimpanan untuk file `.pkl` dan model NLP (*pretrained*).
- `styles.py`: Konfigurasi CSS terpusat untuk tema dan UI komponen.

---

**© 2026 AgriMind AI — NLP Research Edition**
