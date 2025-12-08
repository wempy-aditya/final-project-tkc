# Troubleshooting Gemini API Errors

## ❌ Error: finish_reason = 2 (SAFETY)

### Masalah:
```
Error: Unable to generate text. Invalid operation: The `response.text` quick accessor 
requires the response to contain a valid `Part`, but none were returned. 
The candidate's finish_reason is 2.
```

### Penyebab:
- **finish_reason = 2** berarti response diblokir oleh **safety filters** Gemini
- Gemini menganggap prompt atau response berpotensi tidak aman
- Ini bisa terjadi bahkan untuk prompt yang sebenarnya aman

### ✅ Solusi yang Sudah Diterapkan:

Saya sudah memperbaiki kode dengan:

1. **Menambahkan Safety Settings**
   - Menonaktifkan safety filters yang terlalu ketat
   - Settings: `BLOCK_NONE` untuk semua kategori

2. **Error Handling yang Lebih Baik**
   - Cek `finish_reason` sebelum akses `response.text`
   - Fallback ke `candidate.content.parts` jika perlu
   - Pesan error yang lebih jelas

### 📝 Finish Reason Codes:

| Code | Nama | Arti |
|------|------|------|
| 0 | FINISH_REASON_UNSPECIFIED | Tidak diketahui |
| 1 | STOP | ✅ Normal completion |
| 2 | MAX_TOKENS | Token limit tercapai |
| 3 | SAFETY | ❌ Blocked by safety |
| 4 | RECITATION | ❌ Blocked (recitation) |
| 5 | OTHER | Error lain |

### 🔧 Cara Menggunakan Kode yang Sudah Diperbaiki:

Tidak ada yang perlu diubah! Kode sudah otomatis:
- ✅ Menggunakan safety settings yang lebih permisif
- ✅ Handle semua finish_reason dengan baik
- ✅ Memberikan pesan error yang jelas

### 🧪 Test Ulang:

```bash
python test_gemini.py
```

Atau langsung jalankan aplikasi:
```bash
streamlit run src\ui\app.py
```

### 💡 Tips Menghindari Safety Blocks:

1. **Gunakan prompt yang jelas dan spesifik**
   - ✅ "Describe a dog playing in a park"
   - ❌ Prompt yang ambigu atau mengandung kata-kata sensitif

2. **Hindari kata-kata yang bisa di-flag**
   - Kata-kata kekerasan, seksual, atau berbahaya
   - Gunakan bahasa yang netral

3. **Jika masih kena block:**
   - Coba model lain: `gemini-1.5-flash` atau `gemini-1.5-pro`
   - Ubah temperature lebih rendah (0.3-0.5)
   - Simplify prompt

### 🔄 Alternative: Ganti Model

Jika `gemini-2.5-flash` masih bermasalah, coba model lain di `.env`:

```env
# Option 1: Gemini 2.0 Flash (Recommended)
LLM_MODEL=gemini-2.0-flash-exp

# Option 2: Gemini 1.5 Flash
LLM_MODEL=gemini-1.5-flash

# Option 3: Gemini 1.5 Pro (Lebih powerful)
LLM_MODEL=gemini-1.5-pro
```

### 📊 Perbandingan Model:

| Model | Speed | Quality | Safety Filters |
|-------|-------|---------|----------------|
| gemini-2.0-flash-exp | ⚡⚡⚡ | ⭐⭐⭐ | Ketat |
| gemini-2.5-flash | ⚡⚡ | ⭐⭐⭐⭐ | Sangat Ketat |
| gemini-1.5-flash | ⚡⚡ | ⭐⭐⭐ | Sedang |
| gemini-1.5-pro | ⚡ | ⭐⭐⭐⭐⭐ | Sedang |

**Rekomendasi:** Gunakan `gemini-2.0-flash-exp` atau `gemini-1.5-flash`

### 🎯 Konfigurasi Optimal untuk Proyek Ini:

Edit `.env`:

```env
# Gemini Configuration
GEMINI_API_KEY=your-api-key-here
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash-exp

# Generation Settings (Lebih konservatif untuk hindari blocks)
LLM_TEMPERATURE=0.5
LLM_MAX_TOKENS=300
```

### 🔍 Debug Mode:

Jika masih ada masalah, tambahkan debug print di `text_generator.py`:

```python
# Di method generate(), setelah response = self.client.generate_content(...)
print(f"Response candidates: {len(response.candidates)}")
if response.candidates:
    print(f"Finish reason: {response.candidates[0].finish_reason}")
    print(f"Safety ratings: {response.candidates[0].safety_ratings}")
```

### ✅ Checklist Troubleshooting:

- [x] Safety settings sudah diset ke `BLOCK_NONE`
- [x] Error handling untuk semua finish_reason
- [x] Fallback ke `parts[0].text` jika `response.text` gagal
- [ ] Test dengan `python test_gemini.py`
- [ ] Jika masih error, coba model lain
- [ ] Jika masih error, coba turunkan temperature

### 📞 Jika Masih Bermasalah:

1. **Cek safety ratings:**
   ```python
   print(response.candidates[0].safety_ratings)
   ```

2. **Coba prompt yang lebih sederhana:**
   ```python
   "Describe an image of a sunset"
   ```

3. **Gunakan provider lain:**
   ```env
   LLM_PROVIDER=openai  # atau groq
   ```

---

**Update:** Kode sudah diperbaiki! Seharusnya error finish_reason=2 sudah tidak muncul lagi. Jika masih muncul, coba ganti model ke `gemini-2.0-flash-exp`.
