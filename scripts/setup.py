"""
Setup Script
Automates the entire setup process: download data, generate embeddings, build index
"""

import sys
from pathlib import Path
import argparse

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.preprocess.download_coco import download_coco_dataset
from src.preprocess.preprocess_images import preprocess_images
from src.preprocess.generate_embeddings import generate_embeddings
from src.retrieval.faiss_index import build_faiss_index


def setup_all(
    data_dir: str = "data/coco",
    subset_size: int = 10000,
    skip_download: bool = False,
    skip_preprocess: bool = False
):
    """
    Run complete setup pipeline
    
    Args:
        data_dir: Data directory
        subset_size: Number of images to use
        skip_download: Skip dataset download
        skip_preprocess: Skip image preprocessing
    """
    print("=" * 60)
    print("MULTIMODAL RAG SYSTEM - SETUP")
    print("=" * 60)
    
    # Step 1: Download COCO dataset
    if not skip_download:
        print("\n[1/4] Downloading COCO dataset...")
        try:
            download_coco_dataset(data_dir, subset_size)
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            print("You can skip this step with --skip-download if data already exists")
            return
    else:
        print("\n[1/4] Skipping dataset download")
    
    # Step 2: Preprocess images
    if not skip_preprocess:
        print("\n[2/4] Preprocessing images...")
        try:
            preprocess_images(
                input_dir=f"{data_dir}/images",
                output_dir="data/processed"
            )
        except Exception as e:
            print(f"Error preprocessing images: {e}")
            print("You can skip this step with --skip-preprocess")
    else:
        print("\n[2/4] Skipping image preprocessing")
    
    # Step 3: Generate embeddings
    print("\n[3/4] Generating CLIP embeddings...")
    try:
        generate_embeddings(
            images_dir=f"{data_dir}/images",
            captions_file=f"{data_dir}/captions.json",
            output_dir="embeddings",
            batch_size=32
        )
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return
    
    # Step 4: Build FAISS index
    print("\n[4/4] Building FAISS index...")
    try:
        build_faiss_index(
            embeddings_file="embeddings/image_embeddings.npy",
            output_file="embeddings/faiss_index.bin"
        )
    except Exception as e:
        print(f"Error building FAISS index: {e}")
        return
    
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print("\nYou can now run the Streamlit app:")
    print("  streamlit run src/ui/app.py")
    print("\nOr test the retrieval system:")
    print("  python src/retrieval/retriever.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup Multimodal RAG System")
    parser.add_argument("--data_dir", type=str, default="data/coco", help="Data directory")
    parser.add_argument("--subset_size", type=int, default=10000, help="Number of images")
    parser.add_argument("--skip-download", action="store_true", help="Skip dataset download")
    parser.add_argument("--skip-preprocess", action="store_true", help="Skip image preprocessing")
    
    args = parser.parse_args()
    
    setup_all(
        args.data_dir,
        args.subset_size,
        args.skip_download,
        args.skip_preprocess
    )
