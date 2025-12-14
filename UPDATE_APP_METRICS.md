# Manual Update Instructions for app.py

Karena file `app.py` cukup panjang, berikut adalah perubahan yang perlu ditambahkan secara manual:

## Step 1: Add Import (Line 12)

Tambahkan setelah `import os`:

```python
import time
```

Dan tambahkan di bagian imports (setelah line 20):

```python
from src.utils.metrics_calculator import MetricsCalculator
```

## Step 2: Update Search Button Handler

Ganti bagian search button handler (mulai dari line ~189) dengan kode berikut:

```python
    # Search button
    if st.button("🔍 Search & Generate", type="primary", use_container_width=True):
        # Validation
        if query_mode == "Text Only" and not query_text:
            st.warning("Please enter a text query")
            return
        if query_mode == "Image Only" and query_image is None:
            st.warning("Please upload an image")
            return
        if query_mode == "Text + Image (Multimodal)":
            if not query_text or query_image is None:
                st.warning("Please provide both text and image for multimodal search")
                return
        
        # Initialize metrics calculator
        calc = MetricsCalculator()
        
        # Start total timer
        total_start = time.time()
        
        # Perform retrieval with timing
        retrieval_start = time.time()
        with st.spinner("Searching for similar images..."):
            if query_mode == "Text Only":
                results = retriever.search_by_text(query_text, k=top_k)
            elif query_mode == "Image Only":
                temp_path = "temp_query.jpg"
                query_image.save(temp_path)
                results = retriever.search_by_image(temp_path, k=top_k)
                os.remove(temp_path)
            else:  # Multimodal
                temp_path = "temp_query.jpg"
                query_image.save(temp_path)
                results = retriever.search_by_multimodal(
                    query_text=query_text,
                    query_image=temp_path,
                    text_weight=text_weight,
                    k=top_k
                )
                os.remove(temp_path)
        
        retrieval_time = time.time() - retrieval_start
        
        # Calculate retrieval metrics
        retrieval_metrics = calc.calculate_retrieval_metrics(results)
```

## Step 3: Add Metrics Display

Tambahkan setelah bagian "Generated Description" (sebelum footer):

```python
        # Calculate total time
        total_time = time.time() - total_start
        
        # Display Metrics & Performance
        st.markdown('<div class="section-header">📊 Metrics & Performance</div>', unsafe_allow_html=True)
        
        with st.expander("📈 View Detailed Metrics", expanded=True):
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            # Retrieval Metrics
            with metric_col1:
                st.markdown("**🔍 Retrieval Quality**")
                st.metric("Avg Similarity", f"{retrieval_metrics['avg_similarity']:.3f}")
                st.metric("Diversity", f"{retrieval_metrics['diversity']:.1%}")
                st.metric("Score Range", f"{retrieval_metrics['min_similarity']:.3f} - {retrieval_metrics['max_similarity']:.3f}")
            
            # Generation Metrics
            with metric_col2:
                st.markdown("**📝 Generation Quality**")
                if text_metrics:
                    st.metric("Word Count", text_metrics['word_count'])
                    st.metric("Sentence Count", text_metrics['sentence_count'])
                    st.metric("Vocabulary", f"{text_metrics['vocabulary_richness']:.1%}")
                else:
                    st.caption("_Text generation not enabled_")
            
            # Performance Metrics
            with metric_col3:
                st.markdown("**⚡ Performance**")
                st.metric("Retrieval", calc.format_time(retrieval_time))
                if text_gen_time > 0:
                    st.metric("Text Gen", calc.format_time(text_gen_time))
                if image_gen_time > 0:
                    st.metric("Image Gen", calc.format_time(image_gen_time))
                st.metric("**Total**", calc.format_time(total_time))
```

## Step 4: Update Text Generation Section

Dalam bagian text generation, tambahkan timing:

```python
        # Initialize timing variables
        text_gen_time = 0.0
        image_gen_time = 0.0
        text_metrics = {}
        
        # Generate text description
        if generate_text and text_gen:
            st.markdown('<div class="section-header">📄 Generated Description</div>', unsafe_allow_html=True)
            
            text_gen_start = time.time()
            with st.spinner("Generating description..."):
                # ... existing code ...
                description = text_gen.generate_from_context(context)
            
            text_gen_time = time.time() - text_gen_start
            
            # Calculate text metrics
            text_metrics = calc.calculate_text_metrics(description)
            
            st.markdown(f'<div class="result-card">{description}</div>', unsafe_allow_html=True)
```

## Alternative: Use Complete File

Jika manual update terlalu ribet, saya sudah siapkan:
1. `src/utils/metrics_calculator.py` ✅ (sudah dibuat)
2. `METRICS_GUIDE.md` ✅ (sudah dibuat)

Untuk app.py, Anda bisa:
- Copy dari backup multimodal yang sudah jalan
- Tambahkan import dan metrics display sesuai instruksi di atas

Atau saya bisa buatkan file app_with_metrics.py yang lengkap untuk Anda copy manual.
