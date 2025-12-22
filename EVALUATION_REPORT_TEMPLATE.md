# Template Analisis Hasil Evaluasi untuk Laporan Akhir

## BAB 5: PENGUJIAN & EVALUASI (TEMPLATE)

### 5.1 Metodologi Evaluasi

Evaluasi sistem dilakukan menggunakan script otomatis (`run_evaluation.py`) yang mengukur performa pada dua aspek utama: **retrieval** dan **generation**. Evaluasi dilakukan dengan menggunakan [JUMLAH] query test yang terdiri dari:
- Query predefined dari 4 kategori skenario (simple objects, complex scenes, specific attributes, abstract concepts)
- Query random sampling dari dataset COCO

**Hardware & Environment:**
- Processor: [ISI SPEC]
- RAM: [ISI SPEC]
- GPU: [ISI SPEC / None]
- Python Version: 3.x
- Backend API: Groq/OpenAI

---

### 5.2 Hasil Evaluasi Retrieval

#### 5.2.1 Metrik Keseluruhan

Tabel 1. Hasil Evaluasi Retrieval
| Metrik | Nilai | Interpretasi |
|--------|-------|--------------|
| Total Queries | [ISI] | Jumlah query yang dievaluasi |
| Average Latency | [ISI]s | Waktu rata-rata pencarian |
| Min Latency | [ISI]s | Waktu tercepat |
| Max Latency | [ISI]s | Waktu terlama |
| Avg Similarity Score | [ISI] | Rata-rata skor kemiripan |
| **Recall@1** | [ISI] | % dokumen relevan di rank 1 |
| **Recall@3** | [ISI] | % dokumen relevan di top-3 |
| **Recall@5** | [ISI] | % dokumen relevan di top-5 |
| **Recall@10** | [ISI] | % dokumen relevan di top-10 |
| **Precision@1** | [ISI] | Akurasi hasil rank 1 |
| **Precision@3** | [ISI] | Akurasi hasil top-3 |
| **Precision@5** | [ISI] | Akurasi hasil top-5 |
| **Precision@10** | [ISI] | Akurasi hasil top-10 |

#### 5.2.2 Analisis Performa Retrieval

**Kecepatan (Latency):**
> Sistem menunjukkan performa kecepatan yang [SANGAT BAIK/BAIK/CUKUP/KURANG] dengan rata-rata latency [ISI]s. Nilai ini [MEMENUHI/TIDAK MEMENUHI] target < 0.5s untuk aplikasi real-time. [JELASKAN FAKTOR PENYEBAB].

**Akurasi (Recall & Precision):**
> Recall@5 sebesar [ISI] menunjukkan bahwa sistem mampu menemukan [ISI]% dokumen relevan dalam 5 hasil teratas. Precision@5 sebesar [ISI] mengindikasikan bahwa [ISI]% dari hasil yang ditampilkan memang relevan. [BANDINGKAN DENGAN BASELINE ATAU PENELITIAN TERKAIT].

**Kualitas Embedding (Similarity Score):**
> Average similarity score [ISI] menunjukkan bahwa [ANALISIS: tinggi/rendah, apa artinya untuk kualitas hasil].

#### 5.2.3 Performa Per Skenario

Tabel 2. Perbandingan Performa Antar Skenario
| Skenario | Recall@5 | Precision@5 | Avg Latency | Catatan |
|----------|----------|-------------|-------------|---------|
| Simple Objects | [ISI] | [ISI] | [ISI]s | [ANALISIS] |
| Complex Scenes | [ISI] | [ISI] | [ISI]s | [ANALISIS] |
| Specific Attributes | [ISI] | [ISI] | [ISI]s | [ANALISIS] |
| Abstract Concepts | [ISI] | [ISI] | [ISI]s | [ANALISIS] |

**Insight:**
> [JELASKAN skenario mana yang paling mudah/sulit untuk sistem, kenapa, dan apa implikasinya]

---

### 5.3 Hasil Evaluasi Generation

#### 5.3.1 Metrik Keseluruhan

Tabel 3. Hasil Evaluasi Text Generation
| Metrik | Nilai | Interpretasi |
|--------|-------|--------------|
| Total Queries | [ISI] | Jumlah query yang dievaluasi |
| Avg Generation Time | [ISI]s | Waktu rata-rata generate teks |
| **Faithfulness** | [ISI] | Tingkat grounding pada konteks |
| **Answer Relevance** | [ISI] | Relevansi jawaban terhadap query |
| **Context Precision** | [ISI] | Kualitas konteks yang diambil |

#### 5.3.2 Analisis Performa Generation

**Kecepatan Generation:**
> Waktu rata-rata generation [ISI]s menunjukkan [ANALISIS: cepat/lambat, acceptable/tidak untuk user experience].

**Faithfulness (Anti-Halusinasi):**
> Score faithfulness [ISI] mengindikasikan bahwa [ISI]% dari teks yang dihasilkan berasal dari konteks yang diberikan. Ini menunjukkan sistem [SANGAT MINIM/MINIM/CUKUP BANYAK/BANYAK] mengalami halusinasi. [JELASKAN IMPLIKASI].

**Answer Relevance:**
> Score [ISI] menunjukkan bahwa jawaban yang dihasilkan [SANGAT RELEVAN/RELEVAN/KURANG RELEVAN] dengan query pengguna. [ANALISIS LEBIH LANJUT].

**Context Precision:**
> Nilai [ISI] menunjukkan bahwa komponen retrieval [BERHASIL/CUKUP BERHASIL/KURANG BERHASIL] dalam mengambil konteks yang relevan untuk generation. [JELASKAN HUBUNGAN DENGAN RETRIEVAL METRICS].

#### 5.3.3 Contoh Output Generation

**Query:** "[ISI CONTOH QUERY]"

**Retrieved Captions:**
1. [ISI]
2. [ISI]
3. [ISI]

**Generated Description:**
> "[ISI HASIL GENERATION]"

**Analisis:**
- Faithfulness: [ISI] - [JELASKAN kenapa tinggi/rendah]
- Answer Relevance: [ISI] - [JELASKAN]
- Kualitas Bahasa: [SUBJEKTIF: koheren/tidak, natural/tidak]

---

### 5.4 Analisis Kualitatif

#### 5.4.1 Kelebihan Sistem
1. **[KELEBIHAN 1]**: [JELASKAN dengan data pendukung]
2. **[KELEBIHAN 2]**: [JELASKAN dengan data pendukung]
3. **[KELEBIHAN 3]**: [JELASKAN dengan data pendukung]

#### 5.4.2 Keterbatasan Sistem
1. **[KETERBATASAN 1]**: [JELASKAN dengan contoh kasus]
2. **[KETERBATASAN 2]**: [JELASKAN dengan contoh kasus]
3. **[KETERBATASAN 3]**: [JELASKAN dengan contoh kasus]

#### 5.4.3 Perbandingan dengan Baseline

Tabel 4. Perbandingan dengan Sistem Baseline
| Metrik | Sistem Kami | Baseline* | Improvement |
|--------|-------------|-----------|-------------|
| Recall@5 | [ISI] | [ISI] | [ISI]% |
| Precision@5 | [ISI] | [ISI] | [ISI]% |
| Latency | [ISI]s | [ISI]s | [ISI]% |
| Faithfulness | [ISI] | N/A | - |

*Baseline: [JELASKAN apa baseline-nya, misal: traditional keyword search, atau penelitian terkait]

---

### 5.5 Kesimpulan Evaluasi

Berdasarkan hasil evaluasi komprehensif yang telah dilakukan:

1. **Performa Retrieval**: Sistem menunjukkan [KESIMPULAN SINGKAT tentang retrieval performance]

2. **Performa Generation**: Komponen generatif [KESIMPULAN SINGKAT tentang generation performance]

3. **Kesiapan Sistem**: Sistem [SIAP/BELUM SIAP/SIAP DENGAN CATATAN] untuk [deployment/penggunaan lebih lanjut] dengan [JELASKAN kondisi atau improvement yang diperlukan]

4. **Kontribusi Utama**: Penelitian ini berhasil [JELASKAN kontribusi utama, misal: "mengintegrasikan RAG dengan multimodal search" atau "menunjukkan efektivitas CLIP untuk domain tertentu"]

---

## CARA MENGISI TEMPLATE INI:

### Step 1: Jalankan Evaluasi
```bash
python scripts/run_evaluation.py
```

### Step 2: Buka File Hasil
- `experiments/results/evaluation_report.txt` - untuk angka-angka
- `experiments/results/evaluation_results.json` - untuk detail

### Step 3: Copy Angka ke Template
Salin nilai dari report.txt ke tabel-tabel di atas

### Step 4: Tulis Analisis
Untuk setiap [ISI] atau [ANALISIS], tulis interpretasi berdasarkan:
- Apakah nilai bagus/buruk? (bandingkan dengan threshold di EVALUATION_GUIDE.md)
- Kenapa bisa begitu? (jelaskan faktor teknis)
- Apa implikasinya? (untuk user experience atau sistem secara keseluruhan)

### Step 5: Tambahkan Visualisasi (Opsional)
Buat grafik dari data JSON:
- Bar chart: Recall@K vs K
- Line chart: Latency distribution
- Scatter plot: Similarity score vs Recall

### Step 6: Screenshot
Ambil screenshot dari:
- Web UI saat melakukan search
- Hasil evaluasi di terminal
- Contoh hasil generation yang bagus/jelek

---

## CONTOH ANALISIS YANG BAIK:

❌ **Buruk:**
> "Recall@5 adalah 0.72. Ini bagus."

✅ **Baik:**
> "Sistem mencapai Recall@5 sebesar 0.72, yang berarti 72% dari dokumen relevan berhasil ditemukan dalam 5 hasil teratas. Nilai ini melampaui threshold minimum 0.6 yang umumnya dianggap acceptable untuk sistem retrieval (Manning et al., 2008). Performa ini menunjukkan bahwa model CLIP ViT-B/32 yang digunakan mampu menangkap semantic similarity dengan baik pada dataset COCO. Namun, masih terdapat 28% dokumen relevan yang terlewat, yang kemungkinan disebabkan oleh keterbatasan embedding dimension (512) dan variasi caption yang terbatas per image."

---

**Catatan Penting:**
- Jujur dalam melaporkan hasil (baik atau buruk)
- Selalu sertakan interpretasi, jangan hanya angka
- Hubungkan hasil dengan teori/literatur
- Jelaskan limitasi dan future work
