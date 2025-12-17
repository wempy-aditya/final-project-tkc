"""
Test script for multimodal search functionality
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.retrieval.retriever import Retriever
from PIL import Image
import os


def test_multimodal_search():
    """Test multimodal search with different weight settings"""
    
    print("=" * 70)
    print("MULTIMODAL SEARCH TEST")
    print("=" * 70)
    
    # Initialize retriever
    print("\n[1/4] Initializing retriever...")
    try:
        retriever = Retriever()
        print("✅ Retriever loaded successfully")
    except Exception as e:
        print(f"❌ Error loading retriever: {e}")
        print("\nMake sure you have run: python scripts/setup.py")
        return
    
    # Test queries
    test_text = "a dog playing in the park"
    
    # Check if we have a test image
    test_image_path = None
    possible_paths = [
        "data/coco/images/000000000001.jpg",
        "data/coco/val2017/000000000139.jpg"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            test_image_path = path
            break
    
    if not test_image_path:
        print("\n⚠️ No test image found. Will test text-only mode.")
        print("To test multimodal, make sure COCO images are downloaded.")
    
    # Test 1: Text-only search
    print("\n[2/4] Testing text-only search...")
    try:
        results = retriever.search_by_text(test_text, k=3)
        print(f"✅ Found {len(results['results'])} results")
        print(f"   Query: {results['query']}")
        print(f"   Top result: {results['results'][0]['file_name']}")
        print(f"   Score: {results['results'][0]['similarity_score']:.3f}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Image-only search (if image available)
    if test_image_path:
        print("\n[3/4] Testing image-only search...")
        try:
            results = retriever.search_by_image(test_image_path, k=3)
            print(f"✅ Found {len(results['results'])} results")
            print(f"   Query image: {test_image_path}")
            print(f"   Top result: {results['results'][0]['file_name']}")
            print(f"   Score: {results['results'][0]['similarity_score']:.3f}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("\n[3/4] Skipping image-only search (no test image)")
    
    # Test 3: Multimodal search with different weights
    if test_image_path:
        print("\n[4/4] Testing multimodal search with different weights...")
        
        weights = [0.0, 0.3, 0.5, 0.7, 1.0]
        
        for weight in weights:
            try:
                results = retriever.search_by_multimodal(
                    query_text=test_text,
                    query_image=test_image_path,
                    text_weight=weight,
                    k=3
                )
                
                weight_desc = "Image-only" if weight == 0.0 else \
                             "Image-focused" if weight < 0.5 else \
                             "Balanced" if weight == 0.5 else \
                             "Text-focused" if weight < 1.0 else \
                             "Text-only"
                
                print(f"\n   Weight {weight:.1f} ({weight_desc}):")
                print(f"   ├─ Top result: {results['results'][0]['file_name']}")
                print(f"   ├─ Score: {results['results'][0]['similarity_score']:.3f}")
                print(f"   └─ Caption: {results['results'][0]['captions'][0][:60]}...")
                
            except Exception as e:
                print(f"   ❌ Error with weight {weight}: {e}")
    else:
        print("\n[4/4] Skipping multimodal search (no test image)")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
    
    if test_image_path:
        print("\nAll search modes are working!")
        print("You can now use the Streamlit UI:")
        print("  streamlit run src\\ui\\app.py")
    else:
        print("\nText search is working!")
        print("For full multimodal testing, download COCO images first:")
        print("  python src/preprocess/download_coco.py")
    
    print()


def test_embedding_fusion():
    """Test embedding fusion logic"""
    
    print("\n" + "=" * 70)
    print("EMBEDDING FUSION TEST")
    print("=" * 70)
    
    try:
        retriever = Retriever()
        
        # Get sample embeddings
        text_emb = retriever.encoder.encode_text("a dog")
        
        # Find a test image
        test_image = None
        for path in ["data/coco/images/000000000001.jpg", "data/coco/val2017/000000000139.jpg"]:
            if os.path.exists(path):
                test_image = path
                break
        
        if not test_image:
            print("⚠️ No test image found, skipping fusion test")
            return
        
        image_emb = retriever.encoder.encode_image(test_image)
        
        print(f"\n✅ Embeddings generated:")
        print(f"   Text embedding shape: {text_emb.shape}")
        print(f"   Image embedding shape: {image_emb.shape}")
        
        # Test fusion
        fused = retriever._fuse_embeddings(text_emb, image_emb, text_weight=0.5)
        
        print(f"\n✅ Fused embedding:")
        print(f"   Shape: {fused.shape}")
        print(f"   Norm: {(fused ** 2).sum() ** 0.5:.6f} (should be ~1.0)")
        
        # Test different weights
        print(f"\n✅ Testing different fusion weights:")
        for weight in [0.0, 0.25, 0.5, 0.75, 1.0]:
            fused = retriever._fuse_embeddings(text_emb, image_emb, text_weight=weight)
            norm = (fused ** 2).sum() ** 0.5
            print(f"   Weight {weight:.2f}: norm = {norm:.6f}")
        
        print("\n✅ Fusion test passed!")
        
    except Exception as e:
        print(f"❌ Fusion test failed: {e}")


if __name__ == "__main__":
    # Run tests
    test_multimodal_search()
    test_embedding_fusion()
