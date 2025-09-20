#!/usr/bin/env python3
"""
Simple test script to verify the quotes app setup
"""

import os
import sys
from quotes import QuotesGenerator
import config

def test_quotes_generator():
    """Test the quotes generator functionality"""
    print("Testing Quotes Generator...")
    
    # Check if API key is set
    if not config.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found")
        print("   Please set it as an environment variable:")
        print("     export GEMINI_API_KEY='your_key_here'")
        print("   Or create a .env file with:")
        print("     GEMINI_API_KEY=your_key_here")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")
        return False
    
    print("✅ GEMINI_API_KEY is configured")
    
    try:
        # Test quotes generator
        generator = QuotesGenerator(config.GEMINI_API_KEY)
        print("✅ QuotesGenerator initialized successfully")
        
        # Test quote generation
        quotes = generator.generate_quotes("success")
        print(f"✅ Generated {len(quotes)} quotes")
        
        # Validate quote structure
        for i, quote in enumerate(quotes):
            if 'quote' not in quote or 'context' not in quote:
                print(f"❌ Quote {i+1} has invalid structure")
                return False
        
        print("✅ All quotes have valid structure")
        
        # Display sample quote
        if quotes:
            print(f"\n📝 Sample quote:")
            print(f"   Quote: \"{quotes[0]['quote']}\"")
            print(f"   Context: {quotes[0]['context']}")
        
        return True
        
    except ValueError as e:
        # This is expected if API key is not set
        print(f"❌ {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing quotes generator: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"❌ Google Generative AI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Quotes Reading App Setup\n")
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    print()
    
    # Test quotes generator
    if not test_quotes_generator():
        print("\n❌ Quotes generator tests failed")
        sys.exit(1)
    
    print("\n🎉 All tests passed! The app is ready to run.")
    print("\nTo start the server, run:")
    print("   python app.py")
    print("\nThen open your browser to: http://localhost:8000")

if __name__ == "__main__":
    main()