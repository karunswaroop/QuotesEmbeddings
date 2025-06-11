# Shailosophy Quotes RAG System

This application uses OpenAI's text-embedding-3-small model for embeddings and gpt-4o-mini for LLM responses to create a Retrieval-Augmented Generation (RAG) system for Shailosophy quotes.

## Quick Start

1. **Set up your OpenAI API key in a .env file:**
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

2. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Generate embeddings:**
   ```bash
   python -m models.simple_embeddings
   ```

4. **Run the application:**
   ```bash
   streamlit run app/rag_app.py
   ```

## Alternative: Use the Run Script

```bash
# Run everything automatically
python run.py

# Or run specific components
python run.py --setup        # Install requirements
python run.py --test         # Test API connection
python run.py --embeddings   # Generate embeddings
python run.py --run          # Run the app
```

## Features

- Vector search for relevant quotes based on user input topics
- Returns top 3 most relevant quotes using semantic similarity
- Beautiful Streamlit UI for interacting with the system
- Built with OpenAI's API for embeddings and chat completions

## Project Structure

```
rag_quotes/
├── app/
│   └── rag_app.py              # Streamlit UI
├── data/
│   └── ShailosophyQuotes.csv   # Source quotes
├── models/
│   ├── simple_embeddings.py   # Script to generate embeddings
│   ├── simple_rag.py          # RAG implementation
│   └── embeddings.json        # Generated embeddings (auto-created)
├── config.py                  # Configuration settings
├── requirements.txt           # Dependencies
├── run.py                     # Main runner script
├── test_openai.py            # API testing script
└── README.md                 # This file
```

## How It Works

1. The application loads quotes from the ShailosophyQuotes.csv file
2. It generates embeddings for each quote using text-embedding-3-small
3. The embeddings are stored as JSON for fast retrieval
4. When a user enters a topic, the application:
   - Converts the query to an embedding
   - Finds the most similar quotes using cosine similarity
   - Returns the top 3 most relevant quotes with similarity scores