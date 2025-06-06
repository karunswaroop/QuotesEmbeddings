import os
import sys
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import json

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, EMBEDDING_MODEL, LLM_MODEL, CHROMA_PERSIST_DIRECTORY, TOP_N_RESULTS

# Configure OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

class QuotesRAG:
    def __init__(self):
        """Initialize the RAG system"""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)
        
        # Create embedding function
        self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY,
            model_name=EMBEDDING_MODEL
        )
        
        # Connect to collection
        try:
            self.collection = self.chroma_client.get_collection(
                name="shailosophy_quotes",
                embedding_function=self.openai_ef
            )
            print("Connected to existing collection")
        except Exception as e:
            print(f"Error connecting to collection: {e}")
            print("Please run embeddings.py first to create the collection")
            self.collection = None
    
    def retrieve_quotes(self, topic):
        """Search for quotes related to the given topic"""
        if self.collection is None:
            return {"error": "Collection not available"}
        
        # Query the collection
        results = self.collection.query(
            query_texts=[topic],
            n_results=TOP_N_RESULTS
        )
        
        # Format results
        quotes = []
        if results and 'documents' in results and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                quote_id = results['ids'][0][i]
                quotes.append({
                    "id": quote_id,
                    "quote": doc
                })
        
        return quotes
    
    def generate_response(self, topic, quotes):
        """Generate a response using the OpenAI API"""
        if not quotes:
            return f"I couldn't find any quotes related to '{topic}'. Please try a different topic."
        
        # Create a prompt for the OpenAI API
        prompt = f"""I'm looking for Shailosophy quotes related to "{topic}". 
Here are some quotes that might be relevant:

{json.dumps([q['quote'] for q in quotes], indent=2)}

Please provide these quotes in a formatted way, with brief insights on how they relate to the topic of "{topic}".
"""
        
        try:
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides insights on quotes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Return the response content
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {e}"
    
    def query(self, topic):
        """Query the RAG system with a topic"""
        if self.collection is None:
            return {"error": "Vector database not initialized. Run embeddings.py first."}
        
        try:
            # Retrieve quotes
            quotes = self.retrieve_quotes(topic)
            
            # Check if there was an error
            if isinstance(quotes, dict) and "error" in quotes:
                return quotes
            
            # Generate response
            response = self.generate_response(topic, quotes)
            return response
        except Exception as e:
            return {"error": f"Error querying RAG system: {e}"}

# For testing
if __name__ == "__main__":
    rag = QuotesRAG()
    result = rag.query("business")
    print(result) 