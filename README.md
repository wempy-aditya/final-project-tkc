# 🔍 Smart Image Search - Multimodal RAG System

A powerful Multimodal Retrieval-Augmented Generation (RAG) system that combines intelligent image search, AI-powered text generation, and image creation. Built with modern web technologies and state-of-the-art AI models.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### 🎯 Core Capabilities
- **🔍 Multimodal Search**: Search images using text descriptions, reference images, or both combined
- **🤖 AI Text Generation**: Generate intelligent descriptions using LLM with RAG context
- **🎨 AI Image Generation**: Create new images with Stable Diffusion based on search results
- **📊 Performance Metrics**: Real-time quality and performance tracking
- **💾 Search History**: Auto-save searches with full results and metrics
- **🌓 Dark Mode**: Beautiful light and dark themes

### 🌐 Modern Web Interface
- **User-Friendly Design**: Intuitive interface for both beginners and experts
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile
- **Real-time Updates**: Instant search results without page reloads
- **Interactive Components**: Smooth animations and transitions
- **RESTful API**: Decoupled backend for easy integration

### ⚡ Performance
- **Fast Search**: FAISS-powered vector similarity search
- **Efficient Indexing**: Pre-computed CLIP embeddings
- **Smart Caching**: Optimized for quick responses
- **Scalable Architecture**: Ready for production deployment

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Modern Web Frontend                      │
│         (HTML + Tailwind CSS + Vanilla JavaScript)          │
└─────────────────────┬───────────────────────────────────────┘
                      │ REST API
┌─────────────────────▼───────────────────────────────────────┐
│                    Flask Backend Server                      │
│  ┌──────────────┬──────────────┬─────────────────────────┐  │
│  │   Retriever  │ Text Gen     │  Image Gen              │  │
│  │   (CLIP +    │ (LLM)        │  (Stable Diffusion)     │  │
│  │    FAISS)    │              │                         │  │
│  └──────────────┴──────────────┴─────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Data & Storage Layer                        │
│  ┌──────────────┬──────────────┬─────────────────────────┐  │
│  │ COCO Dataset │ FAISS Index  │  SQLite History DB      │  │
│  │  (Images +   │ (Embeddings) │  (Queries + Results)    │  │
│  │   Captions)  │              │                         │  │
│  └──────────────┴──────────────┴─────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 8GB+ RAM
- GPU recommended for image generation (optional)

### Installation

#### 1. Clone the repository
```bash
git clone <repository-url>
cd multimodal-rag
```

#### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
# LLM Provider (choose one)
LLM_PROVIDER=groq  # or 'openai'
GROQ_API_KEY=your_groq_api_key_here
# OPENAI_API_KEY=your_openai_key_here

# Image Generation (optional)
HF_TOKEN=your_huggingface_token
```

#### 5. Setup dataset and embeddings
```bash
python scripts/setup.py
```

This will:
- Download COCO 2017 validation dataset (subset)
- Preprocess images and captions
- Generate CLIP embeddings
- Build FAISS index for fast retrieval

## 💻 Usage

### Option 1: Modern Web UI (Recommended)

#### Start the Flask backend:
```bash
python backend/app.py
```

The server will start at `http://localhost:5000`

#### Access the web interface:
Open your browser and navigate to:
```
http://localhost:5000
```

**Features:**
- 🎨 Beautiful, modern interface
- 🌓 Light/Dark mode toggle
- 📱 Fully responsive design
- ⚡ Real-time search results
- 💾 Automatic history saving
- 📊 Performance metrics

### Option 2: Streamlit UI (Alternative)

```bash
# Basic UI
streamlit run src/ui/app.py

# UI with metrics
streamlit run src/ui/app_with_metrics.py

# Complete UI with history
streamlit run src/ui/app_complete.py
```

### Option 3: Python API

```python
from src.retrieval.retriever import Retriever
from src.models.text_generator import TextGenerator
from src.models.image_generator import ImageGenerator

# Initialize components
retriever = Retriever()
text_gen = TextGenerator()
image_gen = ImageGenerator()

# Text-to-image search
results = retriever.search_by_text("a dog playing in the park", k=5)

# Image-to-image search
results = retriever.search_by_image("path/to/image.jpg", k=5)

# Multimodal search (text + image)
results = retriever.search_multimodal(
    text_query="sunset",
    image_path="path/to/image.jpg",
    text_weight=0.5,
    k=5
)

# Generate description
description = text_gen.generate(
    query="a dog playing",
    context=results['captions']
)

# Generate new image
image = image_gen.txt2img(prompt=description)
```

## 📁 Project Structure

```
multimodal-rag/
├── backend/                    # Flask REST API
│   ├── app.py                 # Main Flask application
│   └── requirements.txt       # Backend dependencies
│
├── frontend/                   # Modern Web UI
│   ├── index.html             # Main HTML page
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       ├── api.js             # API client
│       ├── components.js      # UI components
│       └── app.js             # Main application logic
│
├── src/                        # Core Python modules
│   ├── preprocess/            # Data preprocessing
│   │   ├── download_coco.py
│   │   └── generate_embeddings.py
│   ├── retrieval/             # Search engine
│   │   └── retriever.py
│   ├── models/                # AI models
│   │   ├── context_builder.py
│   │   ├── text_generator.py
│   │   └── image_generator.py
│   ├── utils/                 # Utilities
│   │   ├── metrics_calculator.py
│   │   └── history_manager.py
│   └── ui/                    # Streamlit UIs
│       ├── app.py
│       ├── app_with_metrics.py
│       └── app_complete.py
│
├── data/                       # Dataset storage
│   └── coco/
│       ├── images/
│       └── annotations/
│
├── embeddings/                 # Pre-computed embeddings
│   ├── image_embeddings.npy
│   ├── metadata.json
│   └── faiss_index.bin
│
├── history/                    # Search history
│   ├── queries.db             # SQLite database
│   ├── query_images/          # Uploaded query images
│   └── generated_images/      # AI-generated images
│
├── scripts/                    # Utility scripts
│   └── setup.py
│
├── config/                     # Configuration
│   └── config.yaml
│
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── SETUP_GUIDE.md             # Detailed setup instructions
├── WEB_UI_GUIDE.md            # Web UI deployment guide
└── HISTORY_GUIDE.md           # History feature guide
```

## 🎨 Web UI Features

### Search Modes
1. **Text Search**: Describe what you're looking for
2. **Image Search**: Upload a reference photo
3. **Smart Search**: Combine text + image for best results

### AI Features
- **Write Description**: AI explains the search results
- **Create New Image**: Generate similar images with AI
- **Save Searches**: Auto-save to history for later review

### Customization
- **Results Count**: Choose how many results to show (1-10)
- **Search Balance**: Adjust text vs image weight in multimodal search
- **Theme**: Toggle between light and dark modes

### Performance Metrics
- **Retrieval Quality**: Similarity scores, diversity metrics
- **Generation Quality**: Word count, vocabulary richness
- **Response Time**: Track search and generation speed

## 🔧 Configuration

### Backend Configuration
Edit `backend/app.py` to customize:
- Server port (default: 5000)
- CORS settings
- File upload limits

### Frontend Configuration
Edit `frontend/js/api.js` to change:
- API base URL
- Request timeout
- Error handling

### Model Configuration
Edit `config/config.yaml` for:
- CLIP model variant
- LLM parameters (temperature, max tokens)
- Image generation settings
- Retrieval thresholds

## 📊 API Endpoints

### Search Endpoints
- `POST /api/search/text` - Text-based search
- `POST /api/search/image` - Image-based search
- `POST /api/search/multimodal` - Combined search

### Generation Endpoints
- `POST /api/generate/text` - Generate description
- `POST /api/generate/image` - Generate image

### History Endpoints
- `GET /api/history` - Get all queries
- `GET /api/history/{id}` - Get specific query
- `DELETE /api/history/{id}` - Delete query
- `GET /api/history/stats` - Get statistics
- `POST /api/history/save` - Save new query

### Utility
- `GET /api/health` - Health check

## 🔑 API Keys & Models

### LLM Providers (Choose One)
1. **Groq** (Recommended - Fast & Free)
   - Sign up at https://console.groq.com
   - Get API key
   - Add to `.env`: `GROQ_API_KEY=your_key`

2. **OpenAI**
   - Sign up at https://platform.openai.com
   - Get API key
   - Add to `.env`: `OPENAI_API_KEY=your_key`

### Image Generation (Optional)
- **Hugging Face** for Stable Diffusion
  - Sign up at https://huggingface.co
  - Get token
  - Add to `.env`: `HF_TOKEN=your_token`

## 📈 Performance Metrics

The system tracks:

### Retrieval Metrics
- **Average Similarity**: Quality of retrieved results
- **Diversity Score**: Variety in results
- **Retrieval Time**: Speed of search

### Generation Metrics
- **Word Count**: Length of generated text
- **Sentence Count**: Structure analysis
- **Vocabulary Richness**: Language diversity
- **Generation Time**: AI processing speed

## 💾 Search History

All searches are automatically saved with:
- Query details (text, image, mode)
- Retrieved images and scores
- Generated descriptions
- Generated images
- Performance metrics
- Timestamp

Access history through:
- Web UI sidebar
- API endpoints
- SQLite database directly

## 🌐 Deployment

### Development
```bash
python backend/app.py
```

### Production

#### Option 1: Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

#### Option 2: Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "backend/app.py"]
```

#### Option 3: Cloud Platforms
- **Heroku**: Use Procfile
- **Railway**: Auto-detect Python
- **Render**: Use render.yaml

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Test coverage:
```bash
pytest --cov=src tests/
```

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check dependencies
pip install -r requirements.txt

# Check port availability
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/Mac
```

### CORS errors
- Ensure Flask-CORS is installed
- Check `backend/app.py` CORS configuration

### Images not loading
- Verify dataset is downloaded
- Check embeddings are generated
- Ensure file paths are correct

### API errors
- Check API keys in `.env`
- Verify internet connection
- Check API rate limits

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)**: Detailed installation guide
- **[WEB_UI_GUIDE.md](WEB_UI_GUIDE.md)**: Web interface documentation
- **[HISTORY_GUIDE.md](HISTORY_GUIDE.md)**: History feature guide
- **[METRICS_GUIDE.md](METRICS_GUIDE.md)**: Metrics explanation

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

### Datasets & Models
- **COCO Dataset**: Microsoft COCO Team
- **CLIP**: OpenAI
- **FAISS**: Facebook AI Research
- **Stable Diffusion**: Stability AI

### Libraries & Frameworks
- **Flask**: Web framework
- **Streamlit**: Rapid prototyping
- **Hugging Face**: Transformers & Diffusers
- **Tailwind CSS**: UI styling

### APIs
- **Groq**: Fast LLM inference
- **OpenAI**: GPT models
- **Hugging Face**: Model hosting

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## 🎯 Roadmap

### Completed ✅
- ✅ Multimodal search (text, image, combined)
- ✅ AI text generation with RAG
- ✅ AI image generation
- ✅ Performance metrics tracking
- ✅ Search history with SQLite
- ✅ Modern web UI with dark mode
- ✅ RESTful API backend
- ✅ Responsive design

### Planned 🚧
- 🚧 User authentication
- 🚧 Multi-user support
- 🚧 Advanced filters
- 🚧 Batch processing
- 🚧 Export functionality
- 🚧 Mobile app
- 🚧 More LLM providers
- 🚧 Custom dataset support

---

**Built with ❤️ for intelligent image search**

*Version 2.0 - Modern Web UI Edition*