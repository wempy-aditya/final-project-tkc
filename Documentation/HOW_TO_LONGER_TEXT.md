# Cara Memperpanjang Generated Text

## ✅ Sudah Berhasil dengan Gemini 2.0 Flash!

Untuk membuat deskripsi lebih panjang dan detail, ada 2 cara:

---

## 🎯 **Cara 1: Edit File `.env`** (Termudah)

Buka file `.env` dan ubah:

```env
# Generation Settings
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=600  # Ubah dari 200 ke 600
```

**Parameter:**
- `LLM_MAX_TOKENS`: Maksimal panjang output
  - `200` = ~2-3 kalimat
  - `400` = ~4-5 kalimat  
  - `600` = ~6-8 kalimat
  - `800` = ~10+ kalimat

- `LLM_TEMPERATURE`: Kreativitas
  - `0.5` = Lebih konsisten, faktual
  - `0.7` = Balanced
  - `0.9` = Lebih kreatif, variatif

---

## 🎯 **Cara 2: Edit `context_builder.py`** (Sudah Saya Update!)

File `src/models/context_builder.py` sudah saya update dengan:

### **Perubahan:**

1. **Prompt lebih detail** (baris 17-28):
   ```python
   Create a detailed, comprehensive description (5-7 sentences). Include:
   - Main subject and primary action
   - Setting, environment, and background details
   - Colors, lighting, and visual elements
   - Atmosphere, mood, and overall impression
   - Any notable objects, people, or features
   - Spatial relationships and composition
   ```

2. **Lebih banyak captions** (baris 33):
   ```python
   max_captions: int = 5  # Dari 3 menjadi 5
   ```

---

## 📊 **Perbandingan:**

### **Sebelum (Setting Lama):**
```
LLM_MAX_TOKENS=200
max_captions=3
Prompt: "Create a brief description (2-3 sentences)"

Output: ~50-70 kata
```

### **Sesudah (Setting Baru):**
```
LLM_MAX_TOKENS=600
max_captions=5
Prompt: "Create a detailed description (5-7 sentences). Include: ..."

Output: ~150-200 kata
```

---

## 🚀 **Rekomendasi Setting Optimal:**

### **File `.env`:**
```env
GEMINI_API_KEY=your-key-here
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash-exp

# Settings untuk deskripsi panjang dan detail
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=600
```

### **Restart Aplikasi:**
```bash
# Stop aplikasi (Ctrl+C)
# Jalankan lagi
streamlit run src\ui\app.py
```

---

## 📝 **Contoh Output yang Diharapkan:**

### **Query:** "gerbong kereta sudah melaju"

### **Output Pendek (Setting Lama):**
```
A yellow and blue passenger train is stopped at a station. 
It appears to be a commuter train, ready to pick up passengers.
```

### **Output Panjang (Setting Baru):**
```
A vibrant yellow and blue passenger train sits prominently at a modern railway station platform. The train, appearing to be a commuter or regional service, features a sleek design with large windows running along its length. The bright yellow color scheme creates a striking contrast against the blue accents and the neutral tones of the station infrastructure. 

A wooden bench is positioned on the platform, suggesting a waiting area for passengers. The station environment appears calm and orderly, with the train as the central focal point of the scene. The lighting and composition highlight the train's modern design and the functional nature of the transit hub. The overall atmosphere conveys a sense of efficient urban transportation, with the train ready to serve its route.
```

---

## 🎨 **Customization Lebih Lanjut:**

Jika ingin kontrol lebih detail, edit `context_builder.py`:

### **Untuk Deskripsi Sangat Panjang (10+ kalimat):**
```python
# Baris 17-28
self.user_template = """Query: {query}

Captions:
{captions}

Create an extensive, highly detailed description (10-12 sentences). Include:
- Complete scene overview
- Main subjects and all actions
- Detailed setting and environment
- All colors, textures, and materials
- Lighting conditions and shadows
- Atmosphere, mood, and emotional tone
- All visible objects and their positions
- Background elements and context
- Composition and perspective
- Any text or signage visible
- Overall artistic or photographic quality

Description:"""
```

Dan di `.env`:
```env
LLM_MAX_TOKENS=1000
```

---

## ✅ **Yang Sudah Saya Lakukan:**

1. ✅ Update `context_builder.py` dengan prompt lebih detail
2. ✅ Naikkan `max_captions` dari 3 ke 5
3. ✅ Tambahkan instruksi spesifik untuk elemen yang harus disertakan

---

## 🧪 **Test Sekarang:**

1. **Edit `.env`:**
   ```env
   LLM_MAX_TOKENS=600
   LLM_TEMPERATURE=0.8
   ```

2. **Restart aplikasi:**
   ```bash
   streamlit run src\ui\app.py
   ```

3. **Test dengan query:** "gerbong kereta sudah melaju"

4. **Hasilnya seharusnya 5-7 kalimat** dengan detail lebih banyak!

---

**TL;DR:**
- Edit `.env` → `LLM_MAX_TOKENS=600`
- File `context_builder.py` sudah saya update
- Restart aplikasi
- Deskripsi sekarang 5-7 kalimat (vs 2-3 sebelumnya)

Silakan coba dan beri tahu hasilnya! 🚀
