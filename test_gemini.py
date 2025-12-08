"""
Test script untuk Gemini API
"""

import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from src.models.text_generator import TextGenerator

# Load environment variables
load_dotenv()

def test_gemini():
    """Test Gemini API"""
    print("=" * 60)
    print("Testing Gemini API")
    print("=" * 60)
    
    # Check if API key exists
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("\n❌ ERROR: GEMINI_API_KEY not found in .env file")
        print("\nPlease:")
        print("1. Get API key from: https://aistudio.google.com/app/apikey")
        print("2. Add to .env file: GEMINI_API_KEY=your-key-here")
        return
    
    print(f"\n✅ API Key found: {api_key[:10]}...")
    
    # Initialize generator
    try:
        print("\nInitializing Gemini text generator...")
        generator = TextGenerator(provider="gemini")
        print("✅ Generator initialized successfully!")
    except Exception as e:
        print(f"\n❌ Error initializing generator: {e}")
        print("\nMake sure you have installed: pip install google-generativeai")
        return
    
    # Test generation
    print("\n" + "=" * 60)
    print("Testing Text Generation")
    print("=" * 60)
    
    system = "You are a helpful assistant that describes images."
    user = "Describe a beautiful sunset over the ocean in 2-3 sentences."
    
    print(f"\nSystem: {system}")
    print(f"User: {user}")
    print("\nGenerating response...")
    
    try:
        result = generator.generate(system, user)
        print("\n✅ Generated text:")
        print("-" * 60)
        print(result)
        print("-" * 60)
        print("\n🎉 Gemini API is working perfectly!")
        
    except Exception as e:
        print(f"\n❌ Error generating text: {e}")
        print("\nPossible issues:")
        print("- Invalid API key")
        print("- Rate limit exceeded")
        print("- Network connection")
        return
    
    # Test with RAG context
    print("\n" + "=" * 60)
    print("Testing RAG Context")
    print("=" * 60)
    
    from src.models.context_builder import ContextBuilder
    
    builder = ContextBuilder()
    query = "a dog playing in the park"
    captions = [
        "a brown dog playing with a ball",
        "a happy dog running in the grass",
        "a playful puppy outdoors"
    ]
    
    context = builder.build_context(query, captions)
    
    print(f"\nQuery: {query}")
    print(f"Retrieved captions: {len(captions)}")
    print("\nGenerating description...")
    
    try:
        description = generator.generate_from_context(context)
        print("\n✅ Generated description:")
        print("-" * 60)
        print(description)
        print("-" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nYou can now run the full application:")
    print("  streamlit run src/ui/app.py")


if __name__ == "__main__":
    test_gemini()
