# Quick Guide: Metrics & Performance Feature

## ✅ What's New

Fitur metrics dan performance monitoring sudah ditambahkan ke sistem!

## 📊 Metrics yang Ditampilkan

### 1. Retrieval Quality Metrics
- **Avg Similarity**: Rata-rata similarity score (0-1)
- **Diversity**: Keunikan hasil (% unique captions)
- **Score Range**: Min-Max similarity scores
- **Std Deviation**: Konsistensi hasil

### 2. Generation Quality Metrics
- **Word Count**: Jumlah kata dalam deskripsi
- **Sentence Count**: Jumlah kalimat
- **Vocabulary Richness**: Rasio unique words
- **Avg Word Length**: Kompleksitas kata

### 3. Performance Metrics
- **Retrieval Time**: Waktu pencarian
- **Text Gen Time**: Waktu generate text
- **Image Gen Time**: Waktu generate image (jika ada)
- **Total Time**: End-to-end response time

## 🚀 Cara Menggunakan

1. **Jalankan aplikasi:**
   ```bash
   streamlit run src\ui\app.py
   ```

2. **Lakukan search seperti biasa**

3. **Lihat metrics di bagian bawah hasil:**
   - Section "📊 Metrics & Performance"
   - Klik untuk expand/collapse
   - Metrics ditampilkan dalam 3 kolom

## 📈 Interpretasi Metrics

### Retrieval Quality

| Metric | Good | Fair | Poor |
|--------|------|------|------|
| Avg Similarity | ≥0.7 | 0.5-0.7 | <0.5 |
| Diversity | ≥60% | 40-60% | <40% |

**Contoh:**
- Avg Similarity 0.85 = "Good" → Hasil sangat relevan
- Diversity 75% = "Good" → Hasil bervariasi

### Generation Quality

| Metric | Good | Fair | Long/Short |
|--------|------|------|------------|
| Word Count | 40-100 | 20-40 | <20 or >100 |
| Vocabulary | ≥70% | 50-70% | <50% |

**Contoh:**
- Word Count 65 = "Good" → Panjang ideal
- Vocabulary 82% = "Good" → Kaya kosakata

### Performance

| Operation | Target | Acceptable |
|-----------|--------|------------|
| Retrieval | <0.2s | <0.5s |
| Text Gen | <3s | <5s |
| Total | <5s | <10s |

## 🎯 Tips

1. **Retrieval terlalu lambat?**
   - Kurangi top-k value
   - Gunakan GPU jika tersedia

2. **Text generation lambat?**
   - Normal untuk LLM API
   - Gemini biasanya 2-4 detik

3. **Diversity rendah?**
   - Coba query yang lebih spesifik
   - Atau lebih general untuk hasil bervariasi

## 📝 Files yang Ditambahkan

1. `src/utils/metrics_calculator.py` - Metrics calculation logic
2. `src/utils/__init__.py` - Package init
3. Updated `src/ui/app.py` - UI dengan metrics display

## ✨ Features

- ✅ Real-time performance tracking
- ✅ Quality metrics untuk retrieval & generation
- ✅ Expandable metrics section (tidak mengganggu UI)
- ✅ Interpretasi otomatis (Good/Fair/Poor)
- ✅ Time formatting yang readable

Selamat mencoba! 🚀
