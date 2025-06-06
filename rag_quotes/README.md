# Shailosophy Quotes RAG System

This application uses OpenAI's text-embedding-3-small model for embeddings and o4-mini-2025-04-16 for LLM responses to create a Retrieval-Augmented Generation (RAG) system for Shailosophy quotes.

## Features

- Vector search for relevant quotes based on user input topics
- Returns top 3 most relevant quotes using semantic similarity
- Simple Streamlit UI for interacting with the system
- Built with OpenAI's chat completions API

## Setup

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. The application uses the following OpenAI API key:
   ```
   OPENAI_API_KEY=sk-svcacct-AlOr9iIw9iHN7b74ktBWT3BlbkFJcWnle5crbd0pvzMYQKBF
   ```

## Usage

You can run the application in one go:

```bash
python run.py
```

Or run specific steps:

1. Setup the environment:
   ```
   python run.py --setup
   ```

2. Create embeddings for the quotes:
   ```
   python run.py --embeddings
   ```

3. Run the Streamlit app:
   ```
   python run.py --run
   ```

## How It Works

1. The application loads quotes from the ShailosophyQuotes.csv file
2. It generates embeddings for each quote using text-embedding-3-small
3. The embeddings are stored in a ChromaDB vector database
4. When a user enters a topic, the application:
   - Converts the query to an embedding
   - Finds the most similar quotes in the vector database
   - Uses OpenAI's o4-mini-2025-04-16 model to generate a response
   - Returns the top 3 most relevant quotes with insights

## Project Structure

```
rag_quotes/
├── app/
│   └── app.py              # Streamlit UI
├── data/
│   └── ShailosophyQuotes.csv  # Source quotes
├── models/
│   ├── embeddings.py       # Script to generate embeddings
│   └── rag_system.py       # RAG implementation
├── config.py               # Configuration settings
├── requirements.txt        # Dependencies
├── run.py                  # Main runner script
└── README.md               # This file
``` 