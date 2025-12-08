"""
Image Generator using Stable Diffusion
Supports local generation and API endpoints
"""

import os
import requests
from PIL import Image
from io import BytesIO
from typing import Optional, Union
from dotenv import load_dotenv

load_dotenv()


class ImageGenerator:
    def __init__(
        self,
        use_local: bool = False,
        api_url: str = None,
        model: str = None
    ):
        """
        Initialize image generator
        
        Args:
            use_local: Whether to use local Stable Diffusion
            api_url: API endpoint URL (for Colab or external API)
            model: Model name/path
        """
        self.use_local = use_local
        self.api_url = api_url or os.getenv("SD_API_URL")
        self.model = model or os.getenv("SD_MODEL", "stabilityai/stable-diffusion-2-1")
        
        if use_local:
            self._init_local_model()
        
        print(f"Image generator initialized (local={use_local})")
    
    def _init_local_model(self):
        """Initialize local Stable Diffusion model"""
        try:
            from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
            import torch
            
            print(f"Loading Stable Diffusion model: {self.model}")
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            
            # Use DPM solver for faster generation
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # Move to GPU if available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.pipe = self.pipe.to(device)
            
            print(f"Model loaded on {device}")
            
        except Exception as e:
            print(f"Error loading local model: {e}")
            self.use_local = False
    
    def txt2img(
        self,
        prompt: str,
        negative_prompt: str = "blurry, bad quality, distorted",
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        height: int = 512,
        width: int = 512
    ) -> Optional[Image.Image]:
        """
        Generate image from text prompt
        
        Args:
            prompt: Text prompt
            negative_prompt: Negative prompt
            num_inference_steps: Number of denoising steps
            guidance_scale: Guidance scale
            height: Image height
            width: Image width
            
        Returns:
            PIL Image or None
        """
        if self.use_local:
            return self._generate_local(
                prompt, negative_prompt, num_inference_steps,
                guidance_scale, height, width
            )
        elif self.api_url:
            return self._generate_api(
                prompt, negative_prompt, num_inference_steps,
                guidance_scale, height, width
            )
        else:
            print("No generation method available. Set use_local=True or provide api_url")
            return None
    
    def _generate_local(
        self,
        prompt: str,
        negative_prompt: str,
        num_inference_steps: int,
        guidance_scale: float,
        height: int,
        width: int
    ) -> Optional[Image.Image]:
        """Generate image using local model"""
        try:
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                height=height,
                width=width
            ).images[0]
            
            return image
            
        except Exception as e:
            print(f"Error generating image locally: {e}")
            return None
    
    def _generate_api(
        self,
        prompt: str,
        negative_prompt: str,
        num_inference_steps: int,
        guidance_scale: float,
        height: int,
        width: int
    ) -> Optional[Image.Image]:
        """Generate image using API endpoint"""
        try:
            payload = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "height": height,
                "width": width
            }
            
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                return image
            else:
                print(f"API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error generating image via API: {e}")
            return None
    
    def img2img(
        self,
        image: Union[str, Image.Image],
        prompt: str,
        strength: float = 0.75,
        **kwargs
    ) -> Optional[Image.Image]:
        """
        Generate image from image + prompt
        
        Args:
            image: Input image (path or PIL Image)
            prompt: Text prompt
            strength: Transformation strength
            **kwargs: Additional arguments for txt2img
            
        Returns:
            PIL Image or None
        """
        # Load image if path
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        
        if self.use_local:
            try:
                from diffusers import StableDiffusionImg2ImgPipeline
                import torch
                
                # Create img2img pipeline
                pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                    self.model,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
                device = "cuda" if torch.cuda.is_available() else "cpu"
                pipe = pipe.to(device)
                
                result = pipe(
                    prompt=prompt,
                    image=image,
                    strength=strength,
                    **kwargs
                ).images[0]
                
                return result
                
            except Exception as e:
                print(f"Error in img2img: {e}")
                return None
        else:
            print("img2img only supported with local model")
            return None


if __name__ == "__main__":
    # Test image generator
    generator = ImageGenerator(use_local=False)
    
    prompt = "a beautiful sunset over the ocean, vibrant colors, photorealistic"
    print(f"Generating image with prompt: {prompt}")
    
    # This will only work if you have local SD or API configured
    # image = generator.txt2img(prompt)
    # if image:
    #     image.save("test_output.png")
    #     print("Image saved to test_output.png")
