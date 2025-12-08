"""
FAISS Index Module
Handles building and searching FAISS index for image retrieval
"""

import numpy as np
import faiss
from pathlib import Path
from typing import Tuple, List
import pickle


class FAISSIndex:
    def __init__(self, embedding_dim: int = 512):
        """
        Initialize FAISS index
        
        Args:
            embedding_dim: Dimension of embeddings
        """
        self.embedding_dim = embedding_dim
        self.index = None
        
    def build_index(self, embeddings: np.ndarray, normalize: bool = True):
        """
        Build FAISS index from embeddings
        
        Args:
            embeddings: Numpy array of embeddings (N x D)
            normalize: Whether to normalize embeddings for cosine similarity
        """
        if normalize:
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
        
        # Create IndexFlatIP (Inner Product) for cosine similarity
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
        print(f"FAISS index built with {self.index.ntotal} vectors")
        
    def search(self, query_embedding: np.ndarray, k: int = 5, normalize: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Search for top-k similar embeddings
        
        Args:
            query_embedding: Query embedding (1 x D or D)
            k: Number of results to return
            normalize: Whether to normalize query
            
        Returns:
            Tuple of (distances, indices)
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")
        
        # Ensure query is 2D
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        if normalize:
            faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        return distances[0], indices[0]
    
    def save(self, index_path: str):
        """Save FAISS index to file"""
        if self.index is None:
            raise ValueError("No index to save")
        
        index_path = Path(index_path)
        index_path.parent.mkdir(parents=True, exist_ok=True)
        
        faiss.write_index(self.index, str(index_path))
        print(f"Index saved to {index_path}")
    
    def load(self, index_path: str):
        """Load FAISS index from file"""
        self.index = faiss.read_index(str(index_path))
        print(f"Index loaded from {index_path}")
        print(f"Index contains {self.index.ntotal} vectors")
    
    @property
    def size(self) -> int:
        """Get number of vectors in index"""
        return self.index.ntotal if self.index else 0


def build_faiss_index(
    embeddings_file: str = "embeddings/image_embeddings.npy",
    output_file: str = "embeddings/faiss_index.bin"
):
    """
    Build and save FAISS index from embeddings file
    
    Args:
        embeddings_file: Path to embeddings numpy file
        output_file: Path to save index
    """
    print(f"Loading embeddings from {embeddings_file}")
    embeddings = np.load(embeddings_file)
    
    print(f"Embeddings shape: {embeddings.shape}")
    
    # Build index
    faiss_index = FAISSIndex(embedding_dim=embeddings.shape[1])
    faiss_index.build_index(embeddings, normalize=True)
    
    # Save index
    faiss_index.save(output_file)
    
    return faiss_index


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build FAISS index")
    parser.add_argument("--embeddings_file", type=str, default="embeddings/image_embeddings.npy", help="Embeddings file")
    parser.add_argument("--output_file", type=str, default="embeddings/faiss_index.bin", help="Output index file")
    
    args = parser.parse_args()
    
    build_faiss_index(args.embeddings_file, args.output_file)
