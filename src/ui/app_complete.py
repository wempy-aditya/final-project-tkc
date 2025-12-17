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
from src.utils.history_manager import HistoryManager


# Page configuration
st.set_page_config(
    page_title="Multimodal RAG",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern & Elegant Theme
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --primary: #4F46E5;
        --secondary: #10B981;
        --background: #F9FAFB;
        --card-bg: #FFFFFF;
        --text-color: #1F2937;
        --accent: #818CF8;
    }

    /* Global Styles */
    .stApp {
        background-color: var(--background);
        font-family: 'Inter', sans-serif;
        color: var(--text-color);
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #111827;
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    /* Custom Header */
    .main-header-container {
        text-align: center;
        padding: 2rem 0 3rem 0;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
    }
    .main-subtitle {
        font-size: 1.1rem;
        color: #4B5563;
        -webkit-text-fill-color: #4B5563;
        margin-top: 0.5rem;
    }

    /* Cards & Containers */
    .css-card {
        background-color: var(--card-bg);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        border: 1px solid #E5E7EB;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .css-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Section Headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Metrics Badge */
    .metric-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        background: #F3F4F6;
        border-radius: 0.75rem;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
    }
    .metric-label {
        font-size: 0.875rem;
        color: #6B7280;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-score {
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    .badge-rank {
        background-color: #ECEFF1;
        color: #37474F;
    }

    /* Custom Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border-radius: 0.5rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #4338CA 0%, #3730A3 100%);
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.4);
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        border-radius: 0.5rem;
        border: 1px solid #D1D5DB;
        padding: 0.5rem 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }
    
    /* Image styles */
    .result-image {
        border-radius: 0.75rem;
        overflow: hidden;
    }
    
    /* Hide Text Decoration regarding links if any */
    a {
        text-decoration: none;
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
    # Header Section
    st.markdown("""
        <div class="main-header-container">
            <h1 class="main-title">✨ Multimodal RAG</h1>
            <p class="main-subtitle">Experience the power of Search & Generation across Text & Images</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize components
    with st.spinner("Initializing System..."):
        retriever = load_retriever()
    
    if retriever is None:
        st.error("⚠️ Retriever not initialized. Please run setup first.")
        st.code("python scripts/setup.py")
        return
    
    context_builder = ContextBuilder()
    text_gen = load_text_generator()
    image_gen = load_image_generator()
    
    # Initialize history manager
    history_manager = HistoryManager()
    
    # Check if loading from history
    if 'load_query_id' in st.session_state:
        query_id = st.session_state['load_query_id']
        del st.session_state['load_query_id']
        
        # Load query from history
        loaded_query = history_manager.get_query_by_id(query_id)
        
        if loaded_query:
            st.info(f"📂 Loaded query from {loaded_query['timestamp']}")
            
            # Display query info
            st.markdown('<div class="section-header">🔎 Query Information</div>', unsafe_allow_html=True)
            
            info_col1, info_col2, info_col3 = st.columns(3)
            with info_col1:
                st.metric("Query Mode", loaded_query['query_mode'])
                if loaded_query['query_text']:
                    st.caption(f"Query: {loaded_query['query_text'][:50]}...")
            with info_col2:
                st.metric("Avg Similarity", f"{loaded_query['avg_similarity']:.3f}")
                st.metric("Diversity", f"{loaded_query['diversity']:.1%}")
            with info_col3:
                st.metric("Total Time", f"{loaded_query['total_time']:.2f}s")
                st.metric("Results", loaded_query['top_k'])
            
            # Display query image if available
            if loaded_query['query_image_path']:
                st.markdown('<div class="section-header">📷 Query Image</div>', unsafe_allow_html=True)
                try:
                    query_img = Image.open(loaded_query['query_image_path'])
                    st.image(query_img, caption="Query Image", width=300)
                except Exception as e:
                    st.error(f"Error loading query image: {e}")
            
            # Display retrieval results
            st.markdown('<div class="section-header">🖼️ Retrieved Images</div>', unsafe_allow_html=True)
            
            results_list = loaded_query['retrieval_results']
            cols = st.columns(min(3, len(results_list)))
            
            for idx, result in enumerate(results_list):
                with cols[idx % 3]:
                    st.markdown('<div class="css-card" style="padding: 1rem;">', unsafe_allow_html=True)
                    try:
                        img = Image.open(result['image_path'])
                        st.image(img, use_container_width=True)
                        
                        st.markdown(f"""
                            <div style="margin-top: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                                <span class="badge badge-rank">Rank #{result['rank']}</span>
                                <span class="badge badge-score">Sim: {result['similarity_score']:.3f}</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("📝 View Captions"):
                            for cap in result['captions']:
                                st.markdown(f"<small>• {cap}</small>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error loading image: {e}")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Display generated text if available
            if loaded_query['generated_text']:
                st.markdown('<div class="section-header">📄 Generated Description</div>', unsafe_allow_html=True)
                st.markdown(f"""
                    <div style="background: #F3F4F6; padding: 1rem; border-radius: 0.5rem; font-style: italic; color: #4B5563;">
                        "{loaded_query['generated_text']}"
                    </div>
                """, unsafe_allow_html=True)
            
            # Display generated image if available
            if loaded_query['generated_image_path']:
                st.markdown('<div class="section-header">🎨 Generated Image</div>', unsafe_allow_html=True)
                try:
                    gen_img = Image.open(loaded_query['generated_image_path'])
                    st.image(gen_img, caption="Generated Image", width=512)
                except Exception as e:
                    st.error(f"Error loading generated image: {e}")
            
            # Display metrics
            st.markdown('<div class="section-header">📊 Metrics</div>', unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            
            with m1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Avg Similarity</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{loaded_query["avg_similarity"]:.3f}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with m2:
                if loaded_query['word_count']:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.markdown('<div class="metric-label">Word Count</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{loaded_query["word_count"]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No text metrics")
            
            with m3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Total Time</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{loaded_query["total_time"]:.2f}s</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.info("👆 Use the search form above to create a new query")
            return
    
    # Sidebar with Tabs
    with st.sidebar:
        st.markdown("### 🔍 Multimodal RAG")
        
        tab1, tab2 = st.tabs(["⚙️ Config", "📜 History"])
        
        with tab1:
            st.info("Configure your search parameters here.")
            
            st.markdown("---")
            top_k = st.slider("Results to Retrieve", 1, 10, 5)
            
            st.markdown("### 🛠️ Features")
            generate_text = st.toggle("Generate Description", value=True)
            generate_image = st.toggle("Generate New Image", value=False)
            
            if generate_image and image_gen is None:
                st.warning("Image generation not available")
                generate_image = False
            
            st.markdown("---")
            auto_save = st.checkbox("Auto-save to history", value=True, 
                                   help="Automatically save queries to history")
            
            st.markdown("---")
            st.caption("v2.0 • Multimodal AI System")
        
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
    
    # Main Content Area
    
    # --- Input Section ---
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">� Start Your Search</div>', unsafe_allow_html=True)
    
    # Query Mode Selection with custom columns for layout
    col_mode, col_space = st.columns([2, 1])
    with col_mode:
        query_mode = st.radio(
            "Select Search Mode:",
            ["Text Only", "Image Only", "Text + Image (Multimodal)"],
            horizontal=True,
            help="Choose your input modality."
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dynamic Input Fields
    col1, col2 = st.columns(2)
    
    query_text = None
    query_image = None
    uploaded_file = None
    
    with col1:
        disabled_text = query_mode == "Image Only"
        st.markdown(f"**Text Query** {'(Disabled)' if disabled_text else ''}")
        query_text = st.text_input(
            "text_query",
            placeholder="Describe what you are looking for...",
            disabled=disabled_text,
            label_visibility="collapsed"
        )
    
    with col2:
        disabled_img = query_mode == "Text Only"
        st.markdown(f"**Reference Image** {'(Disabled)' if disabled_img else ''}")
        uploaded_file = st.file_uploader(
            "image_query",
            type=['jpg', 'jpeg', 'png'],
            disabled=disabled_img,
            label_visibility="collapsed"
        )
        if uploaded_file:
            st.image(uploaded_file, caption="Preview", width=150)
            query_image = Image.open(uploaded_file)

    # Multimodal Controls
    text_weight = 0.5
    if query_mode == "Text + Image (Multimodal)":
        st.markdown("---")
        st.markdown("**⚖️ Modality Balance**")
        
        w_col1, w_col2 = st.columns([3, 1])
        with w_col1:
            text_weight = st.slider(
                "Text vs Image balance",
                0.0, 1.0, 0.5, 0.1,
                label_visibility="collapsed"
            )
        with w_col2:
            if text_weight < 0.3:
                st.markdown("🖼️ **Image Heavy**")
            elif text_weight > 0.7:
                st.markdown("📝 **Text Heavy**")
            else:
                st.markdown("⚖️ **Balanced**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Search Action
    if st.button("� Run Search & Generate", type="primary"):
        # Validation checks
        if query_mode == "Text Only" and not query_text:
            st.warning("Please enter a text query to proceed.")
            st.markdown('</div>', unsafe_allow_html=True) # Close card
            return
        if query_mode == "Image Only" and query_image is None:
            st.warning("Please upload an image to proceed.")
            st.markdown('</div>', unsafe_allow_html=True) # Close card
            return
        if query_mode == "Text + Image (Multimodal)" and (not query_text or query_image is None):
            st.warning("Please provide both text and image for multimodal search.")
            st.markdown('</div>', unsafe_allow_html=True) # Close card
            return
            
        # --- Processing ---
        st.markdown('</div>', unsafe_allow_html=True) # Close Input Card
        
        calc = MetricsCalculator()
        total_start = time.time()
        
        # 1. Retrieval
        retrieval_start = time.time()
        with st.spinner("🧠 Analyzing and retrieving..."):
            if query_mode == "Text Only":
                results = retriever.search_by_text(query_text, k=top_k)
            elif query_mode == "Image Only":
                temp_path = "temp_query.jpg"
                query_image.save(temp_path)
                results = retriever.search_by_image(temp_path, k=top_k)
                os.remove(temp_path)
            else:
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
        retrieval_metrics = calc.calculate_retrieval_metrics(results)
        
        # --- Results Display ---
        st.markdown('<div class="section-header">🏆 Top Results</div>', unsafe_allow_html=True)
        
        # Grid layout for results
        cols = st.columns(min(3, top_k))
        for idx, result in enumerate(results['results']):
            with cols[idx % 3]:
                # Individual Result Card
                st.markdown('<div class="css-card" style="padding: 1rem;">', unsafe_allow_html=True)
                
                try:
                    img = Image.open(result['image_path'])
                    st.image(img, use_container_width=True, clamp=True)
                    
                    st.markdown(f"""
                        <div style="margin-top: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                            <span class="badge badge-rank">Rank #{result['rank']}</span>
                            <span class="badge badge-score">Sim: {result['similarity_score']:.3f}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📝 View Captions"):
                         for cap in result['captions']:
                            st.markdown(f"<small>• {cap}</small>", unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error("Image load error")
                
                st.markdown('</div>', unsafe_allow_html=True) # Close card

        # --- Generation Phase ---
        all_captions = retriever.get_captions_from_results(results)
        text_gen_time = 0.0
        image_gen_time = 0.0
        text_metrics = {}
        
        # Two columns for generation outputs if both active
        gen_col1, gen_col2 = st.columns(2 if (generate_text and generate_image) else 1)
        
        # Text Generation
        if generate_text and text_gen:
            with gen_col1:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">🤖 AI Synthesis</div>', unsafe_allow_html=True)
                
                text_gen_start = time.time()
                with st.spinner("Writing description..."):
                    if query_mode == "Text Only":
                        query_str = query_text
                    elif query_mode == "Image Only":
                        query_str = "the uploaded image"
                    else:
                        query_str = f"{query_text} (with reference image)"
                    
                    context = context_builder.build_context(query_str, all_captions)
                    description = text_gen.generate_from_context(context)
                
                text_gen_time = time.time() - text_gen_start
                text_metrics = calc.calculate_text_metrics(description)
                
                st.markdown(f"""
                    <div style="background: #F3F4F6; padding: 1rem; border-radius: 0.5rem; font-style: italic; color: #4B5563;">
                        "{description}"
                    </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # Image Generation
        if generate_image and image_gen:
            target_col = gen_col2 if (generate_text and generate_image) else gen_col1
            with target_col:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">🎨 Dreamed Image</div>', unsafe_allow_html=True)
                
                image_gen_start = time.time()
                with st.spinner("Dreaming up visual..."):
                    query_str = query_text if query_mode != "Image Only" else ""
                    img_prompt = context_builder.build_image_generation_prompt(query_str, all_captions)
                    
                    with st.expander("View Prompt"):
                        st.caption(img_prompt)
                    
                    generated_img = image_gen.txt2img(img_prompt)
                    
                    if generated_img:
                        st.image(generated_img, use_container_width=True)
                    else:
                        st.error("Generation failed.")
                
                image_gen_time = time.time() - image_gen_start
                st.markdown('</div>', unsafe_allow_html=True)

        total_time = time.time() - total_start
        
        # --- Metrics Dashboard ---
        st.markdown('<div class="section-header">📊 Performance Analytics</div>', unsafe_allow_html=True)
        
        with st.expander("Show Detailed Metrics", expanded=True):
            m1, m2, m3 = st.columns(3)
            
            with m1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Avg Similarity</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{retrieval_metrics["avg_similarity"]:.3f}</div>', unsafe_allow_html=True)
                st.markdown(f'<small style="color:#6B7280">Diversity: {retrieval_metrics["diversity"]:.1%}</small>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with m2:
                if text_metrics:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.markdown('<div class="metric-label">Vocabulary Richness</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{text_metrics["vocabulary_richness"]:.1%}</div>', unsafe_allow_html=True)
                    st.markdown(f'<small style="color:#6B7280">{text_metrics["word_count"]} words</small>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No text generation metrics")
            
            with m3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.markdown('<div class="metric-label">Total Latency</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{total_time:.2f}s</div>', unsafe_allow_html=True)
                st.markdown(f'<small style="color:#6B7280">Ret: {retrieval_time:.2f}s | Gen: {text_gen_time+image_gen_time:.2f}s</small>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # --- Save to History ---
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
                    generated_text=description if generate_text and text_gen and 'description' in locals() else None,
                    text_metrics=text_metrics if text_metrics else None,
                    generated_image=generated_img if generate_image and image_gen and 'generated_img' in locals() and generated_img else None
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
                        generated_text=description if generate_text and text_gen and 'description' in locals() else None,
                        text_metrics=text_metrics if text_metrics else None,
                        generated_image=generated_img if generate_image and image_gen and 'generated_img' in locals() and generated_img else None
                    )
                    st.success(f"✅ Saved as Query #{query_id}")
                except Exception as e:
                    st.error(f"Error saving: {e}")

    else:
        # Default empty state or welcome message if needed, 
        # but the input card is already visible above.
        pass

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #9CA3AF; font-size: 0.875rem;'>"
        "Built with ❤️ using <b>COCO</b>, <b>CLIP</b>, <b>FAISS</b> & <b>Stable Diffusion</b>"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
