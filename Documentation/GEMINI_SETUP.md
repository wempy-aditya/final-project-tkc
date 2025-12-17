# Panduan Setup Gemini API

## ✅ Gemini API Sudah Didukung!

Saya sudah memodifikasi kode untuk support **Google Gemini API**. Ini pilihan yang bagus karena:
- ✅ **GRATIS** untuk penggunaan tertentu
- ✅ **Cepat** (gemini-2.0-flash-exp sangat cepat)
- ✅ **Powerful** (setara GPT-4)
- ✅ **Mudah** dapat API key

---

## 📝 Yang Sudah Diubah:

### 1. **File `src/models/text_generator.py`**
   - ✅ Ditambahkan support untuk Gemini API
   - ✅ Default provider sekarang `gemini`
   - ✅ Default model `gemini-2.0-flash-exp`

### 2. **File `requirements.txt`**
   - ✅ Ditambahkan `google-generativeai>=0.3.0`

### 3. **File `.env.example`**
   - ✅ Ditambahkan `GEMINI_API_KEY`
   - ✅ Default provider diubah ke `gemini`

---

## 🔑 Cara Mendapatkan Gemini API Key:

1. **Buka**: https://aistudio.google.com/app/apikey
2. **Login** dengan akun Google Anda
3. **Klik "Create API Key"**
4. **Copy** API key yang muncul

**GRATIS** dan langsung bisa digunakan!

---

## ⚙️ Setup File `.env`:

Edit file `.env` Anda dan tambahkan:

```env
# API Keys
GEMINI_API_KEY=AIzaSy...your-actual-key-here

# Model Configuration
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash-exp
```

**Catatan:** Jika ingin pakai model lain, pilihan yang tersedia:
- `gemini-2.0-flash-exp` (Tercepat, Gratis)
- `gemini-1.5-pro` (Lebih powerful)
- `gemini-1.5-flash` (Cepat, stabil)

---

## 📦 Install Library Gemini:

Jika Anda sudah install dependencies sebelumnya, tambahkan library Gemini:

```bash
# Aktivasi venv dulu
venv\Scripts\activate

# Install library Gemini
pip install google-generativeai
```

Atau install ulang semua dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧪 Test Gemini API:

Buat file test sederhana `test_gemini.py`:

```python
import os
from dotenv import load_dotenv
from src.models.text_generator import TextGenerator

load_dotenv()

# Test Gemini
generator = TextGenerator(provider="gemini")

system = "You are a helpful assistant."
user = "Describe a beautiful sunset in 2 sentences."

result = generator.generate(system, user)
print("Generated text:")
print(result)
```

Jalankan:
```bash
python test_gemini.py
```

---

## 📋 Konfigurasi Lengkap File `.env`:

```env
# ============================================
# API Keys
# ============================================
GEMINI_API_KEY=AIzaSy...your-key-here

# (Optional) Jika mau pakai provider lain
# OPENAI_API_KEY=sk-...
# GROQ_API_KEY=gsk_...

# ============================================
# LLM Configuration
# ============================================
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash-exp

# ============================================
# CLIP Configuration
# ============================================
CLIP_MODEL=openai/clip-vit-base-patch32

# ============================================
# Stable Diffusion (Optional)
# ============================================
SD_API_URL=http://localhost:7860
SD_MODEL=stabilityai/stable-diffusion-2-1

# ============================================
# Data Configuration
# ============================================
COCO_SUBSET_SIZE=5000
BATCH_SIZE=32
TOP_K=5

# ============================================
# Generation Parameters
# ============================================
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=200
SD_NUM_INFERENCE_STEPS=50
SD_GUIDANCE_SCALE=7.5
```

---

## 🎯 Pilihan Provider:

### **Option 1: Gemini (Recommended untuk Anda)**
```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash-exp
GEMINI_API_KEY=your-key-here
```
**Keuntungan:**
- ✅ Gratis
- ✅ Cepat
- ✅ Powerful
- ✅ Mudah setup

### **Option 2: OpenAI**
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-your-key-here
```
**Keuntungan:**
- ✅ Sangat powerful
- ❌ Berbayar (butuh credits)

### **Option 3: Groq (Llama)**
```env
LLM_PROVIDER=groq
LLM_MODEL=llama3-70b-8192
GROQ_API_KEY=gsk-your-key-here
```
**Keuntungan:**
- ✅ Gratis (limited)
- ✅ Sangat cepat
- ❌ Kadang rate limit

---

## ✅ Checklist Setup Gemini:

- [ ] Dapat API key dari https://aistudio.google.com/app/apikey
- [ ] Edit file `.env` dan tambahkan `GEMINI_API_KEY`
- [ ] Set `LLM_PROVIDER=gemini`
- [ ] Set `LLM_MODEL=gemini-2.0-flash-exp`
- [ ] Install library: `pip install google-generativeai`
- [ ] Test dengan menjalankan aplikasi

---

## 🚀 Cara Menjalankan:

```bash
# 1. Aktivasi venv
venv\Scripts\activate

# 2. Install library Gemini (jika belum)
pip install google-generativeai

# 3. Jalankan aplikasi
streamlit run src\ui\app.py
```

---

## 💡 Tips:

1. **Gemini 2.0 Flash** sangat cepat dan gratis - cocok untuk development
2. **Rate limit** Gemini gratis: 15 requests/minute, 1500 requests/day
3. Jika kena rate limit, tunggu sebentar atau upgrade ke paid tier
4. API key Gemini bisa di-regenerate kapan saja di dashboard

---

## 🔧 Troubleshooting:

**Error: "google.generativeai not found"**
```bash
pip install google-generativeai
```

**Error: "Invalid API key"**
- Cek API key di https://aistudio.google.com/app/apikey
- Pastikan tidak ada spasi di awal/akhir key
- Regenerate key jika perlu

**Error: "Rate limit exceeded"**
- Tunggu 1 menit
- Atau upgrade ke paid tier
- Atau gunakan provider lain (OpenAI/Groq)

---

## 📞 Link Berguna:

- **Get API Key**: https://aistudio.google.com/app/apikey
- **Gemini Docs**: https://ai.google.dev/docs
- **Pricing**: https://ai.google.dev/pricing (Gratis tier sangat generous!)

---

**Selamat! Anda sekarang bisa menggunakan Gemini API yang gratis dan powerful! 🎉**
