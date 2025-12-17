# Modern Web UI - Deployment Guide

## 🚀 Quick Start

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Backend Server

```bash
python app.py
```

Backend akan running di: `http://localhost:5000`

### 3. Access Frontend

Buka browser dan akses: `http://localhost:5000`

Frontend akan otomatis di-serve oleh Flask!

---

## 📁 Project Structure

```
multimodal-rag/
├── backend/
│   ├── app.py              # Flask REST API
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── index.html          # Main HTML
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       ├── api.js          # API client
│       ├── components.js   # UI components
│       └── app.js          # Main logic
│
└── src/                    # Existing RAG system (unchanged)
```

---

## ✨ Features

### All Streamlit Features + More:

✅ **Multimodal Search**
- Text-only search
- Image-only search  
- Text + Image (multimodal) with weight control

✅ **AI Generation**
- Text description generation
- Image generation (if available)

✅ **Query History**
- Auto-save queries
- Load previous results
- Delete history entries
- Statistics dashboard

✅ **Performance Metrics**
- Retrieval quality metrics
- Generation metrics
- Response time tracking

✅ **Modern UI/UX**
- Gradient headers
- Card-based layout
- Smooth animations
- Responsive design
- Toast notifications

---

## 🎨 UI Highlights

### Design Features:
- **Tailwind CSS** - Modern utility-first CSS
- **Font Awesome** - Beautiful icons
- **Gradient Backgrounds** - Eye-catching colors
- **Smooth Transitions** - Professional animations
- **Responsive Grid** - Works on all devices

### Color Palette:
- Primary: Indigo (#4F46E5)
- Secondary: Green (#10B981)
- Accent: Purple (#7C3AED)

---

## 🔌 API Endpoints

### Search
- `POST /api/search/text` - Text search
- `POST /api/search/image` - Image search
- `POST /api/search/multimodal` - Multimodal search

### Generation
- `POST /api/generate/text` - Generate description
- `POST /api/generate/image` - Generate image

### History
- `GET /api/history` - Get all queries
- `GET /api/history/{id}` - Get specific query
- `DELETE /api/history/{id}` - Delete query
- `GET /api/history/stats` - Get statistics
- `POST /api/history/save` - Save query

### Utility
- `GET /api/health` - Health check

---

## 🛠️ Development

### Backend Development:
```bash
cd backend
python app.py
```

Flask akan auto-reload saat ada perubahan code.

### Frontend Development:
Edit files di `frontend/` folder. Refresh browser untuk melihat perubahan.

---

## 📱 Responsive Design

UI otomatis menyesuaikan untuk:
- 💻 Desktop (1024px+)
- 📱 Tablet (768px - 1023px)
- 📱 Mobile (<768px)

---

## 🎯 Comparison: Streamlit vs Modern Web UI

| Feature | Streamlit | Modern Web UI |
|---------|-----------|---------------|
| **Performance** | Reload on every interaction | No reload, instant updates |
| **Customization** | Limited | Full control |
| **Design** | Basic | Modern & Professional |
| **Animations** | None | Smooth transitions |
| **Responsive** | Limited | Fully responsive |
| **Deployment** | Streamlit Cloud | Any web server |
| **API** | No | Yes (RESTful) |

---

## 🚢 Production Deployment

### Option 1: Single Server (Recommended for simple deployment)

```bash
# Backend serves frontend
python backend/app.py
```

Access: `http://your-server:5000`

### Option 2: Separate Deployment

**Backend:**
- Deploy to Heroku, Railway, or Render
- Set environment variables

**Frontend:**
- Deploy to Vercel or Netlify
- Update `API_BASE_URL` in `frontend/js/api.js`

### Option 3: Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r backend/requirements.txt
EXPOSE 5000
CMD ["python", "backend/app.py"]
```

---

## 🔧 Configuration

### Backend Port:
Edit `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### API URL:
Edit `frontend/js/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

---

## 🐛 Troubleshooting

### Backend tidak start:
```bash
# Check dependencies
pip install -r backend/requirements.txt

# Check port
netstat -ano | findstr :5000
```

### CORS Error:
Backend sudah include `flask-cors`. Pastikan running.

### Images tidak muncul:
Check console browser untuk error. Pastikan backend dapat akses dataset images.

---

## 📝 Notes

- Semua fitur Streamlit tetap ada
- Tidak ada perubahan pada `src/` folder
- Database history tetap di `history/queries.db`
- Compatible dengan existing setup

---

## 🎉 Enjoy!

Modern web UI yang lebih cepat, lebih cantik, dan lebih fleksibel! 🚀
