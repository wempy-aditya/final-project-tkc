"""
Streamlit Web UI for Multimodal RAG System
Supports text-only, image-only, and multimodal (text+image) queries
"""

import streamlit as st
from PIL import Image
import sys
from pathlib import Path
import os
import time

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.retrieval.retriever import Retriever
from src.models.context_builder import ContextBuilder
from src.models.text_generator import TextGenerator
from src.models.image_generator import ImageGenerator
from src.utils.metrics_calculator import MetricsCalculator


# Page configuration
st.set_page_config(
    page_title="Multimodal RAG System",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .result-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .score-badge {
        background-color: #1f77b4;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    .multimodal-badge {
        background-color: #2ca02c;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_retriever():
    """Load retriever (cached)"""
    try:
        return Retriever()
    except Exception as e:
        st.error(f"Error loading retriever: {e}")
        return None


@st.cache_resource
def load_text_generator():
    """Load text generator (cached)"""
    try:
        return TextGenerator()
    except Exception as e:
        st.warning(f"Text generator not available: {e}")
        return None


@st.cache_resource
def load_image_generator():
    """Load image generator (cached)"""
    try:
        return ImageGenerator(use_local=False)
    except Exception as e:
        st.warning(f"Image generator not available: {e}")
        return None


def main():
    # Header
    st.markdown('<div class="main-header">🔍 Multimodal RAG System</div>', unsafe_allow_html=True)
    st.markdown("**Retrieve images using text, image, or both simultaneously!**")
    
    # Initialize components
    retriever = load_retriever()
    if retriever is None:
        st.error("⚠️ Retriever not initialized. Please run setup first.")
        st.code("python scripts/setup.py")
        return
    
    context_builder = ContextBuilder()
    text_gen = load_text_generator()
    image_gen = load_image_generator()
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    top_k = st.sidebar.slider("Number of results (k)", 1, 10, 5)
    generate_text = st.sidebar.checkbox("Generate text description", value=True)
    generate_image = st.sidebar.checkbox("Generate new image", value=False)
    
    if generate_image and image_gen is None:
        st.sidebar.warning("Image generation not available")
        generate_image = False
    
    # Main content
    st.markdown('<div class="section-header">📝 Input Query</div>', unsafe_allow_html=True)
    
    # Query mode selection
    query_mode = st.radio(
        "Query mode:",
        ["Text Only", "Image Only", "Text + Image (Multimodal)"],
        horizontal=True,
        help="Choose how you want to search: text only, image only, or combine both for better results!"
    )
    
    # Input fields in columns
    col1, col2 = st.columns(2)
    
    query_text = None
    query_image = None
    uploaded_file = None
    
    with col1:
        st.markdown("**Text Query:**")
        query_text = st.text_input(
            "Enter your text query:",
            placeholder="e.g., a dog playing in the park",
            disabled=(query_mode == "Image Only"),
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("**Image Query:**")
        uploaded_file = st.file_uploader(
            "Upload an image:",
            type=['jpg', 'jpeg', 'png'],
            disabled=(query_mode == "Text Only"),
            label_visibility="collapsed"
        )
        if uploaded_file:
            query_image = Image.open(uploaded_file)
            st.image(query_image, caption="Query Image", width=250)
    
    # Multimodal weight slider (only for multimodal mode)
    text_weight = 0.5
    if query_mode == "Text + Image (Multimodal)":
        st.markdown("**Fusion Weight:**")
        text_weight = st.slider(
            "Text vs Image balance:",
            0.0, 1.0, 0.5, 0.1,
            help="0.0 = image only, 1.0 = text only, 0.5 = balanced",
            format="%.1f"
        )
        
        # Show weight interpretation
        if text_weight < 0.3:
            weight_desc = "🖼️ Image-focused"
        elif text_weight > 0.7:
            weight_desc = "📝 Text-focused"
        else:
            weight_desc = "⚖️ Balanced"
        
        st.caption(f"Current: {weight_desc} (Text: {text_weight:.1f}, Image: {1-text_weight:.1f})")
    
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
        # Perform retrieval
        with st.spinner("Searching for similar images..."):
            if query_mode == "Text Only":
                results = retriever.search_by_text(query_text, k=top_k)
            elif query_mode == "Image Only":
                # Save uploaded image temporarily
                temp_path = "temp_query.jpg"
                query_image.save(temp_path)
                results = retriever.search_by_image(temp_path, k=top_k)
                os.remove(temp_path)
            else:  # Multimodal
                # Save uploaded image temporarily
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
        
        # Display query info
        st.markdown('<div class="section-header">🔎 Query Information</div>', unsafe_allow_html=True)
        
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.metric("Query Mode", query_mode)
        with info_col2:
            if query_mode == "Text + Image (Multimodal)":
                st.metric("Text Weight", f"{text_weight:.1f}")
            else:
                st.metric("Results", f"{len(results['results'])}")
        with info_col3:
            if query_mode == "Text + Image (Multimodal)":
                st.metric("Image Weight", f"{1-text_weight:.1f}")
            else:
                st.metric("Top-K", top_k)
        
        # Display retrieval results
        st.markdown('<div class="section-header">🖼️ Retrieved Images</div>', unsafe_allow_html=True)
        
        cols = st.columns(min(3, top_k))
        for idx, result in enumerate(results['results']):
            with cols[idx % 3]:
                try:
                    img = Image.open(result['image_path'])
                    st.image(img, use_container_width=True)
                    
                    # Show rank and score
                    badge_html = f"**Rank {result['rank']}** | <span class='score-badge'>Score: {result['similarity_score']:.3f}</span>"
                    st.markdown(badge_html, unsafe_allow_html=True)
                    
                    # Show captions
                    with st.expander("View captions"):
                        for cap in result['captions']:
                            st.write(f"• {cap}")
                except Exception as e:
                    st.error(f"Error loading image: {e}")
        
        # Extract captions for RAG
        all_captions = retriever.get_captions_from_results(results)
        
        # Initialize timing variables
        text_gen_time = 0.0
        image_gen_time = 0.0
        text_metrics = {}
        
        # Generate text description
        if generate_text and text_gen:
            st.markdown('<div class="section-header">📄 Generated Description</div>', unsafe_allow_html=True)
            
            text_gen_start = time.time()
            with st.spinner("Generating description..."):
                # Build query string for context
                if query_mode == "Text Only":
                    query_str = query_text
                elif query_mode == "Image Only":
                    query_str = "the uploaded image"
                else:  # Multimodal
                    query_str = f"{query_text} (with reference image)"
                
                context = context_builder.build_context(query_str, all_captions)
                description = text_gen.generate_from_context(context)
            
            text_gen_time = time.time() - text_gen_start
            
            # Calculate text metrics
            text_metrics = calc.calculate_text_metrics(description)
            
            st.markdown(f'<div class="result-card">{description}</div>', unsafe_allow_html=True)
        
        # Generate new image
        if generate_image and image_gen:
            st.markdown('<div class="section-header">🎨 Generated Image</div>', unsafe_allow_html=True)
            
            image_gen_start = time.time()
            with st.spinner("Generating image... (this may take a while)"):
                query_str = query_text if query_mode != "Image Only" else ""
                img_prompt = context_builder.build_image_generation_prompt(query_str, all_captions)
                
                st.info(f"**Prompt:** {img_prompt}")
                
                generated_img = image_gen.txt2img(img_prompt)
                
                if generated_img:
                    st.image(generated_img, caption="Generated Image", width=512)
                else:
                    st.error("Failed to generate image. Check your configuration.")
            
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
    
    # Footer
    st.markdown("---")
    st.markdown("**Multimodal RAG System** | COCO + CLIP + FAISS + LLM + Stable Diffusion")
    st.caption("💡 Tip: Use multimodal mode for best results by combining text description with a reference image!")


if __name__ == "__main__":
    main()
