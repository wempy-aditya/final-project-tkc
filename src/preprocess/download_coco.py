"""
COCO Dataset Download Script
Downloads COCO 2017 validation dataset and extracts captions
"""

import os
import json
import requests
from pathlib import Path
from tqdm import tqdm
import zipfile
from pycocotools.coco import COCO
import shutil


def download_file(url: str, dest_path: str):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(dest_path, 'wb') as f, tqdm(
        desc=dest_path,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)


def download_coco_dataset(data_dir: str = "data/coco", subset_size: int = 10000):
    """
    Download COCO 2017 validation dataset
    
    Args:
        data_dir: Directory to save data
        subset_size: Number of images to download (max)
    """
    data_dir = Path(data_dir)
    images_dir = data_dir / "images"
    annotations_dir = data_dir / "annotations"
    
    images_dir.mkdir(parents=True, exist_ok=True)
    annotations_dir.mkdir(parents=True, exist_ok=True)
    
    # URLs for COCO 2017 validation set
    annotations_url = "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"
    images_url = "http://images.cocodataset.org/zips/val2017.zip"
    
    # Download annotations
    annotations_zip = annotations_dir / "annotations.zip"
    if not annotations_zip.exists():
        print("Downloading COCO annotations...")
        download_file(annotations_url, str(annotations_zip))
        
        print("Extracting annotations...")
        with zipfile.ZipFile(annotations_zip, 'r') as zip_ref:
            zip_ref.extractall(annotations_dir)
    
    # Download images
    images_zip = data_dir / "val2017.zip"
    if not (data_dir / "val2017").exists():
        print("Downloading COCO images...")
        download_file(images_url, str(images_zip))
        
        print("Extracting images...")
        with zipfile.ZipFile(images_zip, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
    
    # Load annotations
    ann_file = annotations_dir / "annotations" / "captions_val2017.json"
    coco = COCO(str(ann_file))
    
    # Get image IDs (limit to subset_size)
    img_ids = coco.getImgIds()[:subset_size]
    
    # Extract captions
    captions_data = {}
    
    print(f"Processing {len(img_ids)} images...")
    for img_id in tqdm(img_ids):
        img_info = coco.loadImgs(img_id)[0]
        ann_ids = coco.getAnnIds(imgIds=img_id)
        anns = coco.loadAnns(ann_ids)
        
        # Get all captions for this image
        captions = [ann['caption'] for ann in anns]
        
        # Copy image to images directory
        src_path = data_dir / "val2017" / img_info['file_name']
        dst_path = images_dir / img_info['file_name']
        
        if src_path.exists() and not dst_path.exists():
            shutil.copy(src_path, dst_path)
        
        captions_data[img_info['file_name']] = {
            'image_id': img_id,
            'file_name': img_info['file_name'],
            'captions': captions,
            'width': img_info['width'],
            'height': img_info['height']
        }
    
    # Save captions to JSON
    captions_file = data_dir / "captions.json"
    with open(captions_file, 'w') as f:
        json.dump(captions_data, f, indent=2)
    
    print(f"\nDataset downloaded successfully!")
    print(f"Images: {images_dir}")
    print(f"Captions: {captions_file}")
    print(f"Total images: {len(captions_data)}")
    
    return captions_data


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Download COCO dataset")
    parser.add_argument("--data_dir", type=str, default="data/coco", help="Data directory")
    parser.add_argument("--subset_size", type=int, default=10000, help="Number of images")
    
    args = parser.parse_args()
    
    download_coco_dataset(args.data_dir, args.subset_size)
