"""
Script to add metrics to app.py
Run this to automatically add metrics functionality
"""

import re

def add_metrics_to_app():
    """Add metrics and timing to app.py"""
    
    # Read the file
    with open('src/ui/app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Step 1: Add imports
    if 'import time' not in content:
        content = content.replace(
            'import os',
            'import os\nimport time'
        )
        print("✅ Added 'import time'")
    
    if 'from src.utils.metrics_calculator import MetricsCalculator' not in content:
        content = content.replace(
            'from src.models.image_generator import ImageGenerator',
            'from src.models.image_generator import ImageGenerator\nfrom src.utils.metrics_calculator import MetricsCalculator'
        )
        print("✅ Added MetricsCalculator import")
    
    # Step 2: Add timing and metrics calculation after validation
    search_pattern = r'(if query_mode == "Text \+ Image \(Multimodal\)":\s+if not query_text or query_image is None:\s+st\.warning\("Please provide both text and image for multimodal search"\)\s+return)\s+(# Perform retrieval)'
    
    replacement = r'''\1
        
        # Initialize metrics calculator
        calc = MetricsCalculator()
        
        # Start total timer
        total_start = time.time()
        
        # Perform retrieval with timing
        retrieval_start = time.time()
        # \2'''
    
    content = re.sub(search_pattern, replacement, content, flags=re.MULTILINE)
    print("✅ Added timing initialization")
    
    # Step 3: Add retrieval time calculation after retrieval
    content = content.replace(
        '                os.remove(temp_path)\n        \n        # Display query info',
        '''                os.remove(temp_path)
        
        retrieval_time = time.time() - retrieval_start
        
        # Calculate retrieval metrics
        retrieval_metrics = calc.calculate_retrieval_metrics(results)
        
        # Display query info'''
    )
    print("✅ Added retrieval metrics calculation")
    
    # Step 4: Add text generation timing
    old_text_gen = '''        # Generate text description
        if generate_text and text_gen:
            st.markdown('<div class="section-header">📄 Generated Description</div>', unsafe_allow_html=True)
            
            with st.spinner("Generating description..."):'''
    
    new_text_gen = '''        # Initialize timing variables
        text_gen_time = 0.0
        image_gen_time = 0.0
        text_metrics = {}
        
        # Generate text description
        if generate_text and text_gen:
            st.markdown('<div class="section-header">📄 Generated Description</div>', unsafe_allow_html=True)
            
            text_gen_start = time.time()
            with st.spinner("Generating description..."):'''
    
    content = content.replace(old_text_gen, new_text_gen)
    print("✅ Added text generation timing")
    
    # Step 5: Add text metrics calculation
    content = content.replace(
        '                description = text_gen.generate_from_context(context)\n            \n            st.markdown(f\'<div class="result-card">{description}</div>\', unsafe_allow_html=True)',
        '''                description = text_gen.generate_from_context(context)
            
            text_gen_time = time.time() - text_gen_start
            
            # Calculate text metrics
            text_metrics = calc.calculate_text_metrics(description)
            
            st.markdown(f'<div class="result-card">{description}</div>', unsafe_allow_html=True)'''
    )
    print("✅ Added text metrics calculation")
    
    # Step 6: Add image generation timing
    content = content.replace(
        '        # Generate new image\n        if generate_image and image_gen:\n            st.markdown(\'<div class="section-header">🎨 Generated Image</div>\', unsafe_allow_html=True)\n            \n            with st.spinner("Generating image... (this may take a while)"):',
        '''        # Generate new image
        if generate_image and image_gen:
            st.markdown('<div class="section-header">🎨 Generated Image</div>', unsafe_allow_html=True)
            
            image_gen_start = time.time()
            with st.spinner("Generating image... (this may take a while)"):'''
    )
    print("✅ Added image generation timing start")
    
    content = content.replace(
        '                    st.error("Failed to generate image. Check your configuration.")\n    \n    # Footer',
        '''                    st.error("Failed to generate image. Check your configuration.")
            
            image_gen_time = time.time() - image_gen_start
        
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
                st.metric("Std Deviation", f"{retrieval_metrics['std_similarity']:.3f}")
            
            # Generation Metrics
            with metric_col2:
                st.markdown("**📝 Generation Quality**")
                if text_metrics:
                    st.metric("Word Count", text_metrics['word_count'])
                    st.metric("Sentence Count", text_metrics['sentence_count'])
                    st.metric("Vocabulary Richness", f"{text_metrics['vocabulary_richness']:.1%}")
                    st.metric("Avg Word Length", f"{text_metrics['avg_word_length']:.1f} chars")
                else:
                    st.caption("_Text generation not enabled_")
            
            # Performance Metrics
            with metric_col3:
                st.markdown("**⚡ Performance**")
                st.metric("Retrieval Time", calc.format_time(retrieval_time))
                if text_gen_time > 0:
                    st.metric("Text Gen Time", calc.format_time(text_gen_time))
                if image_gen_time > 0:
                    st.metric("Image Gen Time", calc.format_time(image_gen_time))
                st.metric("**Total Time**", calc.format_time(total_time))
            
            # Metrics interpretation
            st.markdown("---")
            st.markdown("**📖 Metrics Interpretation:**")
            
            interp_col1, interp_col2 = st.columns(2)
            
            with interp_col1:
                st.markdown("**Retrieval:**")
                avg_sim_quality = calc.get_metric_interpretation('avg_similarity', retrieval_metrics['avg_similarity'])
                div_quality = calc.get_metric_interpretation('diversity', retrieval_metrics['diversity'])
                
                if avg_sim_quality:
                    st.caption(f"• Similarity: {avg_sim_quality} ({retrieval_metrics['avg_similarity']:.3f})")
                if div_quality:
                    st.caption(f"• Diversity: {div_quality} ({retrieval_metrics['diversity']:.1%})")
            
            with interp_col2:
                if text_metrics:
                    st.markdown("**Generation:**")
                    vocab_quality = calc.get_metric_interpretation('vocabulary_richness', text_metrics['vocabulary_richness'])
                    
                    if vocab_quality:
                        st.caption(f"• Vocabulary: {vocab_quality} ({text_metrics['vocabulary_richness']:.1%})")
                    
                    # Word count interpretation
                    if 40 <= text_metrics['word_count'] <= 100:
                        st.caption(f"• Length: Good ({text_metrics['word_count']} words)")
                    elif text_metrics['word_count'] < 40:
                        st.caption(f"• Length: Short ({text_metrics['word_count']} words)")
                    else:
                        st.caption(f"• Length: Long ({text_metrics['word_count']} words)")
    
    # Footer'''
    )
    print("✅ Added metrics display section")
    
    # Write back
    with open('src/ui/app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ Successfully added metrics to app.py!")
    print("\nYou can now run: streamlit run src\\ui\\app.py")

if __name__ == "__main__":
    try:
        add_metrics_to_app()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check that:")
        print("1. You're in the project root directory")
        print("2. src/ui/app.py exists and is the multimodal version")
        print("3. You have write permissions")
