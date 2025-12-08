"""
Generate CLIP Embeddings for COCO Images
"""

import os
import json
import numpy as np
from pathlib import Path
from tqdm import tqdm
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.clip_encoder import CLIPEncoder


def generate_embeddings(
    images_dir: str = "data/coco/images",
    captions_file: str = "data/coco/captions.json",
    output_dir: str = "embeddings",
    batch_size: int = 32
):
    """
    Generate CLIP embeddings for all images
    
    Args:
        images_dir: Directory containing images
        captions_file: JSON file with captions
        output_dir: Directory to save embeddings
        batch_size: Batch size for processing
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load captions
    print("Loading captions...")
    with open(captions_file, 'r') as f:
        captions_data = json.load(f)
    
    # Get image paths
    images_dir = Path(images_dir)
    image_paths = []
    metadata = []
    
    for file_name, data in captions_data.items():
        img_path = images_dir / file_name
        if img_path.exists():
            image_paths.append(str(img_path))
            metadata.append({
                'file_name': file_name,
                'image_id': data['image_id'],
                'captions': data['captions'],
                'path': str(img_path)
            })
    
    print(f"Found {len(image_paths)} images")
    
    # Initialize CLIP encoder
    print("Initializing CLIP encoder...")
    encoder = CLIPEncoder()
    
    # Generate embeddings in batches
    print("Generating embeddings...")
    all_embeddings = []
    
    for i in tqdm(range(0, len(image_paths), batch_size)):
        batch_paths = image_paths[i:i + batch_size]
        
        try:
            embeddings = encoder.encode_image(batch_paths)
            all_embeddings.append(embeddings)
        except Exception as e:
            print(f"\nError processing batch {i}: {e}")
            continue
    
    # Concatenate all embeddings
    all_embeddings = np.vstack(all_embeddings)
    
    # Save embeddings
    embeddings_file = output_dir / "image_embeddings.npy"
    print(f"\nSaving embeddings to {embeddings_file}")
    np.save(embeddings_file, all_embeddings)
    
    # Save metadata
    meta_file = output_dir / "meta.json"
    print(f"Saving metadata to {meta_file}")
    with open(meta_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\nEmbeddings generated successfully!")
    print(f"Shape: {all_embeddings.shape}")
    print(f"Embedding dimension: {all_embeddings.shape[1]}")
    print(f"Number of images: {all_embeddings.shape[0]}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate CLIP embeddings")
    parser.add_argument("--images_dir", type=str, default="data/coco/images", help="Images directory")
    parser.add_argument("--captions_file", type=str, default="data/coco/captions.json", help="Captions file")
    parser.add_argument("--output_dir", type=str, default="embeddings", help="Output directory")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    
    args = parser.parse_args()
    
    generate_embeddings(
        args.images_dir,
        args.captions_file,
        args.output_dir,
        args.batch_size
    )
