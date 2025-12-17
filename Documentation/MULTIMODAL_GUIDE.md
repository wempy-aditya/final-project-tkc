# Multimodal Query Feature

## 🎯 Overview

Fitur **multimodal query** memungkinkan Anda untuk mencari gambar menggunakan **text DAN image sekaligus** untuk hasil yang lebih akurat dan relevan.

## ✨ Features

### 3 Query Modes:

1. **Text Only** - Pencarian berdasarkan deskripsi teks
2. **Image Only** - Pencarian berdasarkan gambar referensi
3. **Text + Image (Multimodal)** - Kombinasi keduanya untuk hasil terbaik!

### Fusion Weight Control:

Anda dapat mengatur balance antara text dan image:
- **0.0** = 100% image, 0% text (visual similarity)
- **0.5** = 50% text, 50% image (balanced)
- **1.0** = 100% text, 0% image (semantic similarity)

---

## 🚀 How to Use

### 1. Start the Application

```bash
streamlit run src\ui\app.py
```

### 2. Choose Query Mode

Di UI, pilih salah satu dari 3 mode:
- **Text Only**: Masukkan deskripsi teks saja
- **Image Only**: Upload gambar referensi saja
- **Text + Image (Multimodal)**: Gunakan keduanya!

### 3. Input Your Query

#### For Text Only:
```
Text: "a dog playing in the park"
Image: [disabled]
```

#### For Image Only:
```
Text: [disabled]
Image: [upload dog.jpg]
```

#### For Multimodal:
```
Text: "a dog playing in the park"
Image: [upload dog.jpg]
Weight: 0.5 (balanced)
```

### 4. Adjust Fusion Weight (Multimodal Only)

Gunakan slider untuk mengatur balance:
- **Image-focused (0.0-0.3)**: Prioritas visual similarity
- **Balanced (0.4-0.6)**: Kombinasi seimbang
- **Text-focused (0.7-1.0)**: Prioritas semantic meaning

### 5. Search & Generate

Klik tombol **"🔍 Search & Generate"** untuk:
- Retrieve similar images
- Generate text description
- (Optional) Generate new image

---

## 📊 Use Cases

### Use Case 1: Find Similar Style with Different Subject

**Query:**
- Text: "a cat"
- Image: [photo of a dog in a park]
- Weight: 0.3 (image-focused)

**Result:** Cat photos with similar composition/style to the dog photo

---

### Use Case 2: Find Specific Scene

**Query:**
- Text: "sunset at the beach"
- Image: [photo with orange sky]
- Weight: 0.5 (balanced)

**Result:** Beach sunset photos with orange/warm colors

---

### Use Case 3: Refine Text Search with Visual Example

**Query:**
- Text: "modern architecture"
- Image: [photo of glass building]
- Weight: 0.7 (text-focused)

**Result:** Modern architecture with glass/contemporary style

---

## 🔧 Technical Details

### Embedding Fusion Strategy

The system uses **weighted average fusion**:

```python
fused_embedding = (text_weight × text_embedding) + (image_weight × image_embedding)
```

Where:
- `text_weight` = user-defined (0.0 to 1.0)
- `image_weight` = 1.0 - text_weight
- Result is normalized for cosine similarity

### Why This Works:

1. **CLIP embeddings** are in the same vector space
2. **Text embeddings** capture semantic meaning
3. **Image embeddings** capture visual features
4. **Weighted fusion** combines both modalities
5. **Normalization** ensures valid similarity scores

---

## 💡 Tips for Best Results

### 1. Use Multimodal for Complex Queries

**Instead of:**
- Text: "a dog with brown fur playing with a red ball in a green park"

**Use:**
- Text: "a dog playing"
- Image: [photo showing brown fur, red ball, green grass]
- Weight: 0.5

**Why:** Image provides visual details, text provides context

---

### 2. Adjust Weight Based on Priority

**For style matching:**
- Weight: 0.2-0.3 (image-focused)
- Example: "portrait" + [artistic style reference]

**For concept matching:**
- Weight: 0.7-0.8 (text-focused)
- Example: "celebration" + [party photo]

**For balanced:**
- Weight: 0.5
- Example: "sunset beach" + [orange sky photo]

---

### 3. Combine Abstract Text with Concrete Image

**Good combination:**
- Text: "happiness" (abstract)
- Image: [smiling people] (concrete)

**Result:** Photos of happy moments with similar visual style

---

## 📈 Performance

### Retrieval Speed:

| Mode | Encoding Time | Search Time | Total |
|------|--------------|-------------|-------|
| Text Only | ~50ms | ~10ms | ~60ms |
| Image Only | ~100ms | ~10ms | ~110ms |
| Multimodal | ~150ms | ~10ms | ~160ms |

**Note:** Multimodal is only ~2x slower than text-only but provides much better results!

---

## 🎨 UI Features

### Query Information Display

After search, you'll see:
- **Query Mode**: Which mode you used
- **Text Weight**: Fusion weight (multimodal only)
- **Image Weight**: 1 - text_weight (multimodal only)

### Retrieved Images

- **Rank**: Position in results (1-k)
- **Score**: Similarity score (0-1, higher = more similar)
- **Captions**: Original COCO captions

### Generated Description

LLM-generated description based on:
- Your query (text/image/both)
- Retrieved image captions
- Fusion weight (for multimodal)

---

## 🔬 Advanced Usage

### Programmatic API

You can also use the multimodal search programmatically:

```python
from src.retrieval.retriever import Retriever

retriever = Retriever()

# Multimodal search
results = retriever.search_by_multimodal(
    query_text="a dog in a park",
    query_image="path/to/image.jpg",
    text_weight=0.5,
    k=10
)

# Access results
for result in results['results']:
    print(f"Rank {result['rank']}: {result['file_name']}")
    print(f"Score: {result['similarity_score']:.3f}")
```

### Custom Fusion Strategies

The `_fuse_embeddings()` method can be extended for:
- **Concatenation**: `[text; image]` (requires new index)
- **Attention-based**: Learned weights
- **Adaptive**: Auto-adjust based on query quality

---

## ❓ FAQ

### Q: When should I use multimodal vs single-modal?

**A:** Use multimodal when:
- You have both text description AND visual reference
- Single-modal results are not precise enough
- You want to combine semantic + visual similarity

### Q: What's the best weight setting?

**A:** It depends on your use case:
- **0.5** is a good default (balanced)
- **0.3** for style/composition matching
- **0.7** for concept/semantic matching
- Experiment to find what works best!

### Q: Can I use multimodal without text?

**A:** Yes! Set text_weight=0.0 or leave query_text empty. It will behave like image-only search.

### Q: Can I use multimodal without image?

**A:** Yes! Set text_weight=1.0 or leave query_image empty. It will behave like text-only search.

### Q: Does multimodal work with text generation?

**A:** Yes! The generated description will consider both your text query and image query.

---

## 🐛 Troubleshooting

### Issue: "Please provide both text and image"

**Solution:** In multimodal mode, both inputs are required. Either:
- Provide both text and image, OR
- Switch to "Text Only" or "Image Only" mode

### Issue: Results are too image-focused

**Solution:** Increase text_weight to 0.6-0.8

### Issue: Results are too text-focused

**Solution:** Decrease text_weight to 0.2-0.4

### Issue: Slow performance

**Solution:** 
- Reduce top-k value
- Use faster hardware (GPU)
- Multimodal is inherently slower (encodes both modalities)

---

## 📚 References

- **CLIP Paper**: [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020)
- **Multimodal Fusion**: Weighted average is a simple but effective fusion strategy
- **FAISS**: Efficient similarity search library

---

## 🎯 Next Steps

Try these examples:

1. **Style Transfer Query:**
   - Text: "portrait"
   - Image: [Van Gogh painting]
   - Weight: 0.3

2. **Concept + Visual:**
   - Text: "celebration party"
   - Image: [colorful decorations]
   - Weight: 0.5

3. **Semantic Search:**
   - Text: "teamwork collaboration"
   - Image: [people working together]
   - Weight: 0.7

Enjoy exploring with multimodal search! 🚀
