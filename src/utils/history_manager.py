"""
History Manager for Query Storage
Manages SQLite database and file storage for query history
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import shutil
from PIL import Image
from typing import Dict, List, Optional


class HistoryManager:
    """Manage query history with SQLite database"""
    
    def __init__(self, db_path='history/queries.db'):
        """
        Initialize history manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.history_dir = Path('history')
        self.query_images_dir = self.history_dir / 'query_images'
        self.generated_images_dir = self.history_dir / 'generated_images'
        
        # Create directories
        self.history_dir.mkdir(exist_ok=True)
        self.query_images_dir.mkdir(exist_ok=True)
        self.generated_images_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self._init_db()
    
    def _init_db(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create queries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                query_mode TEXT NOT NULL,
                query_text TEXT,
                query_image_path TEXT,
                text_weight REAL,
                top_k INTEGER,
                
                -- Retrieval Metrics
                retrieval_time REAL,
                avg_similarity REAL,
                diversity REAL,
                min_similarity REAL,
                max_similarity REAL,
                std_similarity REAL,
                
                -- Generation Results
                generated_text TEXT,
                generated_image_path TEXT,
                
                -- Text Metrics
                word_count INTEGER,
                sentence_count INTEGER,
                vocabulary_richness REAL,
                avg_word_length REAL,
                
                -- Performance
                text_gen_time REAL,
                image_gen_time REAL,
                total_time REAL
            )
        ''')
        
        # Create retrieval results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS retrieval_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER NOT NULL,
                rank INTEGER NOT NULL,
                image_path TEXT NOT NULL,
                file_name TEXT NOT NULL,
                similarity_score REAL NOT NULL,
                captions TEXT NOT NULL,
                
                FOREIGN KEY (query_id) REFERENCES queries(id) ON DELETE CASCADE
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_query_timestamp 
            ON queries(timestamp DESC)
        ''')
        
        conn.commit()
        conn.close()
    
    def _save_query_image(self, image: Image.Image, query_id: int) -> str:
        """
        Save query image to disk
        
        Args:
            image: PIL Image object
            query_id: Query ID for filename
            
        Returns:
            Path to saved image
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"query_{query_id}_{timestamp}.jpg"
        filepath = self.query_images_dir / filename
        
        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        image.save(filepath, 'JPEG', quality=95)
        return str(filepath)
    
    def _save_generated_image(self, image: Image.Image, query_id: int) -> str:
        """
        Save generated image to disk
        
        Args:
            image: PIL Image object
            query_id: Query ID for filename
            
        Returns:
            Path to saved image
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"gen_{query_id}_{timestamp}.jpg"
        filepath = self.generated_images_dir / filename
        
        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        image.save(filepath, 'JPEG', quality=95)
        return str(filepath)
    
    def save_query(
        self,
        query_data: Dict,
        results: Dict,
        retrieval_metrics: Dict,
        performance: Dict,
        generated_text: Optional[str] = None,
        text_metrics: Optional[Dict] = None,
        generated_image: Optional[Image.Image] = None
    ) -> int:
        """
        Save complete query to database
        
        Args:
            query_data: Query information (mode, text, image, etc.)
            results: Retrieval results
            retrieval_metrics: Retrieval quality metrics
            performance: Performance metrics
            generated_text: Generated text description
            text_metrics: Text generation metrics
            generated_image: Generated image
            
        Returns:
            Query ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert query first to get ID
            cursor.execute('''
                INSERT INTO queries (
                    query_mode, query_text, text_weight, top_k,
                    retrieval_time, avg_similarity, diversity, 
                    min_similarity, max_similarity, std_similarity,
                    generated_text,
                    word_count, sentence_count, vocabulary_richness, avg_word_length,
                    text_gen_time, image_gen_time, total_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                query_data['query_mode'],
                query_data.get('query_text'),
                query_data.get('text_weight'),
                query_data['top_k'],
                performance['retrieval_time'],
                retrieval_metrics['avg_similarity'],
                retrieval_metrics['diversity'],
                retrieval_metrics['min_similarity'],
                retrieval_metrics['max_similarity'],
                retrieval_metrics['std_similarity'],
                generated_text,
                text_metrics.get('word_count') if text_metrics else None,
                text_metrics.get('sentence_count') if text_metrics else None,
                text_metrics.get('vocabulary_richness') if text_metrics else None,
                text_metrics.get('avg_word_length') if text_metrics else None,
                performance.get('text_gen_time', 0),
                performance.get('image_gen_time', 0),
                performance['total_time']
            ))
            
            query_id = cursor.lastrowid
            
            # Save query image if provided
            if query_data.get('query_image'):
                query_image_path = self._save_query_image(
                    query_data['query_image'],
                    query_id
                )
                cursor.execute(
                    'UPDATE queries SET query_image_path = ? WHERE id = ?',
                    (query_image_path, query_id)
                )
            
            # Save generated image if provided
            if generated_image:
                gen_image_path = self._save_generated_image(
                    generated_image,
                    query_id
                )
                cursor.execute(
                    'UPDATE queries SET generated_image_path = ? WHERE id = ?',
                    (gen_image_path, query_id)
                )
            
            # Insert retrieval results
            for result in results['results']:
                cursor.execute('''
                    INSERT INTO retrieval_results (
                        query_id, rank, image_path, file_name,
                        similarity_score, captions
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    query_id,
                    result['rank'],
                    result['image_path'],
                    result['file_name'],
                    result['similarity_score'],
                    json.dumps(result['captions'])
                ))
            
            conn.commit()
            return query_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_all_queries(self, limit: int = 50) -> List[Dict]:
        """
        Get recent queries
        
        Args:
            limit: Maximum number of queries to return
            
        Returns:
            List of query dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM queries
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        queries = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return queries
    
    def get_query_by_id(self, query_id: int) -> Optional[Dict]:
        """
        Get specific query with all results
        
        Args:
            query_id: Query ID
            
        Returns:
            Query dictionary with results, or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get query
        cursor.execute('SELECT * FROM queries WHERE id = ?', (query_id,))
        query = cursor.fetchone()
        
        if not query:
            conn.close()
            return None
        
        query_dict = dict(query)
        
        # Get retrieval results
        cursor.execute('''
            SELECT * FROM retrieval_results
            WHERE query_id = ?
            ORDER BY rank
        ''', (query_id,))
        
        results = []
        for row in cursor.fetchall():
            result = dict(row)
            result['captions'] = json.loads(result['captions'])
            results.append(result)
        
        query_dict['retrieval_results'] = results
        
        conn.close()
        return query_dict
    
    def delete_query(self, query_id: int) -> bool:
        """
        Delete query and associated files
        
        Args:
            query_id: Query ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get file paths before deleting
            cursor.execute(
                'SELECT query_image_path, generated_image_path FROM queries WHERE id = ?',
                (query_id,)
            )
            row = cursor.fetchone()
            
            if row:
                # Delete files
                if row[0] and Path(row[0]).exists():
                    Path(row[0]).unlink()
                if row[1] and Path(row[1]).exists():
                    Path(row[1]).unlink()
            
            # Delete from database (CASCADE will delete retrieval_results)
            cursor.execute('DELETE FROM queries WHERE id = ?', (query_id,))
            conn.commit()
            
            return True
            
        except Exception as e:
            conn.rollback()
            print(f"Error deleting query: {e}")
            return False
        finally:
            conn.close()
    
    def get_statistics(self) -> Dict:
        """
        Get usage statistics
        
        Returns:
            Dictionary with statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total queries
        cursor.execute('SELECT COUNT(*) FROM queries')
        total_queries = cursor.fetchone()[0]
        
        # Average metrics
        cursor.execute('''
            SELECT 
                AVG(avg_similarity) as avg_sim,
                AVG(diversity) as avg_div,
                AVG(total_time) as avg_time
            FROM queries
        ''')
        row = cursor.fetchone()
        
        # Query mode distribution
        cursor.execute('''
            SELECT query_mode, COUNT(*) as count
            FROM queries
            GROUP BY query_mode
        ''')
        mode_dist = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_queries': total_queries,
            'avg_similarity': row[0] if row[0] else 0,
            'avg_diversity': row[1] if row[1] else 0,
            'avg_time': row[2] if row[2] else 0,
            'mode_distribution': mode_dist
        }


if __name__ == "__main__":
    # Test history manager
    manager = HistoryManager()
    print("History manager initialized successfully!")
    print(f"Database: {manager.db_path}")
    print(f"Query images: {manager.query_images_dir}")
    print(f"Generated images: {manager.generated_images_dir}")
    
    # Get statistics
    stats = manager.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total queries: {stats['total_queries']}")
    print(f"  Avg similarity: {stats['avg_similarity']:.3f}")
    print(f"  Avg time: {stats['avg_time']:.2f}s")
