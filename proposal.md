# **SISTEM RAG MULTIMODAL BERBASIS CITRA DENGAN INTEGRASI CLIP, FAISS, LLM, DAN STABLE DIFFUSION PADA DATASET MS COCO**

Proposal ini disusun guna memenuhi salah satu tugas pada mata kuliah *Project Temu Kembali Citra*.



**Daftar Isi**

[1\. PENDAHULUAN	4](#heading=)

[1.1 Latar Belakang	4](#heading=)

[1.2 Rumusan Masalah	5](#heading=)

[1.3 Tujuan Proyek	5](#heading=)

[1.4 Ruang Lingkup dan Batasan Masalah	6](#heading=)

[2\. TINJAUAN PUSTAKA DAN LANDASAN TEORI	6](#heading=)

[2.1 Multimodal Embedding dan CLIP (Contrastive Language-Image Pre-training)	6](#heading=)

[2.2 Vector Database dan FAISS	7](#heading=)

[2.3 Retrieval-Augmented Generation (RAG)	8](#heading=)

[2.4 Generative AI: LLM dan Stable Diffusion	8](#heading=)

[3\. METODOLOGI DAN ARSITEKTUR SISTEM	8](#heading=)

[3.1 Gambaran Umum Arsitektur (High-Level Architecture)	9](#heading=)

[3.2 Komponen 1: Manajemen Dataset dan Preprocessing	9](#heading=)

[3.3 Komponen 2: Feature Extraction (Embedding)	10](#heading=)

[3.4 Komponen 3: Retrieval Engine (FAISS)	11](#heading=)

[3.5 Komponen 4: Generative Augmentation (RAG)	11](#heading=)

[4\. RENCANA IMPLEMENTASI TEKNIS	12](#heading=)

[4.1 Lingkungan Pengembangan (Development Environment)	12](#heading=)

[4.2 Struktur Proyek	12](#heading=)

[4.3 Alur Implementasi (Step-by-Step)	13](#heading=)

[Tahap 1: Persiapan Data (Minggu 1\)	13](#heading=)

[Tahap 2: Pembangunan Indeks (Minggu 2\)	13](#heading=)

[Tahap 3: Integrasi Generatif (Minggu 3\)	13](#heading=)

[Tahap 4: Pengembangan UI & Integrasi Akhir (Minggu 4\)	13](#heading=)

[5\. STRATEGI EVALUASI DAN MATRIKS PENGUKURAN	13](#heading=)

[5.1 Evaluasi Komponen Retrieval	14](#heading=)

[5.2 Evaluasi Komponen Generatif (Teks)	14](#heading=)

[5.3 Evaluasi Komponen Generatif (Citra)	15](#heading=)

[6\. MANAJEMEN PROYEK	15](#heading=)

[6.1 Struktur Tim dan Pembagian Tugas	15](#heading=)

[6.2 Timeline Pengerjaan (4 Minggu)	16](#heading=)

[Minggu 1: Fondasi dan Data (25 Nov \- 1 Des)	16](#heading=)

[Minggu 2: Core Retrieval Implementation (2 Des \- 7 Des)	17](#heading=)

[Minggu 3: Generative Integration & UI (8 Des \- 14 Des)	17](#heading=)

[Minggu 4: Evaluasi dan Finalisasi (15 Des \- 21 Des)	17](#heading=)

[7\. HASIL ANTAR MUKA YANG DIHARAPKAN	17](#heading=)

[8\. KESIMPULAN	19](#heading=)

[REFERENSI	20](#heading=)

## 

## **1\. PENDAHULUAN**

### **1.1 Latar Belakang** 

Dalam lanskap teknologi informasi kontemporer, volume data visual yang diproduksi dan dikonsumsi oleh masyarakat global telah mencapai tingkat eksponensial. Platform media sosial, arsip digital, dan repository medis dibanjiri oleh citra dan video, menciptakan kebutuhan mendesak akan sistem temu kembali informasi (*Information Retrieval* atau IR) yang tidak hanya cepat tetapi juga cerdas secara semantik. Paradigma tradisional dalam temu kembali informasi, yang selama berdekade-dekade didominasi oleh pencarian berbasis kata kunci (*keyword-based search*) atau *lexical matching* seperti BM25 dan TF-IDF, kini menghadapi limitasi fundamental. Pendekatan leksikal ini sering kali gagal menangkap nuansa makna, sinonim, dan konteks visual yang implisit, fenomena yang dikenal sebagai *semantic gap* atau kesenjangan semantik antara representasi data tingkat rendah (piksel) dan konsep tingkat tinggi (makna manusia).  
Seiring dengan perkembangan *Deep Learning*, khususnya arsitektur *Transformer*, telah terjadi revolusi dalam cara mesin memahami data. Pendekatan *Dense Retrieval* muncul sebagai solusi superior, dimana entitas data—baik teks maupun citra—diproyeksikan ke dalam ruang vektor berdimensi tinggi (*high-dimensional latent space*). Dalam ruang ini, kedekatan geometris merepresentasikan kedekatan semantik. Terobosan ini difasilitasi oleh model pra-latih (*pre-trained models*) seperti BERT untuk pemrosesan bahasa alami (*Natural Language Processing* \- NLP) dan Vision Transformer (ViT) untuk visi komputer.  
Namun, tantangan dalam rekayasa kecerdasan buatan modern tidak berhenti pada kemampuan "mencari" (*retrieval*). Terdapat kebutuhan yang semakin besar untuk kemampuan "mensintesis" dan "menciptakan" (*generation*). Model generatif besar (*Generative AI*), seperti seri GPT (*Generative Pre-trained Transformer*) dan model difusi (*Diffusion Models*), telah menunjukkan kemampuan luar biasa dalam menghasilkan teks dan citra yang koheren. Akan tetapi, model-model ini memiliki kelemahan kritis: kecenderungan untuk berhalusinasi (*hallucination*), yaitu menghasilkan informasi yang tampak meyakinkan namun faktanya salah atau tidak berdasar, serta keterbatasan pengetahuan yang terhenti pada tanggal pemotongan data latih (*knowledge cutoff*).1  
Untuk mengatasi dilema ini, konsep Retrieval-Augmented Generation (RAG) hadir sebagai arsitektur hibrida yang elegan. RAG menggabungkan presisi sistem pencarian (retrieval) dengan kreativitas sistem generatif. Dalam sistem RAG, model tidak dibiarkan mengarang jawaban dari ruang hampa; sebaliknya, model "dipaksa" untuk merujuk pada dokumen atau data eksternal yang relevan yang ditemukan melalui proses retrieval sebelum menghasilkan respons. Meskipun RAG awalnya dipopulerkan dalam domain teks, proyek ini bertujuan untuk memperluas cakrawala tersebut ke domain multimodal.  
Proyek Akhir ini, yang berjudul "Pengembangan Sistem Multimodal RAG Berbasis Citra", dirancang untuk membangun sebuah ekosistem cerdas yang mampu memproses, memahami, dan mensintesis informasi lintas modalitas (teks dan citra). Sistem ini akan mengintegrasikan teknologi *State-of-the-Art* (SOTA) termasuk CLIP (Contrastive Language-Image Pre-training) sebagai jembatan semantik antara visi dan bahasa, FAISS (Facebook AI Similarity Search) sebagai mesin pencari vektor berkinerja tinggi, Large Language Models (LLM) untuk penalaran naratif, dan Stable Diffusion untuk sintesis visual.2

### **1.2 Rumusan Masalah**

Berdasarkan latar belakang tersebut, pengembangan sistem ini didorong oleh sejumlah permasalahan teknis dan teoritis yang perlu diselesaikan:

1. Kesenjangan Modalitas (Modality Gap): Bagaimana merancang arsitektur sistem yang mampu memetakan input teks dan citra ke dalam ruang fitur yang sama (common embedding space) sehingga memungkinkan pencarian lintas-modal (*cross-modal retrieval*) yang akurat tanpa pelatihan ulang model dari nol?  
2. Akurasi dan Efisiensi Retrieval: Bagaimana mengimplementasikan mekanisme indeksasi vektor yang *scalable* untuk dataset berskala ribuan hingga jutaan citra, serta metrik jarak apa yang paling optimal untuk mengukur kemiripan semantik dalam konteks dataset MS COCO?  
3. Halusinasi Generatif dan Grounding: Bagaimana mekanisme *context injection* yang efektif untuk memastikan bahwa narasi yang dihasilkan oleh LLM dan citra yang dihasilkan oleh Stable Diffusion benar-benar berpijak (*grounded*) pada hasil retrieval, bukan semata-mata hasil interpolasi model?  
4. Kompleksitas Evaluasi Multimodal: Mengingat subjektivitas dalam persepsi visual dan narasi, metrik evaluasi kuantitatif dan kualitatif apa yang harus diterapkan untuk mengukur kinerja sistem RAG secara holistik, mencakup aspek *faithfulness*, *relevance*, dan *coherence*?.3

### **1.3 Tujuan Proyek**

Proyek ini memiliki tujuan komprehensif yang mencakup aspek teknis, akademis, dan praktis:

1. Rancang Bangun Sistem End-to-End: Mengembangkan sistem RAG multimodal fungsional yang mengintegrasikan *retriever* (CLIP \+ FAISS) dan *generator* (LLM \+ Stable Diffusion) dalam satu *pipeline* terpadu.  
2. Implementasi Temu Kembali Cerdas: Merealisasikan kemampuan pencarian *Text-to-Image* dan *Image-to-Image* yang melampaui pencocokan kata kunci, memanfaatkan pemahaman semantik mendalam.  
3. Augmentasi Generatif: Menghasilkan deskripsi tekstual yang kaya konteks dan sintesis citra baru yang memiliki koherensi tinggi dengan kueri pengguna, berbasiskan bukti visual yang ditemukan dari dataset.  
4. Evaluasi Terukur: Melakukan pengujian sistematis menggunakan metrik standar industri seperti Recall@K, Precision@K, CLIP Score, dan evaluasi berbasis LLM (*LLM-as-a-judge*) untuk memvalidasi kinerja sistem.  
5. Antarmuka Pengguna Interaktif: Menyediakan aksesibilitas bagi pengguna melalui Web UI berbasis Streamlit yang intuitif.

### **1.4 Ruang Lingkup dan Batasan Masalah**

Agar pengerjaan proyek tetap terfokus dan dapat diselesaikan dalam *timeline* yang ditentukan (satu bulan), ditetapkan batasan masalah sebagai berikut 2:

* Dataset: Menggunakan subset dari MS COCO Captions 2017 (5.000–10.000 sampel) untuk menjaga efisiensi waktu komputasi saat indeksasi dan retrieval.  
* Model Pre-trained: Tidak melakukan pelatihan model (*training from scratch*) atau *fine-tuning* berat. Fokus pada pemanfaatan model pra-latih (CLIP, Llama-3/GPT-4o-mini, Stable Diffusion v1.5/SDXL).  
* Infrastruktur: Pengembangan dan pengujian dilakukan pada lingkungan *cloud* Google Colab (Free) dan mesin lokal dengan GPU setara NVIDIA T4/RTX 3050\.  
* Fokus Evaluasi: Evaluasi ditekankan pada akurasi retrieval (Top-K) dan kualitas semantik hasil generasi, bukan pada optimasi latensi tingkat produksi (*production-grade latency*).

## **2\. TINJAUAN PUSTAKA DAN LANDASAN TEORI**

Bagian ini menguraikan fondasi teoritis yang mendasari arsitektur sistem yang diusulkan, mencakup evolusi embedding multimodal, mekanisme pencarian vektor, dan paradigma RAG.

### **2.1 Multimodal Embedding dan CLIP (Contrastive Language-Image Pre-training)**

Sistem temu kembali citra konvensional sering kali bergantung pada ekstraksi fitur visual menggunakan Convolutional Neural Networks (CNN) seperti ResNet atau VGG yang dilatih pada dataset klasifikasi ImageNet. Pendekatan ini memiliki kelemahan fundamental: model hanya mampu mengenali objek yang termasuk dalam kelas label tertutup (*closed-set labels*) yang dipelajari selama pelatihan. Model ini kesulitan memahami konsep abstrak, relasi antar-objek, atau deskripsi bahasa alami yang kompleks.  
CLIP (Contrastive Language-Image Pre-training), yang dikembangkan oleh OpenAI, mengubah paradigma ini dengan memperkenalkan pembelajaran representasi visual melalui supervisi bahasa alami (*natural language supervision*). CLIP dilatih pada 400 juta pasangan (citra, teks) yang dikumpulkan dari internet.2  
Mekanisme inti CLIP adalah Contrastive Learning. Model ini terdiri dari dua enkoder terpisah:

1. Image Encoder: Biasanya berbasis Vision Transformer (ViT), yang memecah citra menjadi *patches* (misalnya 32x32 piksel), lalu memprosesnya melalui lapisan *Self-Attention* untuk menghasilkan vektor representasi visual If.  
2. Text Encoder: Berbasis Transformer, yang memproses urutan token teks menjadi vektor representasi tekstual  Tf.

Tujuan pelatihan CLIP adalah memaksimalkan *Cosine Similarity* antara  If dan  Tf untuk pasangan yang benar (positif) dalam sebuah *batch*, sembari meminimalkan kemiripan untuk pasangan yang salah (negatif). Secara matematis, ini menciptakan ruang laten bersama (*shared latent space*) di mana vektor gambar "anjing" akan berada sangat dekat secara geometris dengan vektor teks "a dog". Properti inilah yang memungkinkan kita melakukan *Zero-Shot Retrieval*: mencari gambar berdasarkan deskripsi teks sembarang tanpa perlu melatih ulang model untuk label tertentu.

### **2.2 Vector Database dan FAISS**

Setelah representasi vektor diperoleh dari CLIP (umumnya berdimensi 512 atau 768), tantangan berikutnya adalah pencarian. Mencari vektor yang paling mirip dengan vektor kueri dalam dataset besar memerlukan biaya komputasi yang tinggi jika dilakukan dengan metode *brute-force* ([![][image1]](https://www.codecogs.com/eqnedit.php?latex=O\(N\)#0)), di mana jarak dihitung satu per satu terhadap seluruh [![][image2]](https://www.codecogs.com/eqnedit.php?latex=N#0) data.  
FAISS (Facebook AI Similarity Search) adalah pustaka yang dirancang untuk mengatasi masalah skalabilitas ini. FAISS menyediakan berbagai struktur indeksasi untuk mempercepat pencarian tetangga terdekat (*Nearest Neighbor Search*).

* IndexFlatIP / IndexFlatL2: Metode eksak (*brute-force*) yang sangat akurat tetapi lambat untuk dataset jutaan data. Namun, untuk skala proyek ini (10.000 data), metode ini masih sangat cepat dan memberikan akurasi maksimum (Ground Truth).  
* IVF (Inverted File Index): Membagi ruang vektor menjadi sel-sel Voronoi. Pencarian hanya dilakukan pada sel yang relevan, mempercepat proses secara drastis dengan sedikit pengorbanan akurasi.  
* HNSW (Hierarchical Navigable Small World): Struktur berbasis graf yang memungkinkan navigasi cepat menuju tetangga terdekat, sangat populer untuk aplikasi *real-time*.5

Dalam proyek ini, integrasi FAISS dengan embedding CLIP memungkinkan sistem melakukan kueri semantik seperti "suasana pasar yang ramai di malam hari" dan mendapatkan hasil visual yang relevan dalam hitungan milidetik.

### **2.3 Retrieval-Augmented Generation (RAG)**

RAG adalah kerangka kerja yang menghubungkan model generatif (seperti LLM) dengan memori eksternal. Dalam konteks LLM tradisional, pengetahuan model "dibekukan" pada saat pelatihan selesai. RAG memungkinkan model mengakses data terkini atau data spesifik (proprietary) tanpa perlu pelatihan ulang.  
Arsitektur RAG umumnya terdiri dari tiga komponen utama:

1. Retriever: Bertugas mengambil dokumen atau data yang relevan dari basis pengetahuan eksternal berdasarkan kueri pengguna. Metrik keberhasilan komponen ini diukur dengan *Recall* dan *Precision*.3  
2. Context Builder: Bertugas menggabungkan kueri asli dengan data yang ditemukan (*retrieved context*) menjadi satu *prompt* terstruktur.  
3. Generator: Model generatif (LLM atau Image Generator) yang memproses *prompt* tersebut untuk menghasilkan jawaban atau konten baru.

Keunggulan utama RAG adalah Verifiability (pengguna dapat melihat sumber data yang digunakan model) dan Extensibility (basis pengetahuan dapat diperbarui kapan saja hanya dengan menambah data ke indeks vektor). Dalam proyek ini, RAG diperluas menjadi Multimodal RAG, di mana "dokumen" yang dicari bukan hanya teks, tetapi juga citra, dan "konteks" yang diberikan ke generator mencakup deskripsi visual dari citra tersebut.7

### **2.4 Generative AI: LLM dan Stable Diffusion**

* Large Language Models (LLM): Model seperti GPT-4 atau Llama 3 bekerja dengan memprediksi token berikutnya berdasarkan probabilitas statistik. Dalam sistem RAG, LLM berfungsi sebagai "narator" yang merajut informasi terfragmentasi dari hasil retrieval menjadi cerita atau penjelasan yang koheren.  
* Stable Diffusion: Merupakan model generatif berbasis difusi laten (*Latent Diffusion Models*). Model ini bekerja dengan cara membalikkan proses difusi (menghilangkan *noise* dari gambar acak) secara bertahap, dipandu oleh *embedding* teks (prompt). Dalam proyek ini, Stable Diffusion berfungsi sebagai "ilustrator" yang memvisualisasikan narasi atau konsep yang telah diperkaya oleh proses retrieval.2

## **3\. METODOLOGI DAN ARSITEKTUR SISTEM**

Bagian ini menjelaskan secara rinci desain arsitektur sistem, komponen-komponen penyusun, serta alur data dari input pengguna hingga output akhir. Pendekatan yang digunakan bersifat modular, memungkinkan setiap komponen untuk dievaluasi atau diganti secara independen.

### **3.1 Gambaran Umum Arsitektur (High-Level Architecture)**

Arsitektur sistem dirancang mengikuti pola *Retriever-Reader/Generator*. Secara konseptual, sistem terbagi menjadi dua fase utama: fase *offline* (persiapan data) dan fase *online* (interaksi pengguna).  
![][image3]  
Gambar 1\. Blueprint: Overall System Architecture (Rag Multimodal)  
Alur Kerja Fase Offline (Indexing):

1. Dataset Ingestion (MS COCO).  
2. Preprocessing (Resize, Normalisasi).  
3. Feature Extraction (CLIP Encoder).  
4. Vector Indexing (FAISS Construction).  
5. Metadata Storage (Mapping ID ke Caption).

Alur Kerja Fase Online (Inference):

1. User Query Processing (Text/Image).  
2. Query Embedding (CLIP Encoder).  
3. Similarity Search (FAISS Retrieval).  
4. Context Aggregation.  
5. Generative Augmentation (LLM & Stable Diffusion).  
6. Response Rendering (Streamlit UI).

### **3.2 Komponen 1: Manajemen Dataset dan Preprocessing**

Dataset: MS COCO Captions 2017.2  
Mengingat keterbatasan komputasi, kami menerapkan teknik sampling untuk mengambil subset data.

* Total Data: Kami akan mengambil sampel acak sebanyak 10.000 pasang gambar-caption. Jumlah ini dipilih sebagai keseimbangan antara keragaman data (untuk retrieval yang bermakna) dan kecepatan indeksasi.  
* Struktur Data:  
  * Folder *images*/: Berisi file.jpg.  
  * File captions.json: Berisi metadata *{image\_id, file\_name, caption}*.

Proses Preprocessing:  
Kualitas data input sangat menentukan kualitas embedding. Langkah-langkah preprocessing meliputi:

1. Resizing & Center Cropping: Mengubah dimensi citra menjadi [![][image4]](https://www.codecogs.com/eqnedit.php?latex=224%20%5Ctimes%20224#0) piksel. Ini adalah resolusi standar input untuk model CLIP ViT-B/32. Center cropping memastikan objek utama (yang biasanya di tengah) tetap terjaga aspek rasionya.  
2. Normalisasi Tensor: Mengkonversi nilai piksel (0-255) ke rentang tensor *float* (0.0-1.0), kemudian melakukan normalisasi menggunakan nilai rata-rata (*mean*) dan standar deviasi (*std*) dari dataset ImageNet:  
   * Mean: \[0.48145466, 0.4578275, 0.40821073\]  
   * Std: \[0.26862954, 0.26130258, 0.27577711\]  
     Normalisasi ini krusial agar input sesuai dengan distribusi data yang dilihat model saat pelatihan awal.  
3. Text Tokenization: Untuk caption, teks dibersihkan (lowercase, remove special chars) dan ditokenisasi menggunakan tokenizer BPE (*Byte Pair Encoding*) bawaan CLIP dengan panjang maksimum konteks 77 token.

### **3.3 Komponen 2: Feature Extraction (Embedding)**

Pada tahap ini, data mentah diubah menjadi representasi matematis. Kami menggunakan model openai/clip-vit-base-patch32 karena keseimbangan performa dan efisiensi.2  
Proses Teknis:

* Setiap citra *I* diproses oleh CLIP Image Encoder  EI menghasilkan vektor [![][image5]](https://www.codecogs.com/eqnedit.php?latex=v_I%20%5Cin%20%5Cmathbb%7BR%7D%5E%7B512%7D#0).  
* Setiap teks caption [![][image6]](https://www.codecogs.com/eqnedit.php?latex=T#0) diproses oleh CLIP Text Encoder [![][image7]](https://www.codecogs.com/eqnedit.php?latex=E_T#0) menghasilkan vektor [![][image8]](https://www.codecogs.com/eqnedit.php?latex=v_T%20%5Cin%20%5Cmathbb%7BR%7D%5E%7B512%7D#0).  
* Penting: Seluruh vektor hasil ekstraksi akan dinormalisasi menggunakan L2-normalization ([![][image9]](https://www.codecogs.com/eqnedit.php?latex=v%20%5Cleftarrow%20%5Cfrac%7Bv%7D%7B%7C%7Cv%7C%7C%7D#0)). Langkah ini sangat penting agar perhitungan *Dot Product* di tahap selanjutnya ekuivalen dengan *Cosine Similarity*.

Hasil dari tahap ini adalah matriks embedding citra berukuran [![][image10]](https://www.codecogs.com/eqnedit.php?latex=\(10.000%20%5Ctimes%20512\)#0) yang disimpan dalam format .npy (NumPy binary) untuk efisiensi pemuatan ulang.

### **3.4 Komponen 3: Retrieval Engine (FAISS)**

FAISS digunakan untuk menyimpan dan mencari vektor. Kami memilih tipe indeks IndexFlatIP (*Inner Product*). Justifikasi Pemilihan IndexFlatIP:  
Karena vektor telah dinormalisasi L2, jarak Cosine Similarity antara dua vektor [![][image11]](https://www.codecogs.com/eqnedit.php?latex=u#0) dan [![][image12]](https://www.codecogs.com/eqnedit.php?latex=v#0) dapat dihitung hanya dengan Dot Product ([![][image13]](https://www.codecogs.com/eqnedit.php?latex=u%20%5Ccdot%20v#0)). IndexFlatIP melakukan perhitungan exact search menggunakan produk titik ini. Untuk 10.000 data, pencarian brute-force ini masih sangat cepat (\< 50ms) dan menjamin akan mendapatkan hasil yang 100% akurat (True Nearest Neighbors), berbeda dengan metode aproksimasi (ANN) seperti HNSW yang mungkin memiliki recall loss kecil.  
Mekanisme Query:

1. Kueri pengguna dikonversi menjadi vektor [![][image14]](https://www.codecogs.com/eqnedit.php?latex=v_q#0) (menggunakan Text Encoder jika input teks, atau Image Encoder jika input gambar).  
2. Vektor [![][image15]](https://www.codecogs.com/eqnedit.php?latex=v_q#0) dinormalisasi L2.  
3. FAISS melakukan operasi [![][image16]](https://www.codecogs.com/eqnedit.php?latex=D%2C%20I%20%3D%20index.search\(v_q%2C%20k%3D5\)#0), di mana [![][image17]](https://www.codecogs.com/eqnedit.php?latex=D#0) adalah jarak (skor kemiripan) dan [![][image18]](https://www.codecogs.com/eqnedit.php?latex=I#0) adalah indeks (ID) dari 5 gambar teratas.

### **3.5 Komponen 4: Generative Augmentation (RAG)**

Setelah mendapatkan Top-K gambar dan caption-nya, sistem membangun konteks untuk generasi.  
A. Text Generation Pipeline (LLM)  
Kami menggunakan pendekatan prompt injection. Caption dari gambar yang ditemukan (retrieved captions) digabungkan menjadi sebuah blok konteks.

* Prompt Template:  
  Role: You are a visual assistant that describes scenes based on retrieved evidence.  
  User Query: {user\_query}  
  Context from Retrieval (Do not hallucinate, use these facts):  
  1. Image A shows: {caption\_1}  
  2. Image B shows: {caption\_2}  
  3. Image C shows: {caption\_3}

Task: Synthesize a coherent, detailed paragraph describing the visual scene requested by the user, incorporating elements from the context above.

* Model yang digunakan: GPT-4o-mini (via API) atau Llama-3-8B (lokal/HuggingFace). LLM ini dipilih karena kemampuannya dalam *instruction following* yang kuat.2

B. Image Generation Pipeline (Stable Diffusion)  
Untuk generasi citra, kami mengimplementasikan dua mode:

1. Refined T2I (Text-to-Image): Prompt pengguna diperkaya dengan kata kunci yang ditemukan dari retrieval. Misalnya, jika pengguna mencari "mobil cepat" dan retrieval menemukan "Ferrari merah di trek balap", prompt ke Stable Diffusion diubah menjadi "A fast car, red Ferrari, racing track, highly detailed, photorealistic, 4k". Ini disebut *Prompt Expansion*.  
2. I2I (Image-to-Image): Menggunakan salah satu gambar hasil retrieval (misalnya gambar dengan skor tertinggi) sebagai *initial image*. Stable Diffusion akan melakukan *denoising* ulang pada gambar ini dengan kekuatan (*strength*) tertentu (misal 0.75). Ini menghasilkan variasi baru yang mempertahankan komposisi asli gambar retrieval tetapi dengan gaya atau detail baru sesuai prompt.2

## **4\. RENCANA IMPLEMENTASI TEKNIS**

Bagian ini merinci langkah-langkah implementasi praktis, termasuk struktur direktori, kebutuhan sistem.

### **4.1 Lingkungan Pengembangan (Development Environment)**

Mengingat kebutuhan akan akselerasi GPU untuk CLIP dan Stable Diffusion, pengembangan utama akan dilakukan di Google Colab (Pro) atau workstation lokal dengan spesifikasi minimal:

* CPU: 4 Cores.  
* RAM: 16GB (penting untuk memuat dataset dan indeks FAISS).  
* GPU: NVIDIA T4 (16GB VRAM) atau setara. VRAM minimal 8GB dibutuhkan untuk memuat Stable Diffusion model secara nyaman.  
* Bahasa: Python 3.9+.  
* Library Utama: torch, transformers, diffusers, faiss-cpu (atau faiss-gpu), streamlit, clip-openai.

### **4.2 Struktur Proyek**

Struktur folder yang rapi sangat penting untuk kolaborasi tim. Berikut adalah rancangan struktur direktori proyek 2:

| multimodal-rag-project/├── data/│   ├── raw/                  \# Dataset asli (images, json)│   ├── processed/            \# Hasil resize, npy arrays│   └── embeddings/           \# File vektor (image\_feats.npy)├── src/│   ├── preprocessing.py      \# Script normalisasi & loading│   ├── embedding.py          \# Script CLIP encoder│   ├── retrieval.py          \# Class wrapper untuk FAISS│   ├── generation.py         \# Integrasi LLM & Stable Diffusion│   └── utils.py              \# Fungsi bantu (logging, config)├── app.py                    \# Main Streamlit application├── requirements.txt          \# Daftar dependensi├── README.md                 \# Dokumentasi└── notebooks/                \# Jupyter notebooks untuk eksperimen |
| :---- |

### **4.3 Alur Implementasi (Step-by-Step)**

#### Tahap 1: Persiapan Data (Minggu 1\)

* Mengunduh train2017.zip dan annotations\_trainval2017.zip dari website COCO.  
* Menjalankan skript preprocessing.py untuk memilih 10.000 gambar secara acak.  
* Mengekstrak caption dari JSON dan menyimpannya dalam format dictionary: {image\_filename: \[list\_of\_captions\]}.

#### Tahap 2: Pembangunan Indeks (Minggu 2\)

* Mengimplementasikan embedding.py. Memuat model CLIP.  
* Melakukan *batch processing* (misal: batch size 32\) untuk mengonversi 10.000 gambar menjadi matriks embedding.  
* Menyimpan matriks ke data/embeddings/features.npy.  
* Mengimplementasikan retrieval.py. Memuat matriks .npy, membangun faiss.IndexFlatIP, dan menambah vektor ke dalamnya. Fungsi pencarian harus menerima teks/gambar dan mengembalikan daftar nama file gambar.

#### Tahap 3: Integrasi Generatif (Minggu 3\)

* Integrasi LLM. Membuat fungsi generate\_description(query, context\_captions). Kami akan bereksperimen dengan *temperature* (misal 0.7) untuk menyeimbangkan kreativitas dan fakta.  
* Integrasi Stable Diffusion. Menggunakan *StableDiffusionPipeline* dari Hugging Face. Mengimplementasikan logika untuk memilih antara mode T2I atau I2I.

#### Tahap 4: Pengembangan UI & Integrasi Akhir (Minggu 4\)

* Membuat app.py dengan Streamlit.  
* Menghubungkan input UI ke fungsi backend.  
* Menambahkan fitur visualisasi seperti *slider* untuk parameter generasi dan galeri grid untuk hasil retrieval.

## **5\. STRATEGI EVALUASI DAN MATRIKS PENGUKURAN**

Evaluasi sistem RAG multimodal memerlukan pendekatan multidimensi yang mencakup kinerja retrieval (ketepatan pencarian) dan kinerja generasi (kualitas konten yang dibuat). Kami akan menggunakan kombinasi metrik kuantitatif otomatis dan evaluasi kualitatif (manusia/model).3

### **5.1 Evaluasi Komponen Retrieval**

Karena dataset COCO memiliki *ground truth* (kategori dan caption), kita dapat mengukur seberapa akurat sistem menemukan gambar yang relevan.  
Metrik Utama:

1. Recall@K (R@K):  
   Ini adalah metrik standar emas dalam IR. Mengukur persentase item relevan yang muncul dalam daftar K hasil teratas.  
   [![][image19]](https://www.codecogs.com/eqnedit.php?latex=%20%5Ctext%7BRecall%40K%7D%20%3D%20%5Cfrac%7B%5Ctext%7BJumlah%20item%20relevan%20di%20Top-K%7D%7D%7B%5Ctext%7BTotal%20item%20relevan%20dalam%20database%7D%7D%20#0)  
   Dalam konteks ini, sebuah gambar dianggap relevan jika caption-nya memiliki overlap kata benda (noun overlap) signifikan dengan kueri, atau jika kueri adalah caption asli dari gambar tersebut. Kami menargetkan Recall@5 \> 0.6.  
2. Precision@K (P@K):  
   Mengukur seberapa banyak "sampah" (hasil tidak relevan) yang ada di halaman pertama.  
   [![][image20]](https://www.codecogs.com/eqnedit.php?latex=%5Ctext%7BPrecision%40K%7D%20%3D%20%5Cfrac%7B%5Ctext%7BJumlah%20item%20relevan%20di%20Top-K%7D%7D%7BK%7D#0)  
   Precision yang tinggi penting untuk kepercayaan pengguna. Jika pengguna mencari "kucing" dan 3 dari 5 gambar pertama adalah "anjing", kepercayaan akan turun.1  
3. Mean Reciprocal Rank (MRR):  
   Metrik ini memberi bobot lebih pada urutan. Jika hasil yang benar ada di posisi 1, skornya 1\. Jika di posisi 2, skornya 0.5. Jika di posisi 5, skornya 0.2. MRR sangat penting untuk sistem yang hanya menampilkan satu hasil utama.  
   [![][image21]](https://www.codecogs.com/eqnedit.php?latex=%5Ctext%7BMRR%7D%20%3D%20%5Cfrac%7B1%7D%7B%7CQ%7C%7D%20%5Csum_%7Bi%3D1%7D%5E%7B%7CQ%7C%7D%20%5Cfrac%7B1%7D%7B%5Ctext%7Brank%7D_i%7D#0)  
4. Retrieval Latency:  
   Kami akan mengukur waktu rata-rata (ms) untuk proses retrieval (Encoding \+ FAISS Search). Target: \< 200ms per kueri.

### **5.2 Evaluasi Komponen Generatif (Teks)**

Evaluasi teks generatif lebih sulit karena sifatnya yang terbuka. Kami mengadopsi kerangka evaluasi modern RAGAS (Retrieval Augmented Generation Assessment) yang menggunakan LLM sebagai juri (*LLM-as-a-judge*).10

1. Faithfulness (Kesetiaan):  
   Mengukur apakah jawaban yang dihasilkan hanya berasal dari konteks yang diberikan. Juri LLM akan memeriksa setiap klaim dalam teks hasil generasi dan memverifikasinya terhadap retrieved captions. Skor tinggi berarti rendah halusinasi.3  
2. Answer Relevance:  
   Mengukur seberapa relevan jawaban terhadap kueri awal pengguna, terlepas dari kebenaran faktanya.  
3. Context Precision:  
   Mengukur rasio signal-to-noise dalam konteks yang diambil. Apakah caption yang diambil benar-benar berguna untuk menjawab kueri?

### **5.3 Evaluasi Komponen Generatif (Citra)**

Untuk mengevaluasi kualitas gambar yang dihasilkan oleh Stable Diffusion dalam konteks RAG:

1. CLIP Score:  
   Ini adalah metrik otomatis referensi-bebas (reference-free). Kami menghitung Cosine Similarity antara vektor kueri teks pengguna dan vektor gambar yang dihasilkan oleh Stable Diffusion menggunakan model CLIP.  
   [![][image22]](https://www.codecogs.com/eqnedit.php?latex=%5Ctext%7BCLIP%20Score%7D\(I%2C%20T\)%20%3D%20%5Ctext%7BCosine%7D\(E_I\(I\)%2C%20E_T\(T\)\)#0)  
   Skor yang tinggi (mendekati 1\) menunjukkan bahwa gambar sangat merepresentasikan teks input. Ini mengukur Image Coherence dan keselarasan semantik.12  
2. Multimodal Faithfulness:  
   Evaluasi kualitatif untuk memeriksa apakah elemen visual kunci yang diminta (misal: "payung merah") benar-benar muncul dalam gambar, dan apakah tidak ada elemen aneh (misal: orang berkepala tiga) yang muncul.4

## **6\. MANAJEMEN PROYEK**

Keberhasilan proyek teknis yang kompleks sangat bergantung pada pembagian peran yang jelas dan manajemen waktu yang disiplin. Mengacu pada praktik terbaik dalam tim Data Science dan AI 16, kami menetapkan struktur tim dan *timeline* sebagai berikut.

### **6.1 Struktur Tim dan Pembagian Tugas**

Kami mengasumsikan tim terdiri dari 4 anggota dengan peran spesialisasi "T-shaped" (memiliki keahlian mendalam di satu bidang, namun mampu memahami bidang lain).  
Tabel 1\. Pembagian Jobdesk dalam Pengerjaan Proyek Multimodal RAG

| Peran | Tanggung Jawab Utama  | Output Kunci |
| :---- | :---- | :---- |
| Project Manager & AI Architect | Tanggung Jawab: Orkestrasi tim, desain sistem level tinggi, manajemen risiko, penulisan laporan akhir. Memastikan keselarasan antara tujuan bisnis (tugas kuliah) dan teknis. | Proposal, Laporan Akhir, Arsitektur Diagram, Slide Presentasi. |
| Data Engineer | Tanggung Jawab: Membangun *pipeline* data yang robust. Menangani unduhan dataset besar, *cleaning*, normalisasi, dan manajemen penyimpanan vektor (FAISS). Memastikan data mengalir lancar dari raw ke embedding.  | Skrip preprocessing.py, Database Vektor (index.bin), Modul Dataloader. |
| Machine Learning Engineer (RAG Specialist) | Tanggung Jawab: Implementasi inti model AI. Menangani model CLIP, integrasi LLM, *Prompt Engineering*, dan optimasi inferensi Stable Diffusion. Fokus pada kualitas model dan metrik evaluasi. | Skrip retrieval.py, generation.py, Laporan Evaluasi Metrik. |
| Full Stack AI Developer (Frontend/UI) | Tanggung Jawab: Mengubah kode Python backend menjadi aplikasi web yang dapat digunakan. Membangun UI Streamlit, menangani interaksi user, dan visualisasi hasil. | Aplikasi Web (app.py), Video Demo. |

### **6.2 Timeline Pengerjaan (4 Minggu)**

Kami mengadopsi metodologi Agile dengan *sprint* mingguan. Mengingat durasi proyek yang pendek (approx. 1 bulan), kecepatan eksekusi dan iterasi sangat krusial.2

#### Minggu 1: Fondasi dan Data (25 Nov \- 1 Des)

* Fokus: Setup infrastruktur dan penyiapan data.  
* Kegiatan:  
  * Kick-off meeting: Finalisasi pembagian tugas.  
  * Setup Google Drive/Colab Environment dan Git Repository.  
  * Download Dataset COCO (subset 10k).  
  * Eksperimen awal dengan notebook CLIP untuk memastikan library berfungsi.  
* Milestone: Repositori siap, data *preprocessed* tersedia.

#### Minggu 2: Core Retrieval Implementation (2 Des \- 7 Des)

* Fokus: Membangun mesin pencari (Retriever).  
* Kegiatan:  
  * Generate embedding untuk 10k gambar (proses batch).  
  * Implementasi FAISS Indexing (FlatIP).  
  * Membuat fungsi pencarian dasar (input teks \-\> output list ID gambar).  
  * Mempersiapkan Demo Progress (8 Des).  
* Milestone: Sistem mampu menerima kueri dan mengembalikan gambar relevan.

#### Minggu 3: Generative Integration & UI (8 Des \- 14 Des)

* Fokus: Menghubungkan otak (LLM/SD) dan wajah (UI).  
* Kegiatan:  
  * Integrasi API LLM untuk *captioning*.  
  * Integrasi Stable Diffusion untuk *image generation*.  
  * Membangun UI Streamlit v1.0 (Input \+ Gallery \+ Output).  
  * Iterasi *prompt engineering* untuk meningkatkan kualitas hasil.  
* Milestone: Aplikasi *end-to-end* berjalan, fitur lengkap.

#### Minggu 4: Evaluasi dan Finalisasi (15 Des \- 21 Des)

* Fokus: Pengujian, perbaikan bug, dan dokumentasi.  
* Kegiatan:  
  * Menjalankan skrip evaluasi otomatis (Recall@K, CLIP Score).  
  * Melakukan *user testing* internal.  
  * Menulis Laporan Akhir Final Project.  
  * Membuat Slide Presentasi dan Video Demo.  
* Milestone: Semua *deliverables* siap untuk Demo Final (22 Des).

## **7\. HASIL ANTAR MUKA YANG DIHARAPKAN**

Antarmuka pengguna (UI) adalah jembatan vital antara kompleksitas algoritma dan pengguna. Kami merancang UI berbasis Streamlit yang memprioritaskan kejelasan dan interaktivitas. Berikut adalah spesifikasi fungsional dari antarmuka yang akan dibangun 2:  
![][image23]  
Gambar 2\. Prototype Halaman Home UI Multimodal RAG System  
![][image24]  
Gambar 3\. Prototype Halaman Generative UI Multimodal RAG System

1. Halaman Utama (Dashboard):  
   * Header: Judul proyek dan deskripsi singkat.  
   * Input Panel (Sidebar/Top):  
     * Tab "Text Search": Kotak input teks untuk kueri natural (misal: "Pemandangan pantai saat matahari terbenam").  
     * Tab "Image Search": Widget *file uploader* (mendukung JPG/PNG) untuk pencarian berbasis gambar (*visual search*).  
   * Settings Panel (Sidebar):  
     * Slider Top-K Retrieval: Mengatur jumlah gambar yang diambil (Default: 5).  
     * Slider Creativity (Temperature): Mengatur parameter LLM.  
     * Checkbox Enable Image Generation: Opsi untuk menyalakan/mematikan Stable Diffusion (untuk menghemat waktu jika hanya butuh pencarian).  
2. Area Hasil (Main Content):  
   * Section 1: Retrieval Results (Evidence): Menampilkan galeri grid (baris berisi gambar) dari Top-K hasil pencarian. Di bawah setiap gambar, ditampilkan skor kemiripan (misal: "Similarity: 85%") dan *caption* asli dari COCO. Ini memberikan transparansi kepada pengguna mengenai data apa yang menjadi dasar jawaban sistem.  
   * Section 2: Generative Insight (LLM): Menampilkan kotak teks berisi narasi deskriptif yang dihasilkan oleh LLM. Teks ini mensintesis informasi visual dari gambar-gambar di atas menjadi satu paragraf yang koheren.  
   * Section 3: Visual Synthesis (Stable Diffusion): Menampilkan satu atau lebih gambar baru yang dihasilkan oleh AI. Gambar ini adalah interpretasi visual baru berdasarkan gabungan kueri pengguna dan konteks yang ditemukan.

## **8\. KESIMPULAN**

Proposal ini menyajikan rancangan komprehensif untuk pengembangan sistem "Multimodal Retrieval-Augmented Generation (RAG) Berbasis Citra". Proyek ini tidak hanya memenuhi persyaratan akademis mata kuliah Image Retrieval, tetapi juga mengeksplorasi batas-batas teknologi AI modern dengan menggabungkan kekuatan representasi semantik CLIP, efisiensi pencarian vektor FAISS, dan kreativitas model generatif.  
Dengan metodologi yang terstruktur, mulai dari kurasi dataset MS COCO, arsitektur modular yang memisahkan *retriever* dan *generator*, hingga strategi evaluasi yang ketat menggunakan metrik industri, kami optimis dapat menghasilkan sebuah prototipe yang fungsional, inovatif, dan bernilai edukatif tinggi. Keberhasilan proyek ini akan mendemonstrasikan bagaimana AI dapat tidak hanya mencari informasi, tetapi juga memahami dan mencipta ulang realitas visual dengan cara yang terverifikasi dan kontekstual.

#### **REFERENSI** 
