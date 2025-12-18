# LAPORAN AKHIR PROJECT TEMU KEMBALI CITRA
**Pengembangan Sistem Multimodal RAG Berbasis Citra dengan Integrasi CLIP, FAISS, LLM, dan Stable Diffusion**

---

**Disusun Oleh:**
* [Nama Anggota 1] (NIM)
* [Nama Anggota 2] (NIM)
* [Nama Anggota 3] (NIM)

**Mata Kuliah:** Project Temu Kembali Citra
**Dosen Pengampu:** [Nama Dosen]

---

## **DAFTAR ISI**

1. [BAB 1: PENDAHULUAN](#bab-1-pendahuluan)
2. [BAB 2: LANDASAN TEORI](#bab-2-landasan-teori)
3. [BAB 3: METODOLOGI & ARSITEKTUR SISTEM](#bab-3-metodologi--arsitektur-sistem)
4. [BAB 4: IMPLEMENTASI & PEMBAHASAN](#bab-4-implementasi--pembahasan)
5. [BAB 5: PENGUJIAN & EVALUASI](#bab-5-pengujian--evaluasi)
6. [BAB 6: KESIMPULAN](#bab-6-kesimpulan)
7. [DAFTAR PUSTAKA](#daftar-pustaka)

---

## **BAB 1: PENDAHULUAN**

### **1.1 Latar Belakang**
Perkembangan teknologi kecerdasan buatan (AI) telah mengubah cara kita berinteraksi dengan informasi visual. Sistem temu kembali informasi (*Information Retrieval*) tradisional yang hanya berbasis kata kunci seringkali gagal menangkap nuansa semantik dari query yang kompleks. Di sisi lain, model generatif modern seperti Large Language Models (LLM) dan model difusi gambar mampu menghasilkan konten kreatif namun terkadang mengalami halusinasi atau kurang memiliki konteks faktual.

Sistem *Retrieval-Augmented Generation* (RAG) hadir sebagai solusi yang menggabungkan kekuatan pencarian presisi dengan kemampuan generatif. Awalnya populer di domain teks, konsep ini kini berkembang ke domain multimodal. Dalam proyek ini, kami mengembangkan sistem "Smart Image Search", sebuah platform Multimodal RAG yang mengintegrasikan pencarian citra berbasis semantik (menggunakan model CLIP dan FAISS) dengan generasi konten cerdas (menggunakan LLM untuk deskripsi dan Stable Diffusion untuk sintesis citra).

Sistem ini tidak hanya mampu mencari gambar yang relevan berdasarkan query teks atau gambar, tetapi juga mampu "memahami" konten tersebut melalui deskripsi otomatis dan melakukan augmentasi visual dengan menciptakan gambar baru yang relevan.

### **1.2 Rumusan Masalah**
1.  Bagaimana membangun sistem pencarian yang mampu memahami query teks dan citra secara simultan dalam satu ruang vektor (embedding space)?
2.  Bagaimana mengintegrasikan hasil pencarian (*retrieved context*) ke dalam *pipeline* generatif untuk menghasilkan deskripsi teks yang akurat dan gambar baru yang relevan?
3.  Bagaimana merancang antarmuka pengguna (User Interface) yang modern, intuitif, dan responsif untuk sistem yang kompleks ini?

### **1.3 Tujuan Proyek**
1.  **Rancang Bangun Sistem End-to-End**: Mengimplementasikan arsitektur Multimodal RAG yang menghubungkan model retrieval (CLIP + FAISS) dengan model generatif (LLM + Stable Diffusion).
2.  **Pencarian Semantik Cerdas**: Menyediakan fitur pencarian *Text-to-Image*, *Image-to-Image*, dan *Multimodal* (gabungan teks dan gambar).
3.  **Augmentasi Generatif Terkini**: Menghasilkan deskripsi otomatis yang informatif dan variasi gambar baru berdasarkan konteks pencarian.
4.  **Modernisasi UI/UX**: Mengembangkan antarmuka web modern, interaktif, dan *user-friendly* menggunakan teknologi web terkini (HTML, Tailwind CSS, Vanilla JS) dan backend Flask.

### **1.4 Ruang Lingkup**
*   **Dataset**: Menggunakan subset dataset publik MS COCO 2017 (Validation Set) sebagai basis pengetahuan.
*   **Model**: Menggunakan *pretrained models* (CLIP ViT-B/32, GPT-4o-mini/Llama-3 via Groq, Stable Diffusion via API).
*   **Teknologi**: Backend menggunakan Python Flask, Frontend menggunakan HTML5 dan Tailwind CSS.
*   **Fokus**: Prototiping fungsi utama retrieval dan generation, serta visualisasi metrik performa.

---

## **BAB 2: LANDASAN TEORI**

### **2.1 Multimodal Retrieval & CLIP**
*Contrastive Language-Image Pre-training* (CLIP) adalah model yang dilatih oleh OpenAI untuk mempelajari representasi visual dari supervisi bahasa alami. CLIP memetakan citra dan teks ke dalam ruang vektor yang sama (*shared latent space*). Hal ini memungkinkan kita untuk menghitung kemiripan (*similarity*) antara deskripsi teks dan gambar menggunakan *cosine similarity* atau *dot product*, yang menjadi fondasi fitur *Cross-Modal Retrieval* pada sistem ini.

### **2.2 Vector Database & FAISS**
*Facebook AI Similarity Search* (FAISS) adalah perpustakaan efisien untuk pencarian kesamaan vektor dalam skala besar. Kami menggunakan indeks `IndexFlatIP` (*Inner Product*) dari FAISS karena memberikan hasil eksak dan sangat cepat untuk ukuran dataset yang kami gunakan. FAISS memungkinkan sistem melakukan kueri semantik dalam hitungan milidetik.

### **2.3 Retrieval-Augmented Generation (RAG)**
RAG adalah arsitektur yang melengkapi model generatif dengan informasi eksternal yang diambil (*retrieved*) dari basis data.
1.  **Retriever**: Mengambil dokumen/gambar relevan (Grounding Data).
2.  **Generator**: Menggunakan data tersebut sebagai konteks untuk menghasilkan jawaban.
Dalam proyek ini, caption dari gambar yang ditemukan (retrieved images) dijadikan konteks untuk LLM agar dapat menceritakan tentang gambar tersebut, dan dijadikan inspirasi untuk Stable Diffusion.

### **2.4 Model Generatif (LLM & Stable Diffusion)**
*   **LLM (Large Language Model)**: Digunakan untuk mensintesis narasi. Kami menggunakan API (seperti Groq/OpenAI) untuk performa tinggi dengan latensi rendah.
*   **Stable Diffusion**: Model generatif berbasis difusi yang mampu membuat gambar baru berdasarkan prompt teks. Sistem kami menggunakan ini untuk fitur "Create New Image".

---

## **BAB 3: METODOLOGI & ARSITEKTUR SISTEM**

### **3.1 Arsitektur Sistem Final**
Berbeda dengan rencana awal yang menggunakan Streamlit monolitik, kami mengimplementasikan arsitektur **Client-Server** terpisah untuk fleksibilitas dan performa UI yang lebih baik.

```mermaid
graph TD
    User[User / Web Frontend] <-->|HTTP REST API| API[Flask Backend API]
    
    subgraph "Backend System"
        API -->|1. Encode Query| CLIP[CLIP Model]
        CLIP -->|Embedding| FAISS[FAISS Vector Index]
        FAISS -->|2. Retrieve IDs| Database[(COCO Dataset + SQLite)]
        
        Database -->|3. Context (Captions)| Context[Context Builder]
        
        Context -->|4. Generate| LLM[LLM Engine (Groq/OpenAI)]
        Context -->|5. Generate| SD[Stable Diffusion API]
        
        API -->|Manage| History[History Manager (SQLite)]
    end
    
    subgraph "Frontend System"
        UI[Modern HTML/JS UI]
        State[App State Manager]
        Vis[Result Visualizer]
    end
```

**Alur Kerja Utama:**
1.  **Input**: Pengguna memasukkan teks, gambar, atau keduanya di Frontend.
2.  **Request**: Frontend mengirim data ke Backend via API (`/api/search`).
3.  **Processing**: Backend melakukan embedding input menggunakan CLIP.
4.  **Retrieval**: FAISS mencari vektor gambar yang paling mirip.
5.  **Generation**: 
    *   Backend mengambil caption dari gambar hasil pencarian.
    *   LLM membuat deskripsi ("What AI sees").
    *   Stable Diffusion membuat gambar variasi baru (opsional).
6.  **Response**: Backend mengirimkan JSON berisi hasil pencarian, teks, gambar base64, dan metrik.
7.  **Rendering**: Frontend menampilkan hasil secara dinamis tanpa *reload* halaman.

### **3.2 Teknologi yang Digunakan**
*   **Frontend**: HTML5, Vanilla JavaScript (ES6+), Tailwind CSS (Styling modern & responsif).
*   **Backend**: Python Flask (REST API Server).
*   **Core AI**: `transformers`, `torch`, `faiss-cpu`, `Pillow`.
*   **Database**: SQLite (untuk riwayat pencarian) & File System (untuk dataset COCO).

### **3.3 Manajemen Data**
*   **Preprocessing**: Gambar di-*resize* ke 224x224, dinormalisasi, dan di-*embedding* menggunakan CLIP ViT-B/32. Embedding disimpan sebagai file `.npy` dan dimuat ke FAISS saat *startup*.
*   **Dataset**: Subset COCO Validation 2017 (Images + Captions).

---

## **BAB 4: IMPLEMENTASI & PEMBAHASAN**

### **4.1 Implementasi Backend (Python Flask)**
Kami membangun backend yang modular. File utama `app.py` menangani *routing* API, sementara logika bisnis dipisah ke dalam folder `src/`:
*   `src/retrieval/retriever.py`: Menangani logika pencarian FAISS dan multimodality dengan *weighting slider* (penyeimbang bobot teks vs gambar).
*   `src/models/text_generator.py`: Wrapper untuk memanggil API LLM dengan prompt RAG yang terstruktur.
*   `src/utils/metrics_calculator.py`: Menghitung metrik performa *real-time* seperti *Diversity Score* dan *Average Similarity*.

**Fitur Unggulan Backend:**
*   **Multimodal Search**: Mampu menggabungkan vektor teks dan vektor gambar dengan bobot yang dapat diatur pengguna (`alpha * text_emb + (1-alpha) * image_emb`).
*   **History Management**: Menyimpan riwayat pencarian, hasil, dan metrik ke database SQLite, memungkinkan pengguna melihat kembali pencarian sebelumnya.

### **4.2 Implementasi Frontend (Modern Web UI)**
Kami beralih dari Streamlit ke *custom web development* untuk mencapai tampilan yang lebih profesional dan UX yang lebih halus.
*   **Desain**: Menggunakan gaya "Glassmorphism" halus dan palet warna modern (Blue, Cyan, Purple) dengan dukungan **Dark Mode**.
*   **Interaktivitas**: Menggunakan AJAX (`fetch` API) untuk komunikasi asinkron, sehingga pengalaman pengguna terasa sangat cepat dan responsif.
*   **Komponen**: 
    *   *Search Bar* intuitif dengan mode selector.
    *   *Masonry Grid* untuk menampilkan hasil gambar.
    *   *Interactive Metrics Cards* untuk menampilkan statistik kualitas pencarian.

### **4.3 Hasil Tampilan Sistem**
*(Pada bagian ini, screenshot sistem yang telah dibuat ditampilkan)*

1.  **Halaman Utama (Light & Dark Mode)**: Menampilkan antarmuka pencarian yang bersih dan ramah pengguna.
2.  **Hasil Pencarian**: Menampilkan gambar-gambar yang relevan dari dataset COCO.
3.  **Hasil Generasi**: Menampilkan deskripsi teks yang dibuat oleh AI dan gambar baru yang dihasilkan.
4.  **Riwayat & Statistik**: Sidebar yang menampilkan log aktivitas dan performa sistem.

---

## **BAB 5: PENGUJIAN & EVALUASI**

### **5.1 Skenario Pengujian**
Kami melakukan pengujian fungsional dan performa:
1.  **Text Search**: Mencari "a cat sleeping on a sofa".
2.  **Image Search**: Mengunggah gambar referensi kucing.
3.  **Multimodal Search**: Mengunggah gambar kucing tapi menambahkan teks "in space" (di luar angkasa).

### **5.2 Hasil Metrik Kuantitatif**
Sistem kami memiliki fitur *built-in metrics* yang menghitung performa setiap kali pencarian dilakukan:
*   **Average Similarity Score**: Rata-rata skor cosinus antara query dan hasil retrieved. (Target: > 0.25 untuk top-5).
*   **Diversity Score**: Mengukur keberagaman hasil agar tidak monoton.
*   **Response Time**: Rata-rata waktu proses backend.
    *   *Retrieval*: ~0.05 detik (Sangat cepat berkat FAISS).
    *   *Generation*: ~2-5 detik (Tergantung API LLM).

### **5.3 Analisis Kualitatif**
*   **Relevansi**: Sistem mampu menemukan objek spesifik (misal: "payung merah") dengan akurasi tinggi berkat model CLIP.
*   **Generasi**: Deskripsi yang dihasilkan LLM sangat kontekstual karena didasarkan pada *ground truth captions* dari dataset, mengurangi halusinasi.
*   **UX**: Transisi ke Web UI kustom memberikan pengalaman yang jauh lebih premium dibandingkan standard Streamlit apps.

---

## **BAB 6: KESIMPULAN & SARAN**

### **6.1 Kesimpulan**
Proyek ini berhasil mencapai seluruh tujuan yang ditetapkan:
1.  Sistem RAG Multimodal berhasil diimplementasikan sepenuhnya dengan arsitektur Client-Server yang modern.
2.  Integrasi CLIP dan FAISS terbukti sangat efektif untuk pencarian semantik skala besar dengan latensi rendah.
3.  Komponen generatif (LLM & Stable Diffusion) berhasil memperkaya hasil pencarian, memberikan nilai tambah informasi dan visual.
4.  UI/UX baru yang dibangun jauh melampaui ekspektasi awal proposal, menawarkan fitur Dark Mode, History, dan real-time metrics.

### **6.2 Saran Pengembangan**
*   **Model Lokal**: Mengganti dependensi API eksternal dengan model lokal terkuantisasi (misal: Llama-3-8B-Quantized) untuk privasi penuh.
*   **Dataset Lebih Besar**: Menguji skalabilitas dengan dataset penuh COCO (100k+ gambar) atau dataset custom.
*   **Video Retrieval**: Memperluas kapabilitas untuk pencarian video.

---

## **DAFTAR PUSTAKA**
1.  Radford, A., et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision* (CLIP). OpenAI.
2.  Johnson, J., et al. (2019). *Billion-scale similarity search with GPUs* (FAISS). IEEE Big Data.
3.  Lewis, P., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS.
4.  Rombach, R., et al. (2022). *High-Resolution Image Synthesis with Latent Diffusion Models*. CVPR.
5.  Documentation & Codebase Project: `multimodal-rag` Repository.

---
*Laporan ini disusun berdasarkan instruksi tugas akhir dan hasil implementasi sistem per tanggal 18 Desember 2025.*
