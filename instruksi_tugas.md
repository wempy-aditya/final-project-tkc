> **Final** **Project**
>
> **Tujuan** **Final** **Project**
>
> Mahasiswa mampu merancang dan mengimplementasikan sistem Retrieval
> AugmentedGeneration (RAG) berbasis citra, yang menggabungkan:
>
> 1\. Temu kembali citra (image retrieval) untuk mencari gambar relevan
> berdasarkan query teks atau citra.
>
> 2\. Model generatif (text or image generation) untuk menghasilkan
> deskripsi, narasi, ataugambar serupa berbasis hasil retrieval.
>
> **KomponenFinal** **Project**
>
> 1\. Dataset
>
> Boleh menggunakan dataset publik (sepertiCIFAR, ImageNet subset, Batik
> dataset 960, Fashion-MNIST, COCO Captions, dll).
>
> 2\. Feature Extraction /Embedding
>
> a\. Gunakan model pretrained seperti: i. CLIP (OpenAI)
>
> ii\. ResNet50 atau ViT
>
> iii\. BLIP untuk multimodal retrieval
>
> b\. Simpan embedding di FAISS atau milvus database atau sejenisnya. 3.
> Retrieval Engine
>
> a\. Implementasikan *vector* *search*(cosine similarity, Euclidean,
> atau dot product).
>
> b\. Tampilkan top-k hasil citra relevan. 4. Generative Component
>
> a\. Gunakan model generatif berbasis teks atau multimodal, misalnya:
> i. GPT-4-turbo, Llama 3, atau Flan-T5
>
> ii\. BLIP-2 untukimage captioning
>
> iii\. Stable Diffusion atau SDXL untuk image generation
>
> b\. Generator harus menggunakan hasil retrieval sebagai*context*untuk
> menghasilkan teks/citra baru.
>
> 5\. User Interface
>
> a\. Web UI sederhana menggunakan Streamlit, Gradio, atau Hugging face.
> b. Input: gambar atau teks query.
>
> c\. Output: hasil citra relevan dan teks hasilgenerative atau image
> hasil generative.

**Instruksi**

> 1\. Final projectdikerjakan secara berkelompok 3-5 orang
>
> 2\. Proposal dipresentasikan oleh setiap anggota kelompokSenin **24**
> **November** **2025**meliputi:
>
> a\. Judul
>
> b\. Deskripsi c. Dataset
>
> d\. Metodologi RAG (Gambaran arsitektur /pipeline) i. Image Retrieval
>
> ii\. Generative
>
> e\. Matrix pengukuran performa
>
> f\. Hasilantar muka yang diharapkan g. Pembagian tugas anggota
> kelompok h. Timeline pengerjaaanfinal project
>
> 3\. Demo Progress: **8** **Desember** **2025** 4. Demo Final: **22**
> **Desember** **2025**
>
> 5\. **Nilai** **UAS** diambil dari nilai**Final** **Project**
