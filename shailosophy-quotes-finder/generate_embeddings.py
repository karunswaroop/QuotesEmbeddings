"""
Generate embeddings for Shailosophy quotes using OpenAI API
This script processes the quotes CSV file and creates embeddings for semantic search.
"""

import os
import csv
import json
import requests
from config import OPENAI_API_KEY, EMBEDDING_MODEL, QUOTES_FILE, EMBEDDINGS_FILE

def load_quotes():
    """Load quotes from CSV file"""
    quotes = []
    
    if not os.path.exists(QUOTES_FILE):
        raise FileNotFoundError(f"Quotes file not found: {QUOTES_FILE}")
    
    with open(QUOTES_FILE, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            if len(row) >= 2 and row[1].strip():  # Ensure we have at least ID and non-empty quote
                quotes.append({
                    "id": row[0],
                    "quote": row[1].strip()
                })
    
    return quotes

def get_embedding(text):
    """Get embedding for a text using OpenAI API"""
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": EMBEDDING_MODEL,
        "input": text
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["data"][0]["embedding"]
    else:
        raise Exception(f"Error getting embedding: {response.text}")

def create_embeddings():
    """Create embeddings for all quotes and save to JSON file"""
    print("🔄 Starting embeddings generation...")
    
    # Check API key
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-api-key-here":
        raise ValueError("❌ Please set your OpenAI API key in the .env file")
    
    # Load quotes
    quotes = load_quotes()
    print(f"📚 Loaded {len(quotes)} quotes from {QUOTES_FILE}")
    
    embeddings_data = []
    
    print(f"🔄 Processing {len(quotes)} quotes...")
    
    for i, quote in enumerate(quotes):
        try:
            print(f"Processing quote {i+1}/{len(quotes)}: {quote['id']}")
            embedding = get_embedding(quote['quote'])
            
            embeddings_data.append({
                "id": quote['id'],
                "quote": quote['quote'],
                "embedding": embedding
            })
            
        except Exception as e:
            print(f"❌ Error processing quote {quote['id']}: {e}")
            continue
    
    # Save embeddings to JSON file
    with open(EMBEDDINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(embeddings_data, f, indent=2)
    
    print(f"✅ Embeddings saved to {EMBEDDINGS_FILE}")
    print(f"✅ Created embeddings for {len(embeddings_data)} quotes")
    
    return len(embeddings_data)

if __name__ == "__main__":
    try:
        count = create_embeddings()
        print(f"\n🎉 Successfully generated embeddings for {count} quotes!")
        print("Now you can run the Streamlit app: streamlit run app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check:")
        print("1. Your .env file contains a valid OPENAI_API_KEY")
        print("2. The data/ShailosophyQuotes.csv file exists")
        print("3. You have internet connection") 