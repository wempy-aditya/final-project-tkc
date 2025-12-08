"""
Retriever Module
Main retrieval engine for text-to-image and image-to-image search
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Union
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.clip_encoder import CLIPEncoder
from src.retrieval.faiss_index import FAISSIndex


class Retriever:
    def __init__(
        self,
        embeddings_dir: str = "embeddings",
        clip_model: str = "openai/clip-vit-base-patch32"
    ):
        """
        Initialize retriever
        
        Args:
            embeddings_dir: Directory containing embeddings and index
            clip_model: CLIP model name
        """
        self.embeddings_dir = Path(embeddings_dir)
        
        # Load metadata
        meta_file = self.embeddings_dir / "meta.json"
        print(f"Loading metadata from {meta_file}")
        with open(meta_file, 'r') as f:
            self.metadata = json.load(f)
        
        # Initialize CLIP encoder
        print("Initializing CLIP encoder...")
        self.encoder = CLIPEncoder(model_name=clip_model)
        
        # Load FAISS index
        print("Loading FAISS index...")
        self.index = FAISSIndex(embedding_dim=self.encoder.embedding_dim)
        index_file = self.embeddings_dir / "faiss_index.bin"
        self.index.load(str(index_file))
        
        print(f"Retriever initialized with {len(self.metadata)} images")
    
    def search_by_text(self, query: str, k: int = 5) -> Dict:
        """
        Search images by text query
        
        Args:
            query: Text query
            k: Number of results to return
            
        Returns:
            Dictionary with results
        """
        # Encode query
        query_embedding = self.encoder.encode_text(query)
        
        # Search
        distances, indices = self.index.search(query_embedding, k=k)
        
        # Prepare results
        results = {
            'query': query,
            'query_type': 'text',
            'results': []
        }
        
        for idx, (distance, index) in enumerate(zip(distances, indices)):
            if index < len(self.metadata):
                meta = self.metadata[index]
                results['results'].append({
                    'rank': idx + 1,
                    'image_path': meta['path'],
                    'file_name': meta['file_name'],
                    'captions': meta['captions'],
                    'similarity_score': float(distance),
                    'image_id': meta['image_id']
                })
        
        return results
    
    def search_by_image(self, image_path: str, k: int = 5) -> Dict:
        """
        Search images by image query
        
        Args:
            image_path: Path to query image
            k: Number of results to return
            
        Returns:
            Dictionary with results
        """
        # Encode image
        query_embedding = self.encoder.encode_image(image_path)
        
        # Search
        distances, indices = self.index.search(query_embedding, k=k)
        
        # Prepare results
        results = {
            'query': image_path,
            'query_type': 'image',
            'results': []
        }
        
        for idx, (distance, index) in enumerate(zip(distances, indices)):
            if index < len(self.metadata):
                meta = self.metadata[index]
                results['results'].append({
                    'rank': idx + 1,
                    'image_path': meta['path'],
                    'file_name': meta['file_name'],
                    'captions': meta['captions'],
                    'similarity_score': float(distance),
                    'image_id': meta['image_id']
                })
        
        return results
    
    def get_captions_from_results(self, results: Dict) -> List[str]:
        """Extract all captions from search results"""
        captions = []
        for result in results['results']:
            captions.extend(result['captions'])
        return captions


if __name__ == "__main__":
    # Test retriever
    retriever = Retriever()
    
    # Test text search
    print("\n=== Text Search Test ===")
    results = retriever.search_by_text("a dog playing in the park", k=3)
    
    print(f"Query: {results['query']}")
    for res in results['results']:
        print(f"\nRank {res['rank']}: {res['file_name']}")
        print(f"Score: {res['similarity_score']:.4f}")
        print(f"Captions: {res['captions'][0]}")
