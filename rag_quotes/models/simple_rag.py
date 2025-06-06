import os
import json
import requests
import math

# Configuration
OPENAI_API_KEY = "sk-svcacct-AlOr9iIw9iHN7b74ktBWT3BlbkFJcWnle5crbd0pvzMYQKBF"
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "o4-mini-2025-04-16"

class SimpleRAG:
    def __init__(self):
        self.embeddings_data = self.load_embeddings()
    
    def load_embeddings(self):
        """Load embeddings from JSON file"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        embeddings_path = os.path.join(current_dir, "embeddings.json")
        
        if not os.path.exists(embeddings_path):
            return None
        
        with open(embeddings_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_embedding(self, text):
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
    
    def cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def search_quotes(self, query, top_n=3):
        """Search for quotes similar to the query"""
        if not self.embeddings_data:
            return []
        
        # Get embedding for the query
        query_embedding = self.get_embedding(query)
        
        # Calculate similarities
        similarities = []
        for item in self.embeddings_data:
            similarity = self.cosine_similarity(query_embedding, item['embedding'])
            similarities.append({
                'id': item['id'],
                'quote': item['quote'],
                'similarity': similarity
            })
        
        # Sort by similarity and return top N
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_n]
    
    def generate_response(self, query, quotes):
        """Generate a response using OpenAI LLM"""
        if not quotes:
            return f"I couldn't find any quotes related to '{query}'. Please try a different topic."
        
        # Create prompt
        quotes_text = "\n\n".join([f"Quote {q['id']}: {q['quote']}" for q in quotes])
        
        prompt = f"""You are a helpful assistant that provides insights on quotes. 
A user is looking for quotes related to "{query}".

Here are the most relevant quotes I found:

{quotes_text}

Please provide a brief, insightful response that:
1. Introduces these quotes as being relevant to "{query}"
2. Briefly explains how each quote relates to the topic
3. Presents the quotes in a clear, readable format

Keep your response concise and meaningful."""
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that provides insights on quotes."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            # Fallback to simple format if API fails
            result = f"Here are the top quotes related to '{query}':\n\n"
            for i, quote in enumerate(quotes, 1):
                result += f"{i}. **Quote #{quote['id']}**: {quote['quote']}\n\n"
            return result
    
    def query(self, topic):
        """Main query function"""
        try:
            quotes = self.search_quotes(topic)
            response = self.generate_response(topic, quotes)
            return {
                "success": True,
                "response": response,
                "quotes": quotes
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing query: {str(e)}",
                "quotes": []
            }

# For testing
if __name__ == "__main__":
    rag = SimpleRAG()
    result = rag.query("business")
    print(result) 