"""
Script to add history feature to app_with_metrics.py
Creates app_with_history.py with integrated history functionality
"""

def add_history_to_app():
    print("Adding history feature to app...")
    
    with open('src/ui/app_with_metrics.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add history manager import
    content = content.replace(
        'from src.utils.metrics_calculator import MetricsCalculator',
        'from src.utils.metrics_calculator import MetricsCalculator\nfrom src.utils.history_manager import HistoryManager'
    )
    
    # 2. Initialize history manager after other components
    content = content.replace(
        '    context_builder = ContextBuilder()\n    text_gen = load_text_generator()\n    image_gen = load_image_generator()',
        '''    context_builder = ContextBuilder()
    text_gen = load_text_generator()
    image_gen = load_image_generator()
    
    # Initialize history manager
    history_manager = HistoryManager()'''
    )
    
    # 3. Add history tab in sidebar (replace sidebar section)
    old_sidebar = '''    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    top_k = st.sidebar.slider("Number of results (k)", 1, 10, 5)
    generate_text = st.sidebar.checkbox("Generate text description", value=True)
    generate_image = st.sidebar.checkbox("Generate new image", value=False)
    
    if generate_image and image_gen is None:
        st.sidebar.warning("Image generation not available")
        generate_image = False'''
    
    new_sidebar = '''    # Sidebar with tabs
    st.sidebar.header("🔍 Multimodal RAG")
    
    tab1, tab2 = st.sidebar.tabs(["⚙️ Config", "📜 History"])
    
    with tab1:
        st.markdown("### Configuration")
        top_k = st.slider("Number of results (k)", 1, 10, 5)
        generate_text = st.checkbox("Generate text description", value=True)
        generate_image = st.checkbox("Generate new image", value=False)
        
        if generate_image and image_gen is None:
            st.warning("Image generation not available")
            generate_image = False
        
        st.markdown("---")
        auto_save = st.checkbox("Auto-save to history", value=True, help="Automatically save queries to history")
    
    with tab2:
        st.markdown("### Query History")
        
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
            st.markdown("### 📊 Statistics")
            st.write(f"Total queries: {stats['total_queries']}")
            st.write(f"Avg similarity: {stats['avg_similarity']:.3f}")
            st.write(f"Avg time: {stats['avg_time']:.2f}s")
        else:
            st.info("No history yet. Start searching to build your history!")'''
    
    content = content.replace(old_sidebar, new_sidebar)
    
    # 4. Add save to history button after metrics display (before footer)
    old_footer = '''    
    # Footer
    st.markdown("---")'''
    
    new_save_section = '''        
        # Save to History
        st.markdown("---")
        save_col1, save_col2 = st.columns([3, 1])
        
        with save_col1:
            if auto_save:
                st.caption("✅ Auto-saved to history")
            else:
                st.caption("💡 Enable auto-save in sidebar or click button →")
        
        with save_col2:
            if not auto_save:
                if st.button("💾 Save to History", use_container_width=True):
                    try:
                        query_id = history_manager.save_query(
                            query_data={
                                'query_mode': query_mode,
                                'query_text': query_text,
                                'query_image': query_image,
                                'text_weight': text_weight,
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
                            generated_image=generated_img if generate_image and image_gen and generated_img else None
                        )
                        st.success(f"✅ Saved as Query #{query_id}")
                    except Exception as e:
                        st.error(f"Error saving: {e}")
        
        # Auto-save logic
        if auto_save:
            try:
                query_id = history_manager.save_query(
                    query_data={
                        'query_mode': query_mode,
                        'query_text': query_text,
                        'query_image': query_image,
                        'text_weight': text_weight,
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
                    generated_image=generated_img if generate_image and image_gen and generated_img else None
                )
            except Exception as e:
                st.error(f"Auto-save failed: {e}")
    
    # Footer
    st.markdown("---")'''
    
    content = content.replace(old_footer, new_save_section)
    
    # 5. Add load query functionality at the beginning of main()
    load_query_check = '''    # Check if loading from history
    if 'load_query_id' in st.session_state:
        query_id = st.session_state['load_query_id']
        del st.session_state['load_query_id']
        
        # Load query from history
        loaded_query = history_manager.get_query_by_id(query_id)
        
        if loaded_query:
            st.info(f"📂 Loaded query from {loaded_query['timestamp']}")
            
            # Display loaded results
            st.markdown('<div class="section-header">🔎 Query Information</div>', unsafe_allow_html=True)
            
            info_col1, info_col2, info_col3 = st.columns(3)
            with info_col1:
                st.metric("Query Mode", loaded_query['query_mode'])
            with info_col2:
                st.metric("Avg Similarity", f"{loaded_query['avg_similarity']:.3f}")
            with info_col3:
                st.metric("Total Time", f"{loaded_query['total_time']:.2f}s")
            
            # Display retrieval results
            st.markdown('<div class="section-header">🖼️ Retrieved Images</div>', unsafe_allow_html=True)
            
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
                st.markdown('<div class="section-header">📄 Generated Description</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-card">{loaded_query["generated_text"]}</div>', unsafe_allow_html=True)
            
            # Display generated image if available
            if loaded_query['generated_image_path']:
                st.markdown('<div class="section-header">🎨 Generated Image</div>', unsafe_allow_html=True)
                try:
                    gen_img = Image.open(loaded_query['generated_image_path'])
                    st.image(gen_img, caption="Generated Image", width=512)
                except Exception as e:
                    st.error(f"Error loading generated image: {e}")
            
            st.markdown("---")
            st.info("👆 Use the search form above to create a new query")
            return
    
'''
    
    # Insert after header
    content = content.replace(
        '    # Initialize components\n    retriever = load_retriever()',
        load_query_check + '    # Initialize components\n    retriever = load_retriever()'
    )
    
    # Write to new file
    with open('src/ui/app_with_history.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[OK] Successfully created app_with_history.py!")
    print("\nFeatures added:")
    print("  - History tab in sidebar")
    print("  - Auto-save option")
    print("  - Load previous queries")
    print("  - Delete history entries")
    print("  - Statistics display")
    print("\nTo use:")
    print("  streamlit run src\\ui\\app_with_history.py")

if __name__ == "__main__":
    try:
        add_history_to_app()
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
