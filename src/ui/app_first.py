"""
Streamlit Web UI for Multimodal RAG System
"""

import streamlit as st
from PIL import Image
import sys
from pathlib import Path
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.retrieval.retriever import Retriever
from src.models.context_builder import ContextBuilder
from src.models.text_generator import TextGenerator
from src.models.image_generator import ImageGenerator


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
    st.markdown("**Retrieve images, generate descriptions, and create new images using AI**")
    
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
    
    # Query type selection
    query_type = st.radio("Query type:", ["Text", "Image"], horizontal=True)
    
    query_text = None
    query_image = None
    
    if query_type == "Text":
        query_text = st.text_input(
            "Enter your text query:",
            placeholder="e.g., a dog playing in the park"
        )
    else:
        uploaded_file = st.file_uploader("Upload an image:", type=['jpg', 'jpeg', 'png'])
        if uploaded_file:
            query_image = Image.open(uploaded_file)
            st.image(query_image, caption="Query Image", width=300)
    
    # Search button
    if st.button("🔍 Search & Generate", type="primary"):
        if query_type == "Text" and not query_text:
            st.warning("Please enter a text query")
            return
        if query_type == "Image" and query_image is None:
            st.warning("Please upload an image")
            return
        
        # Perform retrieval
        with st.spinner("Searching for similar images..."):
            if query_type == "Text":
                results = retriever.search_by_text(query_text, k=top_k)
            else:
                # Save uploaded image temporarily
                temp_path = "temp_query.jpg"
                query_image.save(temp_path)
                results = retriever.search_by_image(temp_path, k=top_k)
                os.remove(temp_path)
        
        # Display retrieval results
        st.markdown('<div class="section-header">🖼️ Retrieved Images</div>', unsafe_allow_html=True)
        
        cols = st.columns(min(3, top_k))
        for idx, result in enumerate(results['results']):
            with cols[idx % 3]:
                try:
                    img = Image.open(result['image_path'])
                    st.image(img, use_container_width=True)
                    st.markdown(f"**Rank {result['rank']}** | "
                              f"<span class='score-badge'>Score: {result['similarity_score']:.3f}</span>",
                              unsafe_allow_html=True)
                    with st.expander("View captions"):
                        for cap in result['captions']:
                            st.write(f"• {cap}")
                except Exception as e:
                    st.error(f"Error loading image: {e}")
        
        # Extract captions for RAG
        all_captions = retriever.get_captions_from_results(results)
        
        # Generate text description
        if generate_text and text_gen:
            st.markdown('<div class="section-header">📄 Generated Description</div>', unsafe_allow_html=True)
            
            with st.spinner("Generating description..."):
                query_str = query_text if query_type == "Text" else "the uploaded image"
                context = context_builder.build_context(query_str, all_captions)
                description = text_gen.generate_from_context(context)
            
            st.markdown(f'<div class="result-card">{description}</div>', unsafe_allow_html=True)
        
        # Generate new image
        if generate_image and image_gen:
            st.markdown('<div class="section-header">🎨 Generated Image</div>', unsafe_allow_html=True)
            
            with st.spinner("Generating image... (this may take a while)"):
                query_str = query_text if query_type == "Text" else ""
                img_prompt = context_builder.build_image_generation_prompt(query_str, all_captions)
                
                st.info(f"**Prompt:** {img_prompt}")
                
                generated_img = image_gen.txt2img(img_prompt)
                
                if generated_img:
                    st.image(generated_img, caption="Generated Image", width=512)
                else:
                    st.error("Failed to generate image. Check your configuration.")
    
    # Footer
    st.markdown("---")
    st.markdown("**Multimodal RAG System** | COCO + CLIP + FAISS + LLM + Stable Diffusion")


if __name__ == "__main__":
    main()