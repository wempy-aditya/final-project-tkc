"""
CLIP Encoder Module
Handles encoding of text and images using OpenAI CLIP model
"""

import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import numpy as np
from typing import Union, List
import os


class CLIPEncoder:
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32", device: str = None):
        """
        Initialize CLIP encoder
        
        Args:
            model_name: HuggingFace model identifier
            device: Device to run model on (cuda/cpu)
        """
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        print(f"Loading CLIP model: {model_name}")
        print(f"Using device: {self.device}")
        
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model.eval()
        
    def encode_text(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Encode text(s) to embeddings
        
        Args:
            texts: Single text string or list of texts
            
        Returns:
            Numpy array of embeddings (normalized)
        """
        if isinstance(texts, str):
            texts = [texts]
            
        with torch.no_grad():
            inputs = self.processor(text=texts, return_tensors="pt", padding=True, truncation=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            text_features = self.model.get_text_features(**inputs)
            
            # Normalize embeddings
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
        return text_features.cpu().numpy()
    
    def encode_image(self, images: Union[str, Image.Image, List[Union[str, Image.Image]]]) -> np.ndarray:
        """
        Encode image(s) to embeddings
        
        Args:
            images: Single image path/PIL Image or list of images
            
        Returns:
            Numpy array of embeddings (normalized)
        """
        if not isinstance(images, list):
            images = [images]
            
        # Load images if paths are provided
        pil_images = []
        for img in images:
            if isinstance(img, str):
                pil_images.append(Image.open(img).convert("RGB"))
            else:
                pil_images.append(img)
        
        with torch.no_grad():
            inputs = self.processor(images=pil_images, return_tensors="pt", padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            image_features = self.model.get_image_features(**inputs)
            
            # Normalize embeddings
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            
        return image_features.cpu().numpy()
    
    def encode_images_batch(self, image_paths: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Encode multiple images in batches
        
        Args:
            image_paths: List of image file paths
            batch_size: Number of images to process at once
            
        Returns:
            Numpy array of all embeddings
        """
        all_embeddings = []
        
        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i:i + batch_size]
            embeddings = self.encode_image(batch_paths)
            all_embeddings.append(embeddings)
            
        return np.vstack(all_embeddings)
    
    @property
    def embedding_dim(self) -> int:
        """Get embedding dimension"""
        return self.model.config.projection_dim
