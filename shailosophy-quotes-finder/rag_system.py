"""
RAG (Retrieval-Augmented Generation) System for Shailosophy Quotes
Handles semantic search and AI response generation for quotes.
"""

import os
import json
import requests
import math
from config import OPENAI_API_KEY, EMBEDDING_MODEL, LLM_MODEL, EMBEDDINGS_FILE, TOP_N_RESULTS

class ShailosophyRAG:
    """RAG system for finding and generating responses about Shailosophy quotes"""
    
    def __init__(self):
        self.embeddings_data = self._load_embeddings()
    
    def _load_embeddings(self):
        """Load embeddings from JSON file"""
        if not os.path.exists(EMBEDDINGS_FILE):
            return None
        
        try:
            with open(EMBEDDINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            return None
    
    def is_ready(self):
        """Check if the RAG system is ready to use"""
        return self.embeddings_data is not None and len(self.embeddings_data) > 0
    
    def get_quotes_count(self):
        """Get the number of quotes loaded"""
        return len(self.embeddings_data) if self.embeddings_data else 0
    
    def _get_embedding(self, text):
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
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def find_similar_quotes(self, query, top_n=None):
        """Search for quotes similar to the query"""
        if not self.is_ready():
            return []
        
        if top_n is None:
            top_n = TOP_N_RESULTS
        
        # Get embedding for the query
        query_embedding = self._get_embedding(query)
        
        # Calculate similarities
        similarities = []
        for item in self.embeddings_data:
            similarity = self._cosine_similarity(query_embedding, item['embedding'])
            similarities.append({
                'id': item['id'],
                'quote': item['quote'],
                'similarity': similarity
            })
        
        # Sort by similarity and return top N
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_n]
    
    def _generate_response(self, query, quotes):
        """Generate a response using OpenAI LLM"""
        if not quotes:
            return f"I couldn't find any quotes related to '{query}'. Please try a different topic."
        
        # Create prompt
        quotes_text = "\n\n".join([f"Quote {q['id']}: {q['quote']}" for q in quotes])
        
        prompt = f"""You are a helpful assistant that provides insights on Shailosophy quotes. 
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
    
    def search(self, topic, include_response=True):
        """Main search function that returns quotes and optional AI response"""
        try:
            quotes = self.find_similar_quotes(topic)
            
            result = {
                "success": True,
                "quotes": quotes,
                "topic": topic
            }
            
            if include_response:
                result["response"] = self._generate_response(topic, quotes)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing query: {str(e)}",
                "quotes": []
            }

# For testing
if __name__ == "__main__":
    rag = ShailosophyRAG()
    if rag.is_ready():
        result = rag.search("business")
        print(f"Found {len(result['quotes'])} quotes")
        for quote in result['quotes']:
            print(f"- {quote['quote'][:100]}... (similarity: {quote['similarity']:.3f})")
    else:
        print("RAG system not ready. Please generate embeddings first.") 