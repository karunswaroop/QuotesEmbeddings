import os
import requests
from config import OPENAI_API_KEY

def test_embedding_api():
    """Test the OpenAI embeddings API"""
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": "This is a test"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Embedding API test successful!")
            print(f"Embedding dimensions: {len(result['data'][0]['embedding'])}")
            return True
        else:
            print(f"❌ Embedding API test failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing embedding API: {e}")
        return False

def test_chat_api():
    """Test the OpenAI chat completions API"""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."}
        ],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat API test successful!")
            print(f"Response: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ Chat API test failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing chat API: {e}")
        return False

if __name__ == "__main__":
    print("Testing OpenAI API connection...")
    print(f"API Key loaded: {'Yes' if OPENAI_API_KEY and len(OPENAI_API_KEY) > 20 else 'No'}")
    print("=" * 50)
    
    # Test both APIs
    embedding_success = test_embedding_api()
    print()
    chat_success = test_chat_api()
    
    print("\n" + "=" * 50)
    if embedding_success and chat_success:
        print("🎉 All API tests passed! Your system is ready to use.")
    else:
        print("⚠️ Some API tests failed. Please check your API key and internet connection.") 