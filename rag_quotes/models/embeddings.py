import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions
import sys
import os

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, EMBEDDING_MODEL, CHROMA_PERSIST_DIRECTORY, QUOTES_FILE

# Configure OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def load_quotes():
    """Load quotes from CSV file"""
    try:
        df = pd.read_csv(QUOTES_FILE)
        print(f"Loaded {len(df)} quotes")
        return df
    except Exception as e:
        print(f"Error loading quotes: {e}")
        return None

def create_vector_store(df):
    """Create and populate Chroma vector store with quote embeddings"""
    # Create Chroma client
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)
    
    # Create embedding function
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name=EMBEDDING_MODEL
    )
    
    # Create or get collection
    try:
        collection = client.get_collection(name="shailosophy_quotes")
        print("Collection already exists, using existing collection")
    except:
        collection = client.create_collection(
            name="shailosophy_quotes", 
            embedding_function=openai_ef
        )
        print("Created new collection")
    
    # Extract data
    ids = df.iloc[:, 0].astype(str).tolist()
    documents = df.iloc[:, 1].astype(str).tolist()
    
    # Add documents to collection
    batch_size = 100
    for i in tqdm(range(0, len(documents), batch_size)):
        batch_ids = ids[i:i+batch_size]
        batch_docs = documents[i:i+batch_size]
        
        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            metadatas=[{"source": "shailosophy_quotes"} for _ in batch_ids]
        )
    
    print(f"Added {len(documents)} documents to vector store")
    return collection

def main():
    """Main function to process quotes and create embeddings"""
    # Ensure directories exist
    os.makedirs(os.path.dirname(CHROMA_PERSIST_DIRECTORY), exist_ok=True)
    
    # Load quotes
    df = load_quotes()
    if df is None:
        return
    
    # Create vector store
    collection = create_vector_store(df)
    print("Vector store created successfully")

if __name__ == "__main__":
    main() 