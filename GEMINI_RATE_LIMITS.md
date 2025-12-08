# Gemini API - Rate Limits & Quota Guide

## ❌ Error 429: Quota Exceeded

### Masalah:
```
429 You exceeded your current quota
Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests
```

### Penyebab:
- Model **experimental** (`gemini-2.0-flash-exp`) memiliki **quota sangat terbatas**
- Free tier memiliki rate limit yang ketat
- Anda sudah mencapai limit requests per menit

---

## 📊 Gemini Models & Quota Comparison

| Model | Type | RPM (Free) | RPD (Free) | TPM (Free) | Rekomendasi |
|-------|------|------------|------------|------------|-------------|
| gemini-2.0-flash-exp | Experimental | **2** ❌ | 50 | 1M | Tidak |
| **gemini-1.5-flash** | **Stable** | **15** ✅ | **1,500** | **1M** | **Ya** |
| gemini-1.5-flash-8b | Stable | 15 | 1,500 | 1M | Ya |
| gemini-1.5-pro | Stable | 2 | 50 | 32K | Powerful |

**RPM** = Requests Per Minute  
**RPD** = Requests Per Day  
**TPM** = Tokens Per Minute

---

## ✅ Solusi: Ganti ke Model Stabil

### **Edit file `.env`:**

```env
# Ganti model dari experimental ke stable
LLM_MODEL=gemini-1.5-flash
```

**Kenapa `gemini-1.5-flash`?**
- ✅ **15 RPM** (vs 2 RPM di experimental)
- ✅ **1,500 requests/day** (vs 50/day)
- ✅ **Stabil** dan production-ready
- ✅ **Gratis** dengan quota yang generous
- ✅ **Cepat** dan berkualitas tinggi

---

## 🎯 Konfigurasi Optimal `.env`:

```env
# API Key
GEMINI_API_KEY=your-api-key-here

# Model Configuration
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-flash

# Generation Settings
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=200
```

---

## 📈 Rate Limits Detail (Free Tier)

### gemini-1.5-flash (RECOMMENDED)
- ✅ **15 requests/minute**
- ✅ **1,500 requests/day**
- ✅ **1 million tokens/minute**
- ✅ **Unlimited tokens/day**

### gemini-2.0-flash-exp (EXPERIMENTAL)
- ❌ **2 requests/minute** (Terlalu rendah!)
- ❌ **50 requests/day**
- ❌ **1 million tokens/minute**
- ❌ **Tidak stabil**

### gemini-1.5-pro (POWERFUL)
- ⚠️ **2 requests/minute**
- ⚠️ **50 requests/day**
- ✅ **32K tokens/minute**
- ✅ **Kualitas terbaik**

---

## 🔄 Cara Mengatasi Rate Limit

### 1. **Ganti Model (Solusi Terbaik)**
```env
LLM_MODEL=gemini-1.5-flash
```

### 2. **Tunggu Beberapa Detik**
Error message bilang: "Please retry in 16.216939282s"
- Tunggu ~20 detik
- Coba lagi

### 3. **Implementasi Retry Logic** (Opsional)
Tambahkan retry otomatis di kode (sudah ada di error handling)

### 4. **Monitor Usage**
- Cek usage: https://ai.dev/usage?tab=rate-limit
- Lihat quota: https://aistudio.google.com/app/apikey

---

## 💰 Upgrade Options (Jika Perlu)

### Pay-as-you-go Pricing (Jika butuh lebih)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| gemini-1.5-flash | $0.075 | $0.30 |
| gemini-1.5-pro | $1.25 | $5.00 |

**Catatan:** Free tier sudah sangat cukup untuk development dan testing!

---

## 🧪 Test dengan Model Baru

```bash
# Test API dengan model baru
python test_gemini.py

# Atau langsung jalankan aplikasi
streamlit run src\ui\app.py
```

---

## 📋 Checklist Solusi

- [ ] Edit `.env` → ganti `LLM_MODEL=gemini-1.5-flash`
- [ ] Restart aplikasi jika sedang running
- [ ] Test dengan `python test_gemini.py`
- [ ] Jika berhasil, jalankan aplikasi utama

---

## 🎯 Model Recommendation by Use Case

### Untuk Development/Testing (Anda)
```env
LLM_MODEL=gemini-1.5-flash
```
- ✅ 15 RPM cukup untuk testing
- ✅ 1,500 RPD sangat generous
- ✅ Gratis

### Untuk Production (Nanti)
```env
LLM_MODEL=gemini-1.5-flash
```
- Sama! Free tier cukup untuk small-medium apps
- Jika traffic tinggi, baru upgrade ke paid

### Untuk Kualitas Maksimal
```env
LLM_MODEL=gemini-1.5-pro
```
- ⚠️ Hanya 2 RPM (lambat untuk testing)
- ✅ Kualitas terbaik
- Gunakan hanya jika butuh kualitas premium

---

## 🔍 Monitoring Usage

### Check Current Usage:
1. Buka: https://ai.dev/usage?tab=rate-limit
2. Login dengan akun Google yang sama
3. Lihat usage per model

### Check API Key:
1. Buka: https://aistudio.google.com/app/apikey
2. Lihat API keys yang aktif
3. Regenerate jika perlu

---

## ⚡ Quick Fix Commands

```bash
# 1. Edit .env (ganti model)
notepad .env

# 2. Restart terminal (reload .env)
deactivate
venv\Scripts\activate

# 3. Test
python test_gemini.py

# 4. Run app
streamlit run src\ui\app.py
```

---

## 💡 Pro Tips

1. **Gunakan `gemini-1.5-flash`** untuk 99% use cases
2. **Monitor usage** di dashboard
3. **Jangan pakai experimental models** untuk production
4. **Free tier sudah sangat cukup** untuk proyek ini
5. **Rate limit reset setiap menit** - tunggu sebentar jika kena limit

---

**TL;DR:** Ganti `LLM_MODEL=gemini-1.5-flash` di `.env` dan masalah selesai! ✅
