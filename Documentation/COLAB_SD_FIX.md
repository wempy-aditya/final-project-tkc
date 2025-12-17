# Solusi Error Stable Diffusion di Colab

## ❌ Error yang Terjadi:
```
401 Client Error: Unauthorized
Repository Not Found for url: https://huggingface.co/api/models/stabilityai/stable-diffusion-2-1
```

## 🔍 Penyebab:
Model `stabilityai/stable-diffusion-2-1` adalah **gated model** yang memerlukan:
1. Hugging Face account
2. Accept license agreement
3. Authentication token

---

## ✅ Solusi 1: Gunakan Model Publik (Termudah)

Ganti model ke yang **tidak perlu authentication**:

### Di Cell "Load Stable Diffusion Model":

```python
# Ganti dari:
model_id = "stabilityai/stable-diffusion-2-1"

# Menjadi:
model_id = "runwayml/stable-diffusion-v1-5"
```

**Keuntungan:**
- ✅ Tidak perlu HF token
- ✅ Langsung bisa digunakan
- ✅ Lebih cepat download
- ✅ Kualitas tetap bagus

---

## ✅ Solusi 2: Setup Hugging Face Token (Untuk SD 2.1)

Jika tetap ingin pakai `stable-diffusion-2-1`:

### Langkah 1: Accept License
1. Buka: https://huggingface.co/stabilityai/stable-diffusion-2-1
2. Login/Sign up
3. Klik "Agree and access repository"

### Langkah 2: Get Token
1. Buka: https://huggingface.co/settings/tokens
2. Klik "New token"
3. Name: "colab-sd"
4. Type: "Read"
5. Copy token

### Langkah 3: Add to Colab Secrets
1. Di Colab, klik 🔑 icon (Secrets) di sidebar kiri
2. Klik "+ Add new secret"
3. Name: `HF_TOKEN`
4. Value: Paste token Anda
5. Toggle "Notebook access" ON

### Langkah 4: Run Cell Baru
Saya sudah tambahkan cell untuk load token dari secrets di notebook yang sudah diupdate.

---

## 📊 Perbandingan Model:

| Model | Auth Required | Quality | Speed | Size |
|-------|--------------|---------|-------|------|
| **runwayml/stable-diffusion-v1-5** | ❌ No | ⭐⭐⭐⭐ | ⚡⚡⚡ | 4GB |
| stabilityai/stable-diffusion-2-1 | ✅ Yes | ⭐⭐⭐⭐⭐ | ⚡⚡ | 5GB |
| CompVis/stable-diffusion-v1-4 | ❌ No | ⭐⭐⭐ | ⚡⚡⚡ | 4GB |

**Rekomendasi:** Gunakan `runwayml/stable-diffusion-v1-5` untuk kemudahan.

---

## 🚀 Quick Fix (Copy-Paste)

### Cell 2 (Baru - Setup HF Token):
```python
# Option 1: Use Colab Secrets (Recommended)
from google.colab import userdata
try:
    HF_TOKEN = userdata.get('HF_TOKEN')
    print("✅ HF_TOKEN loaded from Colab secrets")
except:
    print("⚠️ HF_TOKEN not found in secrets")
    HF_TOKEN = ""  # Or paste token here

# Login to Hugging Face
if HF_TOKEN:
    from huggingface_hub import login
    login(token=HF_TOKEN)
    print("✅ Logged in to Hugging Face")
```

### Cell 3 (Updated - Load Model):
```python
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

# Choose model (no auth required)
model_id = "runwayml/stable-diffusion-v1-5"

print(f"Loading model: {model_id}...")

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    safety_checker=None
)

pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cuda")

print("✅ Model loaded successfully!")
```

---

## 📝 Notebook Sudah Diupdate!

Saya sudah update `colab_sd_server.ipynb` dengan:
1. ✅ Cell baru untuk HF authentication
2. ✅ Default model ke `runwayml/stable-diffusion-v1-5`
3. ✅ Pilihan model yang bisa dipilih
4. ✅ Error handling yang lebih baik
5. ✅ Instruksi troubleshooting

---

## 🧪 Test Sekarang:

1. **Buka notebook di Colab**
2. **Runtime → Change runtime type → GPU (T4)**
3. **Run Cell 1:** Install dependencies
4. **Run Cell 2:** (Optional) Setup HF token
5. **Run Cell 3:** Load model - sekarang pakai `runwayml/stable-diffusion-v1-5`
6. **Run Cell 4:** Create Flask app
7. **Run Cell 5:** Setup ngrok (ganti token)
8. **Run Cell 6:** Start server

---

## 💡 Tips:

1. **Untuk quick start:** Gunakan `runwayml/stable-diffusion-v1-5`
2. **Untuk kualitas terbaik:** Setup HF token dan gunakan SD 2.1
3. **Jika Colab disconnect:** Model perlu di-load ulang
4. **Untuk save model:** Bisa download ke Google Drive

---

**TL;DR:**
1. Ganti `model_id = "runwayml/stable-diffusion-v1-5"`
2. Run notebook
3. Selesai! ✅

Atau jika mau pakai SD 2.1:
1. Accept license di HuggingFace
2. Get token
3. Add to Colab secrets
4. Run notebook dengan cell HF auth

Notebook sudah diupdate dengan semua solusi ini!
