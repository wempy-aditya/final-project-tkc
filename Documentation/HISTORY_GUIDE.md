# Query History Feature Guide

## 🎯 Overview

Fitur **Query History** memungkinkan Anda menyimpan dan me-load kembali semua query yang pernah dilakukan beserta hasilnya.

---

## ✨ Features

### 1. Auto-Save
- Otomatis menyimpan setiap query
- Dapat di-enable/disable di sidebar
- Menyimpan semua data: query, results, metrics

### 2. History Tab
- View 20 query terakhir
- Informasi lengkap setiap query
- Load atau delete dengan 1 klik

### 3. Statistics
- Total queries
- Average similarity
- Average response time

---

## 🚀 How to Use

### Step 1: Enable Auto-Save

Di sidebar, tab "Config":
```
☑ Auto-save to history
```

### Step 2: Perform Searches

Lakukan search seperti biasa. Setiap query akan otomatis tersimpan.

### Step 3: View History

Buka tab "History" di sidebar untuk melihat query history.

### Step 4: Load Previous Query

Klik tombol "🔄 Load" pada query yang ingin di-load ulang.

### Step 5: Delete History

Klik tombol "🗑️ Delete" untuk menghapus query dari history.

---

## 📊 What's Stored

### Query Information
- Query text
- Query image (disimpan sebagai file)
- Query mode (Text/Image/Multimodal)
- Fusion weight (untuk multimodal)
- Top-K value
- Timestamp

### Retrieval Results
- Retrieved image paths
- Similarity scores
- Captions
- Retrieval metrics

### Generation Results
- Generated text description
- Generated image (disimpan sebagai file)
- Text metrics

### Performance Metrics
- Retrieval time
- Text generation time
- Image generation time
- Total time

---

## 📁 File Storage

```
history/
├── queries.db              # SQLite database
├── query_images/           # Uploaded query images
│   ├── query_1_20251217_140530.jpg
│   └── ...
└── generated_images/       # Generated images
    ├── gen_1_20251217_140535.jpg
    └── ...
```

---

## 💡 Tips

### 1. Manage Storage

History akan terus bertambah. Untuk menghemat space:
- Hapus query lama yang tidak diperlukan
- Atau hapus folder `history/` untuk reset

### 2. Export Data

Database SQLite dapat di-export:
```bash
sqlite3 history/queries.db .dump > backup.sql
```

### 3. Performance

- Database di-index untuk query cepat
- Load history: <50ms
- Save query: <100ms

---

## 🔧 Advanced Usage

### Query Database Directly

```python
from src.utils.history_manager import HistoryManager

manager = HistoryManager()

# Get all queries
queries = manager.get_all_queries(limit=50)

# Get specific query
query = manager.get_query_by_id(1)

# Get statistics
stats = manager.get_statistics()
print(f"Total: {stats['total_queries']}")
```

### Backup History

```bash
# Backup database
copy history\queries.db history\queries_backup.db

# Backup all files
xcopy history history_backup /E /I
```

---

## ❓ FAQ

**Q: Berapa lama history disimpan?**  
A: Permanent, sampai Anda hapus manual.

**Q: Apakah query image ikut tersimpan?**  
A: Ya, disimpan di `history/query_images/`

**Q: Bagaimana jika database corrupt?**  
A: Hapus `history/queries.db`, akan di-recreate otomatis.

**Q: Apakah bisa export history?**  
A: Ya, database SQLite bisa di-export/import.

**Q: Berapa ukuran database?**  
A: ~1-2KB per query, ~1-2MB untuk 1000 queries.

---

## 🎉 Example Workflow

1. **Search**: "a dog in the park"
2. **Auto-saved** to history
3. **View** in History tab
4. **Load** query besok untuk review
5. **Delete** jika sudah tidak perlu

Enjoy the history feature! 📜
