# Fix untuk Error NLTK punkt_tab

## ❌ Error yang Terjadi:
```
LookupError: Resource punkt_tab not found.
Please use the NLTK Downloader to obtain the resource
```

## ✅ Solusi yang Sudah Diterapkan:

Saya sudah update file `src/evaluation/generation_metrics.py` dengan:

### 1. **Auto-download NLTK data**
```python
# Download required NLTK data
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    print("✅ NLTK data downloaded")
except Exception as e:
    print(f"⚠️ Could not download NLTK data: {e}")
```

### 2. **Better error handling**
Jika NLTK gagal, otomatis fallback ke simple word overlap.

---

## 🚀 Cara Menggunakan:

### **Option 1: Otomatis (File Sudah Diupdate)**
```bash
python scripts/run_evaluation.py
```

File sudah diupdate dan akan auto-download NLTK data saat pertama kali dijalankan.

---

### **Option 2: Manual Download (Jika Masih Error)**

Jika masih ada error, download manual:

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

Atau di Python REPL:
```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
```

---

## 📝 Yang Sudah Saya Ubah:

1. ✅ Tambahkan auto-download NLTK data di `generation_metrics.py`
2. ✅ Tambahkan error handling yang lebih baik
3. ✅ Fallback ke simple metrics jika NLTK gagal
4. ✅ Print pesan yang lebih jelas

---

## 🧪 Test Sekarang:

```bash
# Jalankan evaluation
python scripts/run_evaluation.py
```

**Expected output:**
```
✅ NLTK data downloaded
[nltk_data] Downloading package punkt to ...
[nltk_data] Downloading package punkt_tab to ...

=== RETRIEVAL EVALUATION ===
...

=== TEXT GENERATION EVALUATION ===
...
```

---

## 💡 Troubleshooting:

### **Jika masih error "punkt_tab not found":**

1. **Download manual:**
   ```bash
   python -c "import nltk; nltk.download('punkt_tab')"
   ```

2. **Check NLTK data path:**
   ```python
   import nltk
   print(nltk.data.path)
   ```

3. **Install ulang NLTK:**
   ```bash
   pip uninstall nltk
   pip install nltk
   ```

### **Jika internet lambat:**
NLTK data akan di-download (~13MB). Jika internet lambat, tunggu beberapa menit.

### **Jika tidak bisa download:**
Metrics akan otomatis fallback ke simple word overlap (tidak seakurat BLEU tapi tetap bisa jalan).

---

## ✅ Checklist:

- [x] File `generation_metrics.py` sudah diupdate
- [x] Auto-download NLTK data sudah ditambahkan
- [x] Error handling sudah diperbaiki
- [ ] Test dengan `python scripts/run_evaluation.py`

---

**TL;DR:**
- File sudah diupdate dengan auto-download
- Langsung jalankan: `python scripts/run_evaluation.py`
- Jika masih error: `python -c "import nltk; nltk.download('punkt_tab')"`

Silakan coba sekarang! ✅
