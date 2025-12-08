# Panduan Setup Lengkap - Multimodal RAG System

## Langkah 1: Buat Virtual Environment

Buka terminal/command prompt di folder proyek ini, lalu jalankan:

```bash
# Buat virtual environment
python -m venv venv
```

## Langkah 2: Aktifkan Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Setelah aktif, Anda akan melihat `(venv)` di awal baris terminal.

## Langkah 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Catatan:** Proses ini akan memakan waktu beberapa menit karena menginstall PyTorch dan library besar lainnya.

## Langkah 4: Setup Environment Variables

1. Copy file `.env.example` menjadi `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit file `.env` dan tambahkan API key Anda:
   ```
   # Pilih salah satu:
   OPENAI_API_KEY=sk-your-openai-key-here
   # ATAU
   GROQ_API_KEY=your-groq-key-here
   
   # Konfigurasi LLM
   LLM_PROVIDER=openai  # atau "groq"
   LLM_MODEL=gpt-4o-mini  # atau "llama3-70b-8192" untuk groq
   ```

## Langkah 5: Download Dataset & Generate Embeddings

**PENTING:** Langkah ini akan:
- Download ~2GB data COCO
- Memakan waktu 20-30 menit
- Memerlukan koneksi internet yang stabil

```bash
python scripts/setup.py
```

**Jika download gagal**, Anda bisa skip download dan gunakan dataset yang lebih kecil:
```bash
python scripts/setup.py --skip-download --subset_size 1000
```

## Langkah 6: Jalankan Aplikasi

### Option A: Web UI (Streamlit)
```bash
streamlit run src/ui/app.py
```

Browser akan otomatis terbuka di `http://localhost:8501`

### Option B: Demo HTML (Tanpa Backend)
Buka file `demo/index.html` di browser Anda.

## Troubleshooting

### Error: "Execution Policy" (Windows PowerShell)
Jika mendapat error saat aktivasi venv, jalankan:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "torch not found" atau "CUDA error"
Ini normal jika Anda tidak punya GPU NVIDIA. PyTorch akan otomatis menggunakan CPU.

### Error: "Out of memory" saat generate embeddings
Kurangi batch size:
```bash
python src/preprocess/generate_embeddings.py --batch_size 16
```

### Error: "COCO download failed"
Download manual dari: http://images.cocodataset.org/zips/val2017.zip
Extract ke folder `data/coco/`

### Error: "OpenAI API key invalid"
- Pastikan API key sudah benar di file `.env`
- Cek saldo/credits di dashboard OpenAI

## Testing Tanpa Download Dataset

Jika Anda hanya ingin test kode tanpa download dataset besar:

1. Buat folder dummy:
   ```bash
   mkdir -p data/coco/images
   mkdir -p embeddings
   ```

2. Skip ke demo HTML:
   Buka `demo/index.html` - ini tidak memerlukan backend atau dataset.

## Struktur Folder Setelah Setup

```
multimodal-rag/
├── venv/                      # Virtual environment (jangan di-commit)
├── data/
│   └── coco/
│       ├── images/            # 5000 gambar COCO
│       ├── annotations/       # Metadata
│       └── captions.json      # Extracted captions
├── embeddings/
│   ├── image_embeddings.npy   # CLIP embeddings (512-dim)
│   ├── meta.json              # Metadata
│   └── faiss_index.bin        # FAISS index
└── ...
```

## Ukuran File yang Diharapkan

- `data/coco/`: ~2 GB
- `embeddings/image_embeddings.npy`: ~10 MB (untuk 5000 gambar)
- `embeddings/faiss_index.bin`: ~10 MB
- `venv/`: ~2-3 GB (tergantung OS)

## Cara Deaktivasi Virtual Environment

Setelah selesai bekerja:
```bash
deactivate
```

## Next Steps

Setelah setup berhasil:
1. ✅ Test retrieval: `python src/retrieval/retriever.py`
2. ✅ Jalankan UI: `streamlit run src/ui/app.py`
3. ✅ Run evaluation: `python scripts/run_evaluation.py`

## Catatan Penting

- **Jangan commit folder `venv/`** - sudah ada di `.gitignore`
- **Jangan commit file `.env`** - berisi API key rahasia
- **Folder `data/` dan `embeddings/`** juga di-ignore karena ukurannya besar
- Untuk deployment, generate embeddings di server/cloud

## Untuk Presentasi

Jika hanya untuk demo presentasi tanpa setup lengkap:
- Gunakan **`demo/index.html`** - buka langsung di browser
- Tidak perlu install Python atau dependencies
- Tidak perlu download dataset
- Sudah ada sample data dan animasi
