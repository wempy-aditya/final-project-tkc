"""
Flask REST API Backend for Multimodal RAG System
Provides endpoints for search, generation, and history management
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sys
from pathlib import Path
import os
import time
from PIL import Image
import io
import base64

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.retrieval.retriever import Retriever
from src.models.context_builder import ContextBuilder
from src.models.text_generator import TextGenerator
from src.models.image_generator import ImageGenerator
from src.utils.metrics_calculator import MetricsCalculator
from src.utils.history_manager import HistoryManager

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configure upload folder
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize components
print("Initializing components...")
retriever = Retriever()
context_builder = ContextBuilder()
text_gen = TextGenerator()
try:
    image_gen = ImageGenerator(use_local=False)
except Exception as e:
    print(f"Image generator not available: {e}")
    image_gen = None

calc = MetricsCalculator()
history_manager = HistoryManager()
print("Components initialized!")


# ============= SEARCH ENDPOINTS =============

@app.route('/api/search/text', methods=['POST'])
def search_text():
    """Search by text query"""
    try:
        data = request.json
        query = data['query']
        top_k = data.get('top_k', 5)
        
        # Perform search
        start_time = time.time()
        results = retriever.search_by_text(query, k=top_k)
        retrieval_time = time.time() - start_time
        
        # Calculate metrics
        metrics = calc.calculate_retrieval_metrics(results)
        metrics['retrieval_time'] = retrieval_time
        
        # Convert image paths to base64 for web display
        for result in results['results']:
            try:
                with Image.open(result['image_path']) as img:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    result['image_base64'] = f"data:image/jpeg;base64,{img_str}"
            except Exception as e:
                result['image_base64'] = None
                print(f"Error encoding image: {e}")
        
        return jsonify({
            'success': True,
            'query_type': 'text',
            'results': results['results'],
            'metrics': metrics
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search/image', methods=['POST'])
def search_image():
    """Search by image"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        top_k = int(request.form.get('top_k', 5))
        
        # Save uploaded image temporarily
        filename = secure_filename(image_file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(temp_path)
        
        # Perform search
        start_time = time.time()
        results = retriever.search_by_image(temp_path, k=top_k)
        retrieval_time = time.time() - start_time
        
        # Calculate metrics
        metrics = calc.calculate_retrieval_metrics(results)
        metrics['retrieval_time'] = retrieval_time
        
        # Convert images to base64
        for result in results['results']:
            try:
                with Image.open(result['image_path']) as img:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    result['image_base64'] = f"data:image/jpeg;base64,{img_str}"
            except Exception as e:
                result['image_base64'] = None
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'query_type': 'image',
            'results': results['results'],
            'metrics': metrics
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search/multimodal', methods=['POST'])
def search_multimodal():
    """Search by text + image (multimodal)"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        query_text = request.form.get('query')
        image_file = request.files['image']
        text_weight = float(request.form.get('text_weight', 0.5))
        top_k = int(request.form.get('top_k', 5))
        
        # Save uploaded image temporarily
        filename = secure_filename(image_file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(temp_path)
        
        # Perform search
        start_time = time.time()
        results = retriever.search_by_multimodal(
            query_text=query_text,
            query_image=temp_path,
            text_weight=text_weight,
            k=top_k
        )
        retrieval_time = time.time() - start_time
        
        # Calculate metrics
        metrics = calc.calculate_retrieval_metrics(results)
        metrics['retrieval_time'] = retrieval_time
        
        # Convert images to base64
        for result in results['results']:
            try:
                with Image.open(result['image_path']) as img:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    result['image_base64'] = f"data:image/jpeg;base64,{img_str}"
            except Exception as e:
                result['image_base64'] = None
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'query_type': 'multimodal',
            'text_weight': text_weight,
            'results': results['results'],
            'metrics': metrics
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============= GENERATION ENDPOINTS =============

@app.route('/api/generate/text', methods=['POST'])
def generate_text():
    """Generate text description"""
    try:
        data = request.json
        query = data['query']
        captions = data['captions']
        query_mode = data.get('query_mode', 'text')
        
        # Build context
        if query_mode == 'text':
            query_str = query
        elif query_mode == 'image':
            query_str = "the uploaded image"
        else:
            query_str = f"{query} (with reference image)"
        
        # Generate text
        start_time = time.time()
        context = context_builder.build_context(query_str, captions)
        description = text_gen.generate_from_context(context)
        generation_time = time.time() - start_time
        
        # Calculate metrics
        text_metrics = calc.calculate_text_metrics(description)
        
        return jsonify({
            'success': True,
            'description': description,
            'metrics': text_metrics,
            'generation_time': generation_time
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate/image', methods=['POST'])
def generate_image():
    """Generate image from prompt"""
    try:
        if not image_gen:
            return jsonify({
                'success': False,
                'error': 'Image generation not available'
            }), 503
        
        data = request.json
        query = data.get('query', '')
        captions = data['captions']
        
        # Build prompt
        img_prompt = context_builder.build_image_generation_prompt(query, captions)
        
        # Generate image
        start_time = time.time()
        generated_img = image_gen.txt2img(img_prompt)
        generation_time = time.time() - start_time
        
        if generated_img:
            # Convert to base64
            buffered = io.BytesIO()
            generated_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return jsonify({
                'success': True,
                'image_base64': f"data:image/jpeg;base64,{img_str}",
                'prompt': img_prompt,
                'generation_time': generation_time
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Image generation failed'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============= HISTORY ENDPOINTS =============

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get all queries from history"""
    try:
        limit = int(request.args.get('limit', 20))
        queries = history_manager.get_all_queries(limit=limit)
        
        return jsonify({
            'success': True,
            'queries': queries,
            'total': len(queries)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history/<int:query_id>', methods=['GET'])
def get_query(query_id):
    """Get specific query by ID"""
    try:
        query = history_manager.get_query_by_id(query_id)
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query not found'
            }), 404
        
        # Convert images to base64
        for result in query['retrieval_results']:
            try:
                with Image.open(result['image_path']) as img:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    result['image_base64'] = f"data:image/jpeg;base64,{img_str}"
            except Exception as e:
                result['image_base64'] = None
        
        # Load query image if exists
        if query['query_image_path']:
            try:
                with Image.open(query['query_image_path']) as img:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    query['query_image_base64'] = f"data:image/jpeg;base64,{img_str}"
            except Exception as e:
                query['query_image_base64'] = None
        
        # Load generated image if exists
        if query['generated_image_path']:
            try:
                with Image.open(query['generated_image_path']) as img:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    query['generated_image_base64'] = f"data:image/jpeg;base64,{img_str}"
            except Exception as e:
                query['generated_image_base64'] = None
        
        return jsonify({
            'success': True,
            'query': query
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history/<int:query_id>', methods=['DELETE'])
def delete_query(query_id):
    """Delete query from history"""
    try:
        success = history_manager.delete_query(query_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Query deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete query'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history/stats', methods=['GET'])
def get_stats():
    """Get history statistics"""
    try:
        stats = history_manager.get_statistics()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history/save', methods=['POST'])
def save_to_history():
    """Save query to history"""
    try:
        data = request.json
        
        # Extract data
        query_data = data['query_data']
        results = data['results']
        retrieval_metrics = data['retrieval_metrics']
        performance = data['performance']
        generated_text = data.get('generated_text')
        text_metrics = data.get('text_metrics')
        
        # Handle query image if base64
        query_image = None
        if 'query_image_base64' in query_data and query_data['query_image_base64']:
            # Decode base64 to PIL Image
            img_data = query_data['query_image_base64'].split(',')[1]
            img_bytes = base64.b64decode(img_data)
            query_image = Image.open(io.BytesIO(img_bytes))
            query_data['query_image'] = query_image
        
        # Handle generated image if base64
        generated_image = None
        if 'generated_image_base64' in data and data['generated_image_base64']:
            img_data = data['generated_image_base64'].split(',')[1]
            img_bytes = base64.b64decode(img_data)
            generated_image = Image.open(io.BytesIO(img_bytes))
        
        # Save to history
        query_id = history_manager.save_query(
            query_data=query_data,
            results={'results': results},
            retrieval_metrics=retrieval_metrics,
            performance=performance,
            generated_text=generated_text,
            text_metrics=text_metrics,
            generated_image=generated_image
        )
        
        return jsonify({
            'success': True,
            'query_id': query_id,
            'message': f'Saved as Query #{query_id}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============= UTILITY ENDPOINTS =============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'components': {
            'retriever': retriever is not None,
            'text_generator': text_gen is not None,
            'image_generator': image_gen is not None,
            'history_manager': history_manager is not None
        }
    })


@app.route('/')
def index():
    """Serve frontend"""
    return send_from_directory('../frontend', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('../frontend', path)


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Multimodal RAG API Server")
    print("="*50)
    print("Server running on: http://localhost:5000")
    print("API endpoints: http://localhost:5000/api")
    print("Frontend: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
