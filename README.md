# Multimodal RAG System

A Multimodal Retrieval-Augmented Generation (RAG) system that combines image retrieval, text generation, and image generation using COCO dataset, CLIP embeddings, FAISS indexing, LLM, and Stable Diffusion.

## Features

- 🔍 **Multimodal Retrieval**: Search images using text or image queries
- 🤖 **Text Generation**: Generate descriptions using LLM with RAG context
- 🎨 **Image Generation**: Create new images with Stable Diffusion
- 🌐 **Web Interface**: Interactive Streamlit UI
- ⚡ **Fast Search**: FAISS-powered vector similarity search

## System Architecture

```
User Query (Text/Image) → CLIP Encoder → FAISS Index → Retrieved Images
                                                              ↓
                                                      Context Builder
                                                              ↓
                                                    ┌─────────┴─────────┐
                                                    ↓                   ↓
                                            Text Generator      Image Generator
                                               (LLM)          (Stable Diffusion)
```

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd multimodal-rag
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 5. Download COCO dataset and generate embeddings
```bash
python scripts/setup.py
```

This will:
- Download COCO 2017 validation dataset (subset)
- Preprocess images
- Generate CLIP embeddings
- Build FAISS index

## Usage

### Run the Streamlit Web UI
```bash
streamlit run src/ui/app.py
```

### Python API Usage

```python
from src.retrieval.retriever import Retriever
from src.models.text_generator import TextGenerator
from src.models.image_generator import ImageGenerator

# Initialize components
retriever = Retriever()
text_gen = TextGenerator()
image_gen = ImageGenerator()

# Text-to-image retrieval
results = retriever.search_by_text("a dog playing in the park", k=5)

# Generate description
description = text_gen.generate(query="a dog playing", context=results['captions'])

# Generate image
image = image_gen.txt2img(prompt=description)
```

## Project Structure

```
multimodal-rag/
├── data/                    # COCO dataset
│   ├── coco/
│   │   ├── images/
│   │   └── annotations/
│   └── processed/
├── embeddings/              # CLIP embeddings and FAISS index
├── src/
│   ├── preprocess/          # Data preprocessing scripts
│   ├── retrieval/           # Retrieval engine
│   ├── models/              # LLM and SD models
│   ├── ui/                  # Streamlit UI
│   └── evaluation/          # Evaluation metrics
├── scripts/                 # Utility scripts
├── config/                  # Configuration files
├── notebooks/               # Jupyter notebooks
└── tests/                   # Unit tests
```

## Configuration

Edit `config/config.yaml` to customize:
- Model parameters
- Retrieval settings (top-k, threshold)
- Generation parameters (temperature, steps)
- Paths

## API Keys Required

- **OpenAI API Key** (for GPT-4o-mini) OR **Groq API Key** (for Llama 3)
- Optional: Stable Diffusion API (or run locally with GPU)

## Evaluation

Run evaluation metrics:
```bash
python scripts/run_evaluation.py
```

Metrics include:
- **Retrieval**: Precision@k, Recall@k, mAP
- **Text Generation**: BLEU, ROUGE, CIDEr

## Requirements

- Python 3.8+
- 8GB+ RAM
- GPU recommended for Stable Diffusion (can use Colab)

## License

MIT License

## Acknowledgments

- COCO Dataset
- OpenAI CLIP
- FAISS
- Hugging Face Transformers & Diffusers


MAU PINDAH KE VIRTUAL ENV (VENV) PYTHON : 
venv\Scripts\activate

PR PROGRESS SELANJUTNA
- PERBAIKI TAMPILAN WEB
- LENGKAPI EVALUASI METRIK
- TAMBAHKAN FITUR MULTIMODAL QUERY
- CARI API LLM YANG STABIL DAN CEPET