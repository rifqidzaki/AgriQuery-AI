# Dashboard NLP Pertanian v6.0 (Final Research Edition) 🌾

Aplikasi berbasis web (Streamlit) yang menyajikan hasil evaluasi dan perbandingan 13 metode ekstraksi fitur dan pemodelan klasifikasi teks (NLP) pada domain pertanian (klasifikasi query Agriculture vs Horticulture). 

Penelitian ini membandingkan teknik representasi fitur **Klasik** (BoW, TF-IDF, N-Gram) dengan **Modern/Semantic** (Word2Vec, GloVe, BERT) dan **Transformer** (DistilBERT Fine-Tuning).

---

## 🌟 Fitur Utama (v6.0)

Dashboard ini telah dirombak total untuk kebutuhan sidang/presentasi penelitian:

1. **No-Training Loading (Speed Optimized)**
   - Semua 13 model langsung dimuat dari file `.pkl` yang sudah dilatih (pre-trained).
   - Waktu loading dari awal hanya membutuhkan **< 30 detik**.

2. **Integrasi 13 Kombinasi Model**
   - **Classical NLP:** DT+BoW, NB+BoW, DT+TF-IDF, NB+TF-IDF, DT+N-Gram, NB+N-Gram
   - **Semantic Embedding:** DT+Word2Vec, NB+Word2Vec, DT+GloVe, NB+GloVe
   - **Contextual Embedding:** DT+BERT, NB+BERT
   - **Transformer:** DistilBERT Fine-Tuning (End-to-End)

3. **9 Halaman Analisis Komprehensif**
   - **Overview:** Ringkasan hasil penelitian dan KPI performa terbaik.
   - **Dataset Overview:** Distribusi kelas, top words, statistik panjang teks.
   - **Preprocessing (BARU):** Visualisasi pipeline pembersihan teks interaktif (Raw → Case Folding → Punctuation → Stopword → Clean).
   - **Feature Extraction:** Penjelasan terpusat untuk ketiga jenis ekstraksi fitur (Classical, Semantic, Contextual).
   - **Training & Evaluation:** Detail Confusion Matrix dan Classification Report per model.
   - **Model Comparison:** Tabel ranking 13 model dan visualisasi Radar Chart.
   - **Error Analysis (BARU):** Komparasi Error Rate, detail False Positive / False Negative, dan *Auto-Generated Insights*.
   - **Interactive Prediction:** Fitur untuk mencoba prediksi query secara real-time dengan semua model (termasuk DistilBERT).
   - **About Project:** Ringkasan latar belakang proyek.

4. **UI/UX Premium & Modern**
   - Palet warna eksklusif "Agriculture Green" (`#1B5E20`, `#2E7D32`, `#66BB6A`).
   - *Card-based layout*, transisi halus, dan tipografi modern (Sora, Inter, JetBrains Mono).

---

## ⚙️ Persyaratan Sistem

- Python 3.9 - 3.11
- Minimal 4GB RAM (Direkomendasikan 8GB karena ada load Word2Vec, GloVe, BERT, dan DistilBERT).

---

## 🛠️ Cara Menjalankan Aplikasi

1. Buka Terminal atau Command Prompt di folder proyek ini (`New Dasboard`).
2. Aktifkan virtual environment:
   ```bash
   # Di Windows
   .\.venv\Scripts\activate
   ```
3. Install dependensi (jika belum):
   ```bash
   pip install -r requirements.txt
   ```
4. Pastikan dataset `query_agg.csv` berada di root folder.
5. Jalankan Streamlit:
   ```bash
   streamlit run app.py
   ```
6. Aplikasi akan terbuka di browser (biasanya `http://localhost:8501`).

---

## 📁 Struktur Direktori Penting

```
New Dasboard/
├── app.py                     # Entry point aplikasi Streamlit
├── styles.py                  # Konfigurasi CSS/UI Premium
├── README.md                  # Dokumentasi proyek
├── query_agg.csv              # Dataset mentah
│
├── backend/                   # Logika backend
│   ├── data_loader.py         # Memuat & preprocessing data
│   ├── model_loader.py        # Memuat 12 model Sklearn
│   ├── transformer_inference.py # Inferensi DistilBERT
│   └── classical_nlp.py       # Penjelasan teks fitur klasik
│
├── components/                # Komponen UI
│   ├── charts.py              # Custom Plotly charts
│   └── sidebar.py             # Navigasi kiri
│
├── pages/                     # Berisi 9 halaman UI (p01 - p09)
│
├── models/                    # Folder 12 pre-trained model Sklearn (.pkl)
│                              # & Vectorizer / Word2Vec / GloVe
│
└── transformer_model/         # Folder model DistilBERT (config, model.safetensors, dll)
```

---

## 📝 Catatan Penting untuk GitHub

Karena batasan ukuran file di GitHub (Max 100MB), file-file berikut **TIDAK DIUNGGAH** ke GitHub dan telah dimasukkan ke dalam `.gitignore`:
- `query_agg.csv` (990MB)
- `models/word2vec_model.bin` (Jika >100MB)
- `models/glove.6B.50d.txt` (400MB)
- `transformer_model/model.safetensors` (268MB)

**PENTING**: Jika akan dipindahkan ke komputer dosen atau komputer lain, folder `models/` dan `transformer_model/` harus disalin utuh menggunakan Flashdisk atau Google Drive, BUKAN ditarik dari GitHub.
