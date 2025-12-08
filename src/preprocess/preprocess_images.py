"""
Image Preprocessing Module
Handles image resizing and preprocessing for CLIP
"""

import os
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from typing import List, Tuple


def preprocess_image(image_path: str, output_path: str, size: Tuple[int, int] = (224, 224)):
    """
    Preprocess a single image
    
    Args:
        image_path: Path to input image
        output_path: Path to save processed image
        size: Target size (width, height)
    """
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(output_path, quality=95)
        return True
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False


def preprocess_images(
    input_dir: str = "data/coco/images",
    output_dir: str = "data/processed",
    size: Tuple[int, int] = (224, 224)
):
    """
    Preprocess all images in directory
    
    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save processed images
        size: Target size for images
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    image_files = [
        f for f in input_dir.iterdir()
        if f.suffix.lower() in image_extensions
    ]
    
    print(f"Found {len(image_files)} images to process")
    
    successful = 0
    for img_file in tqdm(image_files, desc="Processing images"):
        output_path = output_dir / img_file.name
        
        if not output_path.exists():
            if preprocess_image(str(img_file), str(output_path), size):
                successful += 1
        else:
            successful += 1
    
    print(f"\nProcessed {successful}/{len(image_files)} images successfully")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Preprocess images")
    parser.add_argument("--input_dir", type=str, default="data/coco/images", help="Input directory")
    parser.add_argument("--output_dir", type=str, default="data/processed", help="Output directory")
    parser.add_argument("--size", type=int, default=224, help="Image size")
    
    args = parser.parse_args()
    
    preprocess_images(args.input_dir, args.output_dir, (args.size, args.size))
