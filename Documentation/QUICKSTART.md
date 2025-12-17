# Quick Start - Multimodal RAG System

## 🚀 Cara Tercepat (Untuk Presentasi)

Jika Anda hanya butuh demo untuk presentasi:

1. **Buka file `demo/index.html` di browser**
   - Tidak perlu install apapun
   - Tidak perlu Python atau dependencies
   - Langsung jalan di browser

## 📦 Setup Lengkap (Dengan Backend)

### Windows - Cara Mudah

1. **Double-click `setup.bat`**
   - Script akan otomatis:
     - Aktivasi virtual environment
     - Install semua dependencies
     - Setup file .env

2. **Edit file `.env` dan tambahkan API key Anda**

3. **Double-click `run.bat`** untuk menjalankan aplikasi

### Manual Setup (Semua OS)

```bash
# 1. Buat virtual environment
python -m venv venv

# 2. Aktivasi venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env dan tambahkan API key

# 5. (OPTIONAL) Download dataset & generate embeddings
# PERINGATAN: Ini akan download 2GB dan butuh 20-30 menit
python scripts/setup.py

# 6. Jalankan aplikasi
streamlit run src/ui/app.py
```

## ⚡ Quick Commands

Setelah venv aktif:

```bash
# Jalankan web UI
streamlit run src/ui/app.py

# Test retrieval
python src/retrieval/retriever.py

# Run evaluation
python scripts/run_evaluation.py

# Generate embeddings only
python src/preprocess/generate_embeddings.py
```

## 📝 Yang Perlu Diubah

**File `.env`** - Tambahkan API key:
```env
OPENAI_API_KEY=sk-your-key-here
# ATAU
GROQ_API_KEY=your-groq-key-here

LLM_PROVIDER=openai  # atau "groq"
```

**Tidak ada file lain yang perlu diubah!**

## 🎯 Pilihan Setup

### Option 1: Demo HTML Saja (Tercepat)
- ✅ Buka `demo/index.html`
- ✅ Tidak perlu setup apapun
- ❌ Tidak ada backend real

### Option 2: Streamlit Tanpa Dataset
- ✅ Install dependencies saja
- ✅ Bisa test UI
- ❌ Retrieval tidak akan jalan (belum ada embeddings)

### Option 3: Full Setup
- ✅ Download dataset COCO
- ✅ Generate embeddings
- ✅ Semua fitur jalan
- ❌ Butuh waktu 30+ menit
- ❌ Butuh 2GB+ storage

## 🔧 Troubleshooting

**"python not found"**
- Install Python 3.8+ dari python.org

**"venv activation failed" (Windows)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**"Out of memory"**
```bash
# Kurangi batch size
python src/preprocess/generate_embeddings.py --batch_size 16
```

**"COCO download failed"**
- Download manual: http://images.cocodataset.org/zips/val2017.zip
- Extract ke `data/coco/`

## 📊 Untuk Presentasi

**Rekomendasi:**
1. Gunakan `demo/index.html` untuk presentasi
2. Tunjukkan kode di VS Code
3. Jelaskan arsitektur dari diagram di demo
4. (Optional) Jalankan Streamlit jika sudah setup

## 💡 Tips

- Virtual environment sudah di-gitignore
- File .env jangan di-commit (sudah di-gitignore)
- Dataset dan embeddings juga di-gitignore (terlalu besar)
- Untuk deployment, generate embeddings di server

## 📞 Need Help?

Lihat file `SETUP_GUIDE.md` untuk panduan detail lengkap.
