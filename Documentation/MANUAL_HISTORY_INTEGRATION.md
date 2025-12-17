# Manual Integration Guide: Adding History to Your App

## Problem

Script `create_app_with_history.py` tidak berhasil karena struktur file `app_with_metrics.py` berbeda dari yang diexpect.

## Solution

Tambahkan history secara manual dengan langkah-langkah berikut:

---

## Step 1: Add Import

Di bagian imports (sekitar line 20), tambahkan:

```python
from src.utils.history_manager import HistoryManager
```

---

## Step 2: Initialize History Manager

Di dalam fungsi `main()`, setelah initialize components, tambahkan:

```python
# Initialize history manager
history_manager = HistoryManager()
```

---

## Step 3: Add History Tab in Sidebar

Ganti sidebar configuration dengan tabs. Cari bagian sidebar dan ganti dengan:

```python
# Sidebar with tabs
with st.sidebar:
    st.markdown("### 🔍 Multimodal RAG")
    
    tab1, tab2 = st.tabs(["⚙️ Config", "📜 History"])
    
    with tab1:
        st.markdown("#### Configuration")
        top_k = st.slider("Results to Retrieve", 1, 10, 5)
        generate_text = st.toggle("Generate Description", value=True)
        generate_image = st.toggle("Generate New Image", value=False)
        
        if generate_image and image_gen is None:
            st.warning("Image generation not available")
            generate_image = False
        
        st.markdown("---")
        auto_save = st.checkbox("Auto-save to history", value=True, 
                               help="Automatically save queries to history")
    
    with tab2:
        st.markdown("#### Query History")
        
        # Get recent queries
        queries = history_manager.get_all_queries(limit=20)
        
        if queries:
            st.caption(f"Showing {len(queries)} recent queries")
            
            for query in queries:
                timestamp = query['timestamp'].split('.')[0] if '.' in query['timestamp'] else query['timestamp']
                mode_emoji = "📝" if query['query_mode'] == "Text Only" else "🖼️" if query['query_mode'] == "Image Only" else "🔀"
                
                with st.expander(f"{mode_emoji} {timestamp}"):
                    st.write(f"**Mode:** {query['query_mode']}")
                    if query['query_text']:
                        st.write(f"**Query:** {query['query_text'][:50]}...")
                    st.write(f"**Results:** {query['top_k']}")
                    st.write(f"**Similarity:** {query['avg_similarity']:.3f}")
                    st.write(f"**Time:** {query['total_time']:.2f}s")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Load", key=f"load_{query['id']}", use_container_width=True):
                            st.session_state['load_query_id'] = query['id']
                            st.rerun()
                    with col2:
                        if st.button("🗑️ Delete", key=f"del_{query['id']}", use_container_width=True):
                            if history_manager.delete_query(query['id']):
                                st.success("Deleted!")
                                st.rerun()
            
            # Statistics
            st.markdown("---")
            stats = history_manager.get_statistics()
            st.markdown("#### 📊 Statistics")
            st.write(f"Total queries: {stats['total_queries']}")
            st.write(f"Avg similarity: {stats['avg_similarity']:.3f}")
            st.write(f"Avg time: {stats['avg_time']:.2f}s")
        else:
            st.info("No history yet. Start searching to build your history!")
```

---

## Step 4: Add Save Logic

Setelah metrics display (sebelum footer), tambahkan:

```python
# Save to History
st.markdown("---")

if auto_save:
    try:
        query_id = history_manager.save_query(
            query_data={
                'query_mode': query_mode,
                'query_text': query_text,
                'query_image': query_image,
                'text_weight': text_weight if query_mode == "Text + Image (Multimodal)" else None,
                'top_k': top_k
            },
            results=results,
            retrieval_metrics=retrieval_metrics,
            performance={
                'retrieval_time': retrieval_time,
                'text_gen_time': text_gen_time,
                'image_gen_time': image_gen_time,
                'total_time': total_time
            },
            generated_text=description if generate_text and text_gen else None,
            text_metrics=text_metrics if text_metrics else None,
            generated_image=generated_img if generate_image and image_gen and 'generated_img' in locals() else None
        )
        st.success(f"✅ Auto-saved as Query #{query_id}")
    except Exception as e:
        st.error(f"Auto-save failed: {e}")
else:
    if st.button("💾 Save to History", use_container_width=True):
        try:
            query_id = history_manager.save_query(
                query_data={
                    'query_mode': query_mode,
                    'query_text': query_text,
                    'query_image': query_image,
                    'text_weight': text_weight if query_mode == "Text + Image (Multimodal)" else None,
                    'top_k': top_k
                },
                results=results,
                retrieval_metrics=retrieval_metrics,
                performance={
                    'retrieval_time': retrieval_time,
                    'text_gen_time': text_gen_time,
                    'image_gen_time': image_gen_time,
                    'total_time': total_time
                },
                generated_text=description if generate_text and text_gen else None,
                text_metrics=text_metrics if text_metrics else None,
                generated_image=generated_img if generate_image and image_gen and 'generated_img' in locals() else None
            )
            st.success(f"✅ Saved as Query #{query_id}")
        except Exception as e:
            st.error(f"Error saving: {e}")
```

---

## Step 5: Add Load Query Handler (Optional)

Di awal fungsi `main()`, setelah header, tambahkan:

```python
# Check if loading from history
if 'load_query_id' in st.session_state:
    query_id = st.session_state['load_query_id']
    del st.session_state['load_query_id']
    
    # Load query from history
    loaded_query = history_manager.get_query_by_id(query_id)
    
    if loaded_query:
        st.info(f"📂 Loaded query from {loaded_query['timestamp']}")
        
        # Display loaded results
        st.markdown("### 🔎 Query Information")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Query Mode", loaded_query['query_mode'])
        with col2:
            st.metric("Avg Similarity", f"{loaded_query['avg_similarity']:.3f}")
        with col3:
            st.metric("Total Time", f"{loaded_query['total_time']:.2f}s")
        
        # Display retrieval results
        st.markdown("### 🖼️ Retrieved Images")
        
        results_list = loaded_query['retrieval_results']
        cols = st.columns(min(3, len(results_list)))
        
        for idx, result in enumerate(results_list):
            with cols[idx % 3]:
                try:
                    img = Image.open(result['image_path'])
                    st.image(img, use_container_width=True)
                    st.markdown(f"**Rank {result['rank']}** | Score: {result['similarity_score']:.3f}")
                    with st.expander("View captions"):
                        for cap in result['captions']:
                            st.write(f"• {cap}")
                except Exception as e:
                    st.error(f"Error loading image: {e}")
        
        # Display generated text if available
        if loaded_query['generated_text']:
            st.markdown("### 📄 Generated Description")
            st.markdown(loaded_query['generated_text'])
        
        # Display generated image if available
        if loaded_query['generated_image_path']:
            st.markdown("### 🎨 Generated Image")
            try:
                gen_img = Image.open(loaded_query['generated_image_path'])
                st.image(gen_img, caption="Generated Image", width=512)
            except Exception as e:
                st.error(f"Error loading generated image: {e}")
        
        st.markdown("---")
        st.info("👆 Use the search form above to create a new query")
        return
```

---

## Quick Test

Setelah menambahkan kode di atas:

1. Run app: `streamlit run src\ui\app_with_metrics.py`
2. Lakukan search
3. Check History tab di sidebar
4. Klik Load untuk test

---

## Alternative: Use Pre-made File

Jika manual integration terlalu ribet, saya bisa buatkan file lengkap yang sudah terintegrasi. Tapi perlu tahu struktur exact dari app Anda saat ini.

Mau saya buatkan file lengkap atau prefer manual integration?
