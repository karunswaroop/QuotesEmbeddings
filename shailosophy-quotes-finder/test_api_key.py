#!/usr/bin/env python3
"""
Simple test script to verify OpenAI API key is working
Tests both embeddings and chat APIs
"""

import os
import sys
import argparse
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_embeddings_api(api_key):
    """Test OpenAI Embeddings API"""
    print("🔍 Testing Embeddings API...")
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": "This is a test quote for embedding generation."
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            dimensions = len(result["data"][0]["embedding"])
            print(f"✅ Embeddings API test successful!")
            print(f"   Embedding dimensions: {dimensions}")
            print(f"   API Key used: {api_key[:20]}...")
            return True
        else:
            print(f"❌ Embeddings API test failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Embeddings API test failed: {e}")
        return False

def test_chat_api(api_key):
    """Test OpenAI Chat API"""
    print("\n💬 Testing Chat API...")
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": "Say 'Hello! API key is working correctly.'"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print(f"✅ Chat API test successful!")
            print(f"   Response: {message}")
            print(f"   API Key used: {api_key[:20]}...")
            return True
        else:
            print(f"❌ Chat API test failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat API test failed: {e}")
        return False

def main():
    """Run all API tests"""
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Test OpenAI API key functionality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_api_key.py                                    # Use API key from .env file
  python test_api_key.py --api-key sk-...                  # Use provided API key
  python test_api_key.py -k sk-...                         # Short form
        """
    )
    
    parser.add_argument(
        "--api-key", "-k",
        type=str,
        help="OpenAI API key (if not provided, will use .env file)"
    )
    
    args = parser.parse_args()
    
    # Get API key from command line or .env file
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    
    print("🧪 Testing OpenAI API Key...")
    print("=" * 50)
    
    # Check if API key is available
    if api_key:
        source = "command line" if args.api_key else ".env file"
        print(f"📋 API Key loaded: Yes (from {source})")
        print(f"📋 API Key starts with: {api_key[:20]}...")
    else:
        print("📋 API Key loaded: No")
        print("   Please provide API key via --api-key or set it in .env file")
        print("\nUsage examples:")
        print("  python test_api_key.py --api-key sk-...")
        print("  python test_api_key.py  # (uses .env file)")
        return
    
    print("=" * 50)
    
    # Run tests
    embeddings_success = test_embeddings_api(api_key)
    chat_success = test_chat_api(api_key)
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Embeddings API: {'✅ PASS' if embeddings_success else '❌ FAIL'}")
    print(f"   Chat API: {'✅ PASS' if chat_success else '❌ FAIL'}")
    
    if embeddings_success and chat_success:
        print("\n🎉 All tests passed! Your API key is working correctly.")
        print("   You can now run: python generate_embeddings.py")
    else:
        print("\n⚠️ Some tests failed. Please check your API key and internet connection.")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 