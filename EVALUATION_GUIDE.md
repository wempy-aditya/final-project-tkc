# 📊 Panduan Evaluasi Sistem Multimodal RAG

## Overview

Script evaluasi yang telah ditingkatkan (`scripts/run_evaluation.py`) menyediakan pengukuran komprehensif untuk sistem RAG multimodal, mencakup metrik retrieval dan generation dengan skenario testing yang terstruktur.

---

## 🎯 Metrik yang Diukur

### **A. Retrieval Metrics**

#### 1. **Recall@K**
- **Definisi**: Persentase dokumen relevan yang berhasil ditemukan dalam top-K hasil
- **Formula**: `Recall@K = (Jumlah relevan di top-K) / (Total dokumen relevan)`
- **Interpretasi**: 
  - Nilai tinggi (>0.7) = Sistem bagus menemukan dokumen relevan
  - Nilai rendah (<0.3) = Banyak dokumen relevan yang terlewat

#### 2. **Precision@K**
- **Definisi**: Persentase hasil top-K yang benar-benar relevan
- **Formula**: `Precision@K = (Jumlah relevan di top-K) / K`
- **Interpretasi**:
  - Nilai tinggi (>0.7) = Hasil yang ditampilkan sangat akurat
  - Nilai rendah (<0.3) = Banyak hasil yang tidak relevan

#### 3. **Retrieval Latency**
- **Definisi**: Waktu yang dibutuhkan untuk melakukan pencarian
- **Satuan**: Detik (s)
- **Target**: < 0.5s untuk pengalaman real-time yang baik

#### 4. **Average Similarity Score**
- **Definisi**: Rata-rata skor kemiripan hasil yang ditemukan
- **Range**: 0.0 - 1.0
- **Target**: > 0.3 untuk hasil yang relevan

---

### **B. Generation Metrics (RAG-Specific)**

#### 1. **Faithfulness (Kesetiaan)**
- **Definisi**: Seberapa banyak teks yang dihasilkan berasal dari konteks yang diberikan
- **Formula**: `Faithfulness = (Kata dari konteks dalam hasil) / (Total kata hasil)`
- **Interpretasi**:
  - Tinggi (>0.6) = Minim halusinasi, grounded pada fakta
  - Rendah (<0.3) = Banyak informasi yang dibuat-buat

#### 2. **Answer Relevance**
- **Definisi**: Seberapa relevan jawaban terhadap query pengguna
- **Formula**: `Relevance = (Kata query dalam jawaban) / (Total kata query)`
- **Interpretasi**:
  - Tinggi (>0.5) = Jawaban sesuai pertanyaan
  - Rendah (<0.2) = Jawaban melenceng dari topik

#### 3. **Context Precision**
- **Definisi**: Seberapa relevan konteks yang diambil terhadap query
- **Formula**: `Context Precision = Rata-rata overlap kata antara captions dan query`
- **Interpretasi**:
  - Tinggi (>0.4) = Retrieval mengambil konteks yang tepat
  - Rendah (<0.2) = Konteks kurang relevan

#### 4. **Generation Time**
- **Definisi**: Waktu yang dibutuhkan LLM untuk generate teks
- **Satuan**: Detik (s)
- **Target**: < 5s untuk pengalaman yang responsif

---

## 🎬 Test Scenarios

Script menyediakan 4 kategori skenario testing:

### 1. **Simple Objects** (Objek Sederhana)
- Query tentang objek tunggal yang umum
- Contoh: "a cat sitting on a couch", "a car on the street"
- **Tujuan**: Mengukur akurasi dasar sistem

### 2. **Complex Scenes** (Adegan Kompleks)
- Query tentang scene dengan banyak elemen
- Contoh: "a group of people having dinner at a restaurant"
- **Tujuan**: Mengukur kemampuan memahami konteks kompleks

### 3. **Specific Attributes** (Atribut Spesifik)
- Query dengan detail warna, ukuran, atau karakteristik
- Contoh: "a red sports car", "a black and white cat"
- **Tujuan**: Mengukur presisi pencarian

### 4. **Abstract Concepts** (Konsep Abstrak)
- Query tentang emosi atau suasana
- Contoh: "a happy family moment", "a peaceful nature scene"
- **Tujuan**: Mengukur pemahaman semantik tingkat tinggi

---

## 🚀 Cara Menjalankan

### **Opsi 1: Evaluasi Lengkap**
```bash
python scripts/run_evaluation.py
```

Ini akan menjalankan:
- ✅ Retrieval evaluation (40+ queries)
- ✅ Generation evaluation (20+ queries)
- ✅ Scenario-based evaluation (4 scenarios)
- ✅ Generate JSON results + TXT report

### **Opsi 2: Custom Evaluation (Edit Script)**

Anda bisa memodifikasi parameter di fungsi `main()`:

```python
# Ubah jumlah query
retrieval_results = run_enhanced_retrieval_evaluation(
    retriever,
    test_queries=all_test_queries,
    num_random_queries=50,  # Ubah di sini
    k_values=[1, 3, 5, 10, 20]  # Tambah K values
)

# Ubah query untuk generation
generation_results = run_enhanced_generation_evaluation(
    retriever,
    text_gen,
    context_builder,
    test_queries=custom_queries,  # Gunakan query sendiri
    num_random_queries=5
)
```

### **Opsi 3: Tambah Skenario Sendiri**

Edit dictionary `TEST_SCENARIOS` di awal script:

```python
TEST_SCENARIOS = {
    "simple_objects": [...],
    "my_custom_scenario": [
        "query 1 saya",
        "query 2 saya",
        "query 3 saya"
    ]
}
```

---

## 📁 Output Files

### 1. **evaluation_results.json**
Lokasi: `experiments/results/evaluation_results.json`

Struktur:
```json
{
  "timestamp": "2025-12-21T20:00:00",
  "overall_retrieval": {
    "total_queries": 60,
    "avg_latency": 0.0523,
    "avg_similarity": 0.4521,
    "recall@1": 0.3500,
    "recall@5": 0.7200,
    "precision@1": 0.3500,
    "precision@5": 0.1440
  },
  "overall_generation": {
    "total_queries": 20,
    "avg_generation_time": 2.341,
    "avg_faithfulness": 0.6234,
    "avg_answer_relevance": 0.5123,
    "avg_context_precision": 0.4521
  },
  "scenario_results": {
    "simple_objects": {...},
    "complex_scenes": {...}
  }
}
```

### 2. **evaluation_report.txt**
Lokasi: `experiments/results/evaluation_report.txt`

Format human-readable untuk analisis cepat:
```
================================================================================
MULTIMODAL RAG SYSTEM - EVALUATION REPORT
================================================================================
Generated: 2025-12-21T20:00:00

OVERALL RETRIEVAL PERFORMANCE
--------------------------------------------------------------------------------
Total Queries Evaluated: 60
Average Latency: 0.0523s
Average Similarity Score: 0.4521

Recall@K:
  - Recall@1: 0.3500
  - Recall@3: 0.5800
  - Recall@5: 0.7200
  - Recall@10: 0.8500

...
```

---

## 📊 Cara Menganalisis Hasil

### **Step 1: Buka evaluation_report.txt**
Lihat ringkasan performa keseluruhan:
- Apakah latency < 0.5s? ✅
- Apakah Recall@5 > 0.6? ✅
- Apakah Faithfulness > 0.5? ✅

### **Step 2: Analisis Per Skenario**
Lihat bagian "SCENARIO-BASED RESULTS":
- Skenario mana yang performa terbaik?
- Skenario mana yang perlu improvement?

### **Step 3: Buka evaluation_results.json**
Untuk analisis detail:
- Lihat `detailed_retrieval.query_details` untuk per-query breakdown
- Lihat `detailed_generation.query_details` untuk contoh generated text

### **Step 4: Identifikasi Masalah**
| Gejala | Kemungkinan Masalah | Solusi |
|--------|---------------------|--------|
| Recall rendah | Embedding kurang bagus | Fine-tune CLIP atau ganti model |
| Precision rendah | Threshold similarity terlalu rendah | Naikkan threshold |
| Latency tinggi | Index tidak optimal | Gunakan FAISS IVF atau HNSW |
| Faithfulness rendah | LLM terlalu kreatif | Turunkan temperature, perbaiki prompt |
| Answer Relevance rendah | Context tidak relevan | Improve retrieval atau context builder |

---

## 🎓 Contoh Interpretasi untuk Laporan

### **Skenario: Hasil Evaluasi Bagus**
```
Recall@5: 0.78
Precision@5: 0.62
Faithfulness: 0.71
Answer Relevance: 0.68
```

**Analisis untuk Laporan:**
> "Sistem menunjukkan performa yang sangat baik dengan Recall@5 sebesar 0.78, 
> yang berarti 78% dokumen relevan berhasil ditemukan dalam 5 hasil teratas. 
> Precision@5 sebesar 0.62 menunjukkan bahwa mayoritas hasil yang ditampilkan 
> memang relevan. Pada aspek generatif, Faithfulness score 0.71 mengindikasikan 
> bahwa sistem minim halusinasi dan grounded pada konteks yang diberikan."

### **Skenario: Hasil Perlu Improvement**
```
Recall@5: 0.42
Precision@5: 0.28
Faithfulness: 0.35
Answer Relevance: 0.41
```

**Analisis untuk Laporan:**
> "Evaluasi menunjukkan beberapa area yang memerlukan perbaikan. Recall@5 
> sebesar 0.42 mengindikasikan bahwa sistem masih melewatkan banyak dokumen 
> relevan. Precision yang rendah (0.28) menunjukkan banyak hasil yang tidak 
> relevan masuk ke top-5. Faithfulness score 0.35 menunjukkan adanya 
> kecenderungan halusinasi pada model generatif, yang perlu diatasi dengan 
> perbaikan prompt engineering atau penurunan temperature parameter."

---

## 🔧 Troubleshooting

### **Error: "Text Generator not available"**
- **Penyebab**: API key LLM tidak tersedia atau salah
- **Solusi**: Cek `.env` file, pastikan `GROQ_API_KEY` atau `OPENAI_API_KEY` terisi

### **Error: "Failed to load metadata"**
- **Penyebab**: Embeddings belum di-generate
- **Solusi**: Jalankan `python scripts/setup.py` terlebih dahulu

### **Evaluasi terlalu lama**
- **Solusi**: Kurangi `num_random_queries` di script
- Atau comment out generation evaluation jika hanya perlu retrieval metrics

---

## 📈 Tips Meningkatkan Skor

### **Untuk Retrieval:**
1. **Tingkatkan Recall**: 
   - Gunakan model CLIP yang lebih besar (ViT-L/14)
   - Tambah jumlah data training

2. **Tingkatkan Precision**:
   - Naikkan similarity threshold
   - Gunakan re-ranking model

3. **Kurangi Latency**:
   - Gunakan FAISS GPU
   - Implementasi caching

### **Untuk Generation:**
1. **Tingkatkan Faithfulness**:
   - Turunkan temperature (0.3-0.5)
   - Perbaiki system prompt dengan instruksi "stick to facts"

2. **Tingkatkan Answer Relevance**:
   - Improve retrieval quality
   - Gunakan query expansion

3. **Tingkatkan Context Precision**:
   - Filter captions yang terlalu umum
   - Gunakan semantic similarity untuk ranking captions

---

## 📚 Referensi

- **RAGAS Framework**: https://docs.ragas.io/
- **CLIP Paper**: https://arxiv.org/abs/2103.00020
- **RAG Paper**: https://arxiv.org/abs/2005.11401

---

**Dibuat untuk**: Final Project Temu Kembali Citra  
**Terakhir diupdate**: 21 Desember 2025
