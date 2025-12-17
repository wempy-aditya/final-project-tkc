"""
Debug script untuk test Gemini API connection
Menampilkan error detail untuk troubleshooting
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
load_dotenv()

def test_gemini_connection():
    """Test Gemini API connection dengan detail error"""
    
    print("=" * 70)
    print("GEMINI API CONNECTION TEST")
    print("=" * 70)
    
    # 1. Check API Key
    print("\n[1/5] Checking API Key...")
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file")
        print("\nSolusi:")
        print("1. Buka file .env")
        print("2. Tambahkan: GEMINI_API_KEY=your-key-here")
        print("3. Get key from: https://aistudio.google.com/app/apikey")
        return False
    
    if api_key == "your_gemini_api_key_here":
        print("❌ ERROR: GEMINI_API_KEY masih default value")
        print("\nSolusi:")
        print("1. Ganti dengan API key yang sebenarnya")
        print("2. Get key from: https://aistudio.google.com/app/apikey")
        return False
    
    print(f"✅ API Key found: {api_key[:15]}...{api_key[-5:]}")
    
    # 2. Check Model
    print("\n[2/5] Checking Model Configuration...")
    model = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    provider = os.getenv("LLM_PROVIDER", "gemini")
    
    print(f"✅ Provider: {provider}")
    print(f"✅ Model: {model}")
    
    # 3. Test Import
    print("\n[3/5] Testing google-generativeai import...")
    try:
        import google.generativeai as genai
        print("✅ google-generativeai imported successfully")
    except ImportError as e:
        print(f"❌ ERROR: Cannot import google-generativeai")
        print(f"   Error: {e}")
        print("\nSolusi:")
        print("   pip install google-generativeai")
        return False
    
    # 4. Configure API
    print("\n[4/5] Configuring Gemini API...")
    try:
        genai.configure(api_key=api_key)
        print("✅ API configured successfully")
    except Exception as e:
        print(f"❌ ERROR: Failed to configure API")
        print(f"   Error: {e}")
        return False
    
    # 5. Test Simple Generation
    print("\n[5/5] Testing text generation...")
    try:
        # Create model with safety settings
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
        
        model_instance = genai.GenerativeModel(
            model,
            safety_settings=safety_settings
        )
        
        print(f"   Testing with model: {model}")
        print("   Generating response...")
        
        # Simple test prompt
        test_prompt = "Describe a sunset in one sentence."
        
        response = model_instance.generate_content(
            test_prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 100,
            }
        )
        
        # Check response
        if not response.candidates:
            print("❌ ERROR: No candidates returned")
            print("   Kemungkinan: API key invalid atau quota habis")
            return False
        
        candidate = response.candidates[0]
        finish_reason = candidate.finish_reason
        
        print(f"   Finish reason: {finish_reason}")
        
        if finish_reason == 1:  # STOP (success)
            print("✅ Generation successful!")
            print(f"\n   Response: {response.text}")
            return True
        elif finish_reason == 2:
            print("⚠️  Blocked by safety filter (finish_reason: 2)")
            if hasattr(candidate, 'safety_ratings'):
                print("\n   Safety Ratings:")
                for rating in candidate.safety_ratings:
                    print(f"     - {rating.category}: {rating.probability}")
            return False
        elif finish_reason == 3:
            print("⚠️  Blocked by safety filter (finish_reason: 3)")
            return False
        else:
            print(f"⚠️  Unexpected finish_reason: {finish_reason}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR during generation:")
        print(f"   {type(e).__name__}: {str(e)}")
        
        # Specific error handling
        if "429" in str(e):
            print("\n   💡 Solusi: Rate limit exceeded")
            print("      - Tunggu beberapa menit")
            print("      - Atau ganti model ke gemini-1.5-flash")
        elif "403" in str(e) or "API key" in str(e):
            print("\n   💡 Solusi: API key invalid")
            print("      - Cek API key di .env")
            print("      - Regenerate key di: https://aistudio.google.com/app/apikey")
        elif "404" in str(e):
            print("\n   💡 Solusi: Model not found")
            print(f"      - Model '{model}' mungkin tidak tersedia")
            print("      - Coba ganti ke: gemini-1.5-flash")
        
        return False


def main():
    success = test_gemini_connection()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ SEMUA TEST BERHASIL!")
        print("=" * 70)
        print("\nGemini API siap digunakan!")
        print("Jalankan aplikasi: streamlit run src\\ui\\app.py")
    else:
        print("❌ TEST GAGAL")
        print("=" * 70)
        print("\nSilakan perbaiki error di atas sebelum menjalankan aplikasi.")
    print()


if __name__ == "__main__":
    main()
