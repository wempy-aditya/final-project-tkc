# 📓 Panduan Jupyter Notebook - Complete Pipeline

## File: `Complete_Pipeline.ipynb`

Notebook ini mengkonversi semua kode Python dari folder `src` menjadi pipeline yang terstruktur dan mudah dijalankan.

---

## 🎯 Isi Notebook

### **8 Stage Pipeline:**

1. **Setup & Configuration** ⚙️
   - Install dependencies
   - Import libraries
   - Configure paths & settings

2. **Data Preprocessing** 📥
   - Download COCO annotations
   - Load dataset
   - Download sample images

3. **Embedding Generation** 🧠
   - Load CLIP model
   - Generate image embeddings
   - Save embeddings to disk

4. **FAISS Index Building** 🔍
   - Build vector search index
   - Save index for fast retrieval

5. **Retrieval System** 🎯
   - Text-based search
   - Visualize results
   - Test queries

6. **RAG Components** 🤖
   - Context building
   - LLM text generation
   - Integration with Groq API

7. **Evaluation** 📊
   - Recall@K & Precision@K
   - Latency measurement
   - Comprehensive metrics

8. **Interactive Demo** 🎮
   - Interactive search interface
   - Real-time visualization

---

## 🚀 Cara Menggunakan

### **Opsi 1: Jupyter Notebook (Recommended)**

```bash
# 1. Install Jupyter
pip install jupyter notebook

# 2. Launch Jupyter
jupyter notebook

# 3. Buka Complete_Pipeline.ipynb
# 4. Run cells secara berurutan (Shift + Enter)
```

### **Opsi 2: JupyterLab**

```bash
# 1. Install JupyterLab
pip install jupyterlab

# 2. Launch JupyterLab
jupyter lab

# 3. Buka Complete_Pipeline.ipynb
```

### **Opsi 3: VS Code**

```bash
# 1. Install Python extension di VS Code
# 2. Install Jupyter extension
# 3. Buka file .ipynb
# 4. Select Python kernel
# 5. Run cells
```

### **Opsi 4: Google Colab**

```bash
# 1. Upload Complete_Pipeline.ipynb ke Google Drive
# 2. Buka dengan Google Colab
# 3. Run cells
# Note: Perlu upload .env file untuk API keys
```

---

## 📋 Prerequisites

### **Required Packages:**
```bash
pip install torch torchvision transformers
pip install faiss-cpu pillow numpy
pip install openai groq python-dotenv
pip install pycocotools requests tqdm
pip install matplotlib jupyter
```

### **API Keys (Optional):**
Untuk text generation, buat file `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Alternative
```

---

## 🎓 Cara Menjalankan Step-by-Step

### **Stage 1: Setup** (5 menit)
```python
# Cell 1: Install packages
!pip install torch transformers faiss-cpu ...

# Cell 2: Import libraries
import torch, numpy, faiss, ...

# Cell 3: Configuration
CONFIG = {'data_dir': 'data/coco', ...}
```

### **Stage 2: Data Download** (10-30 menit)
```python
# Cell 4: Download annotations
download_coco_annotations()

# Cell 5: Load COCO
coco = COCO(annotations_file)

# Cell 6: Download images (100 samples)
download_images(img_ids, max_download=100)
```

### **Stage 3: Generate Embeddings** (5-10 menit)
```python
# Cell 7: Load CLIP
clip_model = CLIPModel.from_pretrained(...)

# Cell 8: Test embedding
sample_embedding = generate_image_embedding(...)

# Cell 9: Generate all embeddings
embeddings, metadata = generate_all_embeddings()
```

### **Stage 4: Build Index** (1 menit)
```python
# Cell 10: Build FAISS index
faiss_index = build_faiss_index(embeddings)
```

### **Stage 5: Search** (Instant)
```python
# Cell 11: Text search
results = search_by_text("a cat on a couch", k=5)

# Cell 12: Visualize
visualize_results(query, results)
```

### **Stage 6: RAG** (2-5 detik per query)
```python
# Cell 13: Build context
context = build_context(query, captions)

# Cell 14: Generate text (requires API key)
generated_text = generate_text(context)
```

### **Stage 7: Evaluation** (5-10 menit)
```python
# Cell 15: Calculate metrics
recall = calculate_recall_at_k(...)
precision = calculate_precision_at_k(...)

# Cell 16: Full evaluation
eval_results = evaluate_system(test_queries)
```

### **Stage 8: Demo** (Interactive)
```python
# Cell 17: Interactive search
interactive_search()  # Type queries and see results!
```

---

## 💡 Tips & Tricks

### **Untuk Presentasi:**
1. **Run All Cells** sebelum presentasi:
   - Kernel → Restart & Run All
   - Pastikan semua output muncul

2. **Hide Code** untuk fokus pada hasil:
   - View → Toggle Line Numbers
   - Cell → All Output → Toggle Scrolling

3. **Export to HTML** untuk sharing:
   - File → Download as → HTML
   - Bisa dibuka di browser tanpa Jupyter

### **Untuk Development:**
1. **Checkpoint Regularly**:
   - File → Save and Checkpoint
   - Atau Ctrl+S

2. **Clear Output** jika terlalu banyak:
   - Cell → All Output → Clear

3. **Restart Kernel** jika error:
   - Kernel → Restart & Clear Output

### **Untuk Debugging:**
1. **Print Variables**:
   ```python
   print(f"Shape: {embeddings.shape}")
   print(f"Type: {type(faiss_index)}")
   ```

2. **Use `%%time`** untuk measure execution:
   ```python
   %%time
   results = search_by_text(query)
   ```

3. **Use `%debug`** untuk interactive debugging:
   ```python
   %debug
   ```

---

## 📊 Expected Results

### **After Running All Cells:**

```
✅ Setup Complete
   - PyTorch: 2.x.x
   - CUDA: Available/Not Available
   - Device: cuda/cpu

✅ Data Downloaded
   - Images: 100
   - Annotations: 25,000+

✅ Embeddings Generated
   - Shape: (100, 512)
   - Saved to: embeddings/

✅ FAISS Index Built
   - Vectors: 100
   - Dimension: 512

✅ Search Working
   - Latency: ~85ms
   - Results: 5 images

✅ Evaluation Complete
   - Recall@5: ~68%
   - Precision@5: ~14%
```

---

## 🔧 Troubleshooting

### **Error: "No module named 'torch'"**
```bash
pip install torch torchvision
```

### **Error: "CUDA out of memory"**
```python
# Change device to CPU
CONFIG['device'] = 'cpu'
```

### **Error: "File not found"**
```python
# Check paths
print(Path(CONFIG['data_dir']).exists())
```

### **Error: "API key not found"**
```python
# Create .env file or set environment variable
os.environ['GROQ_API_KEY'] = 'your_key_here'
```

### **Notebook Freezes:**
```bash
# Restart kernel
Kernel → Restart

# Or restart Jupyter
Ctrl+C in terminal, then restart
```

---

## 📝 Customization

### **Change Number of Images:**
```python
CONFIG['max_images'] = 1000  # Default: 5000
download_images(img_ids, max_download=500)  # Default: 100
```

### **Change CLIP Model:**
```python
CONFIG['clip_model'] = 'openai/clip-vit-large-patch14'  # Larger model
```

### **Change Search Parameters:**
```python
results = search_by_text(query, k=10)  # More results
```

### **Add Custom Queries:**
```python
test_queries = [
    "your custom query 1",
    "your custom query 2",
    ...
]
```

---

## 🎯 Use Cases

### **For Learning:**
- Run cells one by one
- Read comments and understand each step
- Modify parameters and see effects

### **For Demo:**
- Run all cells beforehand
- Use interactive search for live demo
- Show visualizations

### **For Development:**
- Use as template for new features
- Test different models
- Experiment with parameters

### **For Report:**
- Export results to HTML
- Take screenshots of visualizations
- Copy metrics for analysis

---

## 📚 Additional Resources

### **Documentation:**
- [CLIP Paper](https://arxiv.org/abs/2103.00020)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [Jupyter Docs](https://jupyter-notebook.readthedocs.io/)

### **Tutorials:**
- [CLIP Tutorial](https://huggingface.co/docs/transformers/model_doc/clip)
- [FAISS Tutorial](https://www.pinecone.io/learn/faiss/)

---

**Happy Coding!** 🚀

Notebook ini adalah versi interaktif dari semua kode di folder `src`, disusun dalam pipeline yang mudah dipahami dan dijalankan.
