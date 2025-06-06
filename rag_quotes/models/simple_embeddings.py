import os
import csv
import json
import requests

# Configuration
OPENAI_API_KEY = "sk-svcacct-AlOr9iIw9iHN7b74ktBWT3BlbkFJcWnle5crbd0pvzMYQKBF"
EMBEDDING_MODEL = "text-embedding-3-small"

def load_quotes():
    """Load quotes from CSV file"""
    quotes = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    csv_path = os.path.join(parent_dir, "data", "ShailosophyQuotes.csv")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            quotes.append({
                "id": row[0],
                "quote": row[1]
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
    """Create embeddings for all quotes"""
    quotes = load_quotes()
    embeddings_data = []
    
    print(f"Processing {len(quotes)} quotes...")
    
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
            print(f"Error processing quote {quote['id']}: {e}")
            continue
    
    # Save embeddings to JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    embeddings_path = os.path.join(current_dir, "embeddings.json")
    
    with open(embeddings_path, 'w', encoding='utf-8') as f:
        json.dump(embeddings_data, f, indent=2)
    
    print(f"Embeddings saved to {embeddings_path}")
    print(f"Created embeddings for {len(embeddings_data)} quotes")

if __name__ == "__main__":
    create_embeddings() 