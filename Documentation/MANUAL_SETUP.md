# CARA SETUP MANUAL - STEP BY STEP

## Masalah yang Terjadi
Script batch error karena dijalankan dari folder yang salah. Solusinya: setup manual.

## ✅ Langkah-Langkah Setup (MUDAH)

### 1. Buka Terminal di Folder Proyek

**Cara 1 (Termudah):**
- Di VS Code, klik menu `Terminal` → `New Terminal`
- Terminal akan otomatis terbuka di folder proyek

**Cara 2:**
- Buka folder proyek di File Explorer
- Klik di address bar, ketik `cmd` lalu Enter

**Pastikan Anda berada di folder:**
```
d:\Documents\TUGAS KULIAH\ImageRetrieval\tugas_uas\multimodal-rag
```

### 2. Aktivasi Virtual Environment

```cmd
venv\Scripts\activate
```

Jika berhasil, Anda akan melihat `(venv)` di awal baris terminal:
```
(venv) d:\Documents\TUGAS KULIAH\ImageRetrieval\tugas_uas\multimodal-rag>
```

### 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

⏱️ Proses ini akan memakan waktu 5-10 menit.

### 4. Setup File .env

```cmd
copy .env.example .env
notepad .env
```

Edit file `.env` dan tambahkan API key Anda:
```
OPENAI_API_KEY=sk-your-actual-key-here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
```

Simpan dan tutup notepad.

### 5. Jalankan Aplikasi

```cmd
streamlit run src\ui\app.py
```

Browser akan otomatis terbuka di `http://localhost:8501`

## 🎯 Untuk Presentasi (TANPA Setup)

Jika Anda hanya butuh demo untuk presentasi:

1. Buka File Explorer
2. Navigate ke folder `demo`
3. Double-click file `index.html`
4. Selesai! Demo akan terbuka di browser

**Tidak perlu install Python, venv, atau dependencies apapun!**

## ⚠️ Troubleshooting

### Error: "python is not recognized"
Install Python dari https://www.python.org/downloads/
Centang "Add Python to PATH" saat install.

### Error: "cannot be loaded because running scripts is disabled"
Buka PowerShell sebagai Administrator, jalankan:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "pip install failed"
Coba satu per satu:
```cmd
pip install torch
pip install transformers
pip install streamlit
pip install faiss-cpu
```

### Virtual environment tidak aktif
Pastikan Anda melihat `(venv)` di terminal. Jika tidak, jalankan lagi:
```cmd
venv\Scripts\activate
```

## 📝 Perintah Berguna

```cmd
# Aktivasi venv
venv\Scripts\activate

# Deaktivasi venv
deactivate

# Cek package yang terinstall
pip list

# Jalankan Streamlit
streamlit run src\ui\app.py

# Test retrieval (setelah ada embeddings)
python src\retrieval\retriever.py
```

## 🚀 Next Steps (OPTIONAL)

Jika Anda ingin test retrieval dengan data real:

```cmd
# Download dataset COCO (2GB, 20-30 menit)
python scripts\setup.py
```

⚠️ **Ini OPTIONAL!** Aplikasi bisa jalan tanpa ini, hanya retrieval yang tidak akan bekerja.

## 💡 Rekomendasi

**Untuk Presentasi:**
- Gunakan `demo\index.html` (sudah interaktif dan cantik)
- Tidak perlu setup backend

**Untuk Development/Testing:**
- Setup lengkap dengan venv
- Install semua dependencies
- (Optional) Download dataset

## ✅ Checklist Setup

- [ ] Terminal dibuka di folder proyek yang benar
- [ ] Virtual environment aktif (ada `(venv)` di terminal)
- [ ] Dependencies terinstall (`pip list` menunjukkan streamlit, torch, dll)
- [ ] File `.env` sudah dibuat dan berisi API key
- [ ] Aplikasi bisa dijalankan dengan `streamlit run src\ui\app.py`

Jika semua checklist ✅, setup Anda sudah benar!
