"""
Safe script to add metrics to app.py
This script will add metrics functionality line by line safely
"""

def add_metrics_safely():
    print("=" * 70)
    print("ADDING METRICS TO APP.PY SAFELY")
    print("=" * 70)
    
    # Read current file
    with open('src/ui/app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"\n[OK] Read {len(lines)} lines from app.py")
    
    # Find line numbers for insertions
    import_os_line = None
    import_image_gen_line = None
    validation_end_line = None
    retrieval_end_line = None
    text_gen_start_line = None
    text_gen_end_line = None
    image_gen_start_line = None
    footer_line = None
    
    for i, line in enumerate(lines):
        if 'import os' in line and import_os_line is None:
            import_os_line = i
        if 'from src.models.image_generator import ImageGenerator' in line:
            import_image_gen_line = i
        if 'st.warning("Please provide both text and image for multimodal search")' in line:
            # Next line after return
            validation_end_line = i + 2
        if 'os.remove(temp_path)' in line and retrieval_end_line is None:
            # Find the last os.remove in retrieval section
            if i < len(lines) - 50:  # Not near end of file
                retrieval_end_line = i + 1
        if '# Generate text description' in line and text_gen_start_line is None:
            text_gen_start_line = i
        if 'st.markdown(f\'<div class="result-card">{description}</div>\', unsafe_allow_html=True)' in line:
            text_gen_end_line = i
        if '# Generate new image' in line and image_gen_start_line is None:
            image_gen_start_line = i
        if '# Footer' in line and footer_line is None:
            footer_line = i
    
    print(f"\n[INFO] Found insertion points:")
    print(f"   Import os line: {import_os_line}")
    print(f"   Import ImageGenerator line: {import_image_gen_line}")
    print(f"   Validation end: {validation_end_line}")
    print(f"   Retrieval end: {retrieval_end_line}")
    print(f"   Text gen start: {text_gen_start_line}")
    print(f"   Text gen end: {text_gen_end_line}")
    print(f"   Image gen start: {image_gen_start_line}")
    print(f"   Footer: {footer_line}")
    
    if None in [import_os_line, import_image_gen_line, validation_end_line, retrieval_end_line, text_gen_start_line, footer_line]:
        print("\n[ERROR] Could not find all insertion points!")
        print("Please make sure app.py is the multimodal version")
        return False
    
    # Create new lines list
    new_lines = lines.copy()
    
    # 1. Add imports (insert after import os)
    new_lines.insert(import_os_line + 1, 'import time\n')
    print("\n[OK] Step 1: Added 'import time'")
    
    # Adjust line numbers after first insertion
    import_image_gen_line += 1
    validation_end_line += 1
    retrieval_end_line += 1
    text_gen_start_line += 1
    text_gen_end_line += 1
    image_gen_start_line += 1
    footer_line += 1
    
    # 2. Add MetricsCalculator import (after ImageGenerator import)
    new_lines.insert(import_image_gen_line + 1, 'from src.utils.metrics_calculator import MetricsCalculator\n')
    print("[OK] Step 2: Added MetricsCalculator import")
    
    # Adjust line numbers
    validation_end_line += 1
    retrieval_end_line += 1
    text_gen_start_line += 1
    text_gen_end_line += 1
    image_gen_start_line += 1
    footer_line += 1
    
    # 3. Add metrics initialization (after validation)
    metrics_init = '''        
        # Initialize metrics calculator
        calc = MetricsCalculator()
        
        # Start total timer
        total_start = time.time()
        
        # Perform retrieval with timing
        retrieval_start = time.time()
'''
    new_lines.insert(validation_end_line, metrics_init)
    print("[OK] Step 3: Added metrics initialization")
    
    # Adjust line numbers
    lines_added = metrics_init.count('\n')
    retrieval_end_line += lines_added
    text_gen_start_line += lines_added
    text_gen_end_line += lines_added
    image_gen_start_line += lines_added
    footer_line += lines_added
    
    # 4. Add retrieval metrics (after retrieval)
    retrieval_metrics = '''        
        retrieval_time = time.time() - retrieval_start
        
        # Calculate retrieval metrics
        retrieval_metrics = calc.calculate_retrieval_metrics(results)
'''
    new_lines.insert(retrieval_end_line, retrieval_metrics)
    print("[OK] Step 4: Added retrieval metrics calculation")
    
    # Adjust line numbers
    lines_added = retrieval_metrics.count('\n')
    text_gen_start_line += lines_added
    text_gen_end_line += lines_added
    image_gen_start_line += lines_added
    footer_line += lines_added
    
    # 5. Add text gen timing variables (before text gen)
    text_init = '''        # Initialize timing variables
        text_gen_time = 0.0
        image_gen_time = 0.0
        text_metrics = {}
        
'''
    new_lines.insert(text_gen_start_line, text_init)
    print("[OK] Step 5: Added text generation timing variables")
    
    # Adjust line numbers
    lines_added = text_init.count('\n')
    text_gen_end_line += lines_added
    image_gen_start_line += lines_added
    footer_line += lines_added
    
    # Find the line with "with st.spinner" for text generation
    for i in range(text_gen_start_line, text_gen_start_line + 20):
        if 'with st.spinner("Generating description...")' in new_lines[i]:
            new_lines[i] = new_lines[i].replace(
                'with st.spinner("Generating description..."):',
                'text_gen_start = time.time()\n            with st.spinner("Generating description..."):'
            )
            print("[OK] Step 6: Added text generation timer start")
            text_gen_end_line += 1
            image_gen_start_line += 1
            footer_line += 1
            break
    
    # 6. Add text metrics calculation (after description generation)
    text_metrics_calc = '''            
            text_gen_time = time.time() - text_gen_start
            
            # Calculate text metrics
            text_metrics = calc.calculate_text_metrics(description)
'''
    new_lines.insert(text_gen_end_line, text_metrics_calc)
    print("[OK] Step 7: Added text metrics calculation")
    
    # Adjust line numbers
    lines_added = text_metrics_calc.count('\n')
    image_gen_start_line += lines_added
    footer_line += lines_added
    
    # 7. Add image gen timing
    for i in range(image_gen_start_line, image_gen_start_line + 20):
        if 'with st.spinner("Generating image... (this may take a while)")' in new_lines[i]:
            new_lines[i] = new_lines[i].replace(
                'with st.spinner("Generating image... (this may take a while)"):',
                'image_gen_start = time.time()\n            with st.spinner("Generating image... (this may take a while)"):'
            )
            print("[OK] Step 8: Added image generation timer start")
            footer_line += 1
            
            # Find the end of image generation block and add timing
            for j in range(i, i + 30):
                if 'st.error("Failed to generate image. Check your configuration.")' in new_lines[j]:
                    new_lines.insert(j + 1, '            \n            image_gen_time = time.time() - image_gen_start\n')
                    print("[OK] Step 9: Added image generation timer end")
                    footer_line += 2
                    break
            break
    
    # 8. Add metrics display section (before footer)
    metrics_display = '''        
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
    
'''
    new_lines.insert(footer_line, metrics_display)
    print("[OK] Step 10: Added metrics display section")
    
    # Write the new file
    with open('src/ui/app.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("\n" + "=" * 70)
    print("[OK] SUCCESS! Metrics added to app.py")
    print("=" * 70)
    print("\nYou can now run: streamlit run src\\ui\\app.py")
    print("\nThe metrics will appear in an expandable section after results.")
    return True

if __name__ == "__main__":
    try:
        success = add_metrics_safely()
        if not success:
            print("\n[WARN] Please check the error messages above")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nIf you see this error, please:")
        print("1. Make sure you're in the project root directory")
        print("2. Make sure src/ui/app.py is the working multimodal version")
        print("3. Make sure you have a backup of app.py")
