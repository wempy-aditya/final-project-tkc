"""
Text Generator using LLM
Supports OpenAI GPT, Groq (Llama), and Google Gemini
Optimized for Gemini safety filters
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TextGenerator:
    def __init__(
        self,
        provider: str = None,
        model: str = None,
        api_key: str = None,
        temperature: float = 0.7,
        max_tokens: int = 200
    ):
        """
        Initialize text generator
        
        Args:
            provider: LLM provider ('openai', 'groq', or 'gemini')
            model: Model name
            api_key: API key (optional, will use env var)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        """
        self.provider = provider or os.getenv("LLM_PROVIDER", "gemini")
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if self.provider == "openai":
            from openai import OpenAI
            self.model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.client = OpenAI(api_key=api_key)
            
        elif self.provider == "groq":
            from groq import Groq
            self.model = model or os.getenv("LLM_MODEL", "llama3-70b-8192")
            api_key = api_key or os.getenv("GROQ_API_KEY")
            self.client = Groq(api_key=api_key)
            
        elif self.provider == "gemini":
            import google.generativeai as genai
            self.model = model or os.getenv("LLM_MODEL", "gemini-1.5-flash")
            api_key = api_key or os.getenv("GEMINI_API_KEY")
            genai.configure(api_key=api_key)
            
            # Configure safety settings to be less restrictive
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
            
            self.client = genai.GenerativeModel(
                self.model,
                safety_settings=safety_settings
            )
            
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
        print(f"Text generator initialized: {self.provider}/{self.model}")
    
    def generate(self, system_message: str, user_message: str) -> str:
        """
        Generate text using LLM
        
        Args:
            system_message: System prompt
            user_message: User message
            
        Returns:
            Generated text
        """
        try:
            if self.provider == "gemini":
                # Gemini uses a different API format
                # Combine system and user messages
                full_prompt = f"{system_message}\n\n{user_message}"
                
                response = self.client.generate_content(
                    full_prompt,
                    generation_config={
                        'temperature': self.temperature,
                        'max_output_tokens': self.max_tokens,
                    }
                )
                
                # Check if response was blocked
                if not response.candidates:
                    error_msg = "❌ No candidates returned by Gemini API"
                    print(error_msg)
                    return f"{error_msg}\n\n📝 Fallback:\n{self._create_fallback_description(user_message)}"
                
                candidate = response.candidates[0]
                
                # Check finish reason with detailed messages
                finish_reason = candidate.finish_reason
                
                if finish_reason == 2:
                    # Check safety ratings for more info
                    safety_info = ""
                    if hasattr(candidate, 'safety_ratings') and candidate.safety_ratings:
                        safety_info = "\n🛡️ Safety Ratings:\n"
                        for rating in candidate.safety_ratings:
                            safety_info += f"  - {rating.category}: {rating.probability}\n"
                    
                    error_msg = f"⚠️ Gemini blocked response (finish_reason: 2 - SAFETY/MAX_TOKENS){safety_info}"
                    print(error_msg)
                    return f"{error_msg}\n📝 Fallback:\n{self._create_fallback_description(user_message)}"
                
                if finish_reason == 3:
                    safety_info = ""
                    if hasattr(candidate, 'safety_ratings') and candidate.safety_ratings:
                        safety_info = "\n🛡️ Safety Ratings:\n"
                        for rating in candidate.safety_ratings:
                            safety_info += f"  - {rating.category}: {rating.probability}\n"
                    
                    error_msg = f"⚠️ Gemini blocked response (finish_reason: 3 - SAFETY){safety_info}"
                    print(error_msg)
                    return f"{error_msg}\n📝 Fallback:\n{self._create_fallback_description(user_message)}"
                
                if finish_reason == 4:
                    error_msg = "⚠️ Gemini blocked response (finish_reason: 4 - RECITATION)"
                    print(error_msg)
                    return f"{error_msg}\n📝 Fallback:\n{self._create_fallback_description(user_message)}"
                
                # Try to get text
                try:
                    return response.text
                except ValueError as e:
                    # If response.text fails, try to get from parts
                    if candidate.content and candidate.content.parts:
                        return candidate.content.parts[0].text
                    else:
                        # Use fallback
                        return self._create_fallback_description(user_message)
                
            else:
                # OpenAI and Groq use the same format
                messages = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ]
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                return response.choices[0].message.content
            
        except Exception as e:
            error_msg = f"Error generating text: {str(e)}"
            print(error_msg)
            # Return error details for debugging
            return f"⚠️ API Error: {str(e)}\n\n📝 Fallback Description:\n{self._create_fallback_description(user_message)}"
    
    def generate_from_context(self, context: dict) -> str:
        """
        Generate text from context dictionary
        
        Args:
            context: Dictionary with 'system' and 'user' keys
            
        Returns:
            Generated text
        """
        return self.generate(context['system'], context['user'])
    
    def _create_fallback_description(self, user_message: str) -> str:
        """
        Create a simple fallback description when Gemini blocks the response
        
        Args:
            user_message: The original user message containing captions
            
        Returns:
            Simple description based on captions
        """
        # Extract captions from user message
        lines = user_message.split('\n')
        captions = []
        for line in lines:
            line = line.strip()
            if line and any(c.isalpha() for c in line):
                # Remove numbering, bullet points, etc.
                caption = line.lstrip('0123456789.-) ')
                if caption and len(caption) > 10:  # Skip short lines
                    captions.append(caption)
        
        if not captions:
            return "The image shows a scene based on the provided context."
        
        # Create simple description from captions
        if len(captions) == 1:
            return f"The image shows {captions[0]}"
        elif len(captions) == 2:
            return f"The image shows {captions[0]} It also depicts {captions[1]}"
        else:
            # Combine first 3 captions
            desc = f"The image shows {captions[0]} "
            desc += f"Additionally, {captions[1]} "
            if len(captions) > 2:
                desc += f"The scene also includes {captions[2]}"
            return desc


if __name__ == "__main__":
    # Test text generator
    generator = TextGenerator()
    
    system = "You are a helpful assistant."
    user = "Describe a beautiful sunset."
    
    result = generator.generate(system, user)
    print("Generated text:")
    print(result)
