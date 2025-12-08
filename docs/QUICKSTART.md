# Quick Start Guide

## Prerequisites
- Python 3.8+
- 8GB+ RAM
- GPU recommended (for Stable Diffusion)
- API keys (OpenAI or Groq)

## Installation

### 1. Clone and Setup
```bash
cd multimodal-rag
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Download Data and Build Index
```bash
python scripts/setup.py
```

This will:
- Download COCO dataset (10000 images, ~2GB)
- Generate CLIP embeddings (~10-15 minutes)
- Build FAISS index

## Usage

### Run Web UI
```bash
streamlit run src/ui/app.py
```

### Python API
```python
from src.retrieval.retriever import Retriever
from src.models.text_generator import TextGenerator

retriever = Retriever()
text_gen = TextGenerator()

# Search
results = retriever.search_by_text("a dog playing", k=5)

# Generate
description = text_gen.generate_from_context(context)
```

## Optional: Stable Diffusion Setup

### Option 1: Google Colab (Recommended)
1. Open `notebooks/colab_sd_server.ipynb` in Colab
2. Set runtime to GPU (T4)
3. Run all cells
4. Copy the ngrok URL to your `.env` file

### Option 2: Local (Requires GPU)
Set in `.env`:
```
SD_API_URL=local
```

## Troubleshooting

**Issue: Out of memory during embedding generation**
- Reduce batch size: `python src/preprocess/generate_embeddings.py --batch_size 16`

**Issue: COCO download fails**
- Download manually from http://cocodataset.org
- Place in `data/coco/`

**Issue: LLM API errors**
- Check API key in `.env`
- Verify API credits

## Next Steps
- Run evaluation: `python scripts/run_evaluation.py`
- Customize prompts in `src/models/context_builder.py`
- Adjust retrieval parameters in `config/config.yaml`
