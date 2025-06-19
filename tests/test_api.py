"""
API Connection Tests for Shailosophy Quotes Finder
Test OpenAI API connectivity and functionality.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OPENAI_API_KEY, EMBEDDING_MODEL, LLM_MODEL
import requests
import json

def test_embedding_api():
    """Test OpenAI Embeddings API"""
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": EMBEDDING_MODEL,
        "input": "test quote for embedding"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            dimensions = len(result["data"][0]["embedding"])
            print("✅ Embedding API test successful!")
            print(f"Embedding dimensions: {dimensions}")
            return True
        else:
            print("❌ Embedding API test failed:", response.json())
            return False
    except Exception as e:
        print(f"❌ Embedding API test failed: {e}")
        return False

def test_chat_api():
    """Test OpenAI Chat API"""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": "Say hello!"}],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print("✅ Chat API test successful!")
            print(f"Response: {message}")
            return True
        else:
            print("❌ Chat API test failed:", response.json())
            return False
    except Exception as e:
        print(f"❌ Chat API test failed: {e}")
        return False

def main():
    """Run all API tests"""
    print("Testing OpenAI API connection...")
    print(f"API Key loaded: {'Yes' if OPENAI_API_KEY and len(OPENAI_API_KEY) > 20 else 'No'}")
    print("=" * 50)
    
    embedding_success = test_embedding_api()
    print()
    chat_success = test_chat_api()
    
    print()
    print("=" * 50)
    if embedding_success and chat_success:
        print("🎉 All API tests passed! Your system is ready to use.")
    else:
        print("⚠️ Some API tests failed. Please check your API key and internet connection.")

if __name__ == "__main__":
    main() 