# Shailosophy Quotes Finder - RAG Powered

An AI-powered web application that uses Retrieval-Augmented Generation (RAG) to find the most relevant Shailosophy quotes based on semantic search. Built with Streamlit, OpenAI embeddings, and modern UI/UX principles.

## Features

- **Semantic Search**: Find quotes that are actually related to your topic using AI embeddings
- **Beautiful UI**: Modern Streamlit interface with custom styling and branding
- **Real-time Results**: Get top 3 most relevant quotes with similarity scores
- **Interactive Experience**: Example topics, session state management, and responsive design
- **RAG Implementation**: Full semantic search using OpenAI's text-embedding-3-small model

## Screenshot

The application provides a clean, professional interface with:
- Author branding and social media integration
- Topic-based search with example suggestions
- Formatted quote display with similarity scores
- Responsive design and modern styling

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Step 1: Clone or Download

```bash
git clone <your-repo-url>
cd QuotesEmbeddings
```

### Step 2: Install Dependencies

```bash
pip install -r rag_quotes/requirements.txt
```

Required packages:
- streamlit
- openai
- requests
- pandas (optional, for data manipulation)

### Step 3: Set Up OpenAI API Key

You have several options:

**Option 1: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Option 2: Update config.py**
```python
# In rag_quotes/config.py
OPENAI_API_KEY = "your-api-key-here"
```

**Note**: The current implementation has the API key in the code files. For security, consider moving it to environment variables.

## Initial Setup - Generate Embeddings

Before running the app for the first time, you need to generate embeddings for all quotes:

```bash
cd rag_quotes
python -m models.simple_embeddings
```

This will:
- Read all quotes from `data/ShailosophyQuotes.csv`
- Generate embeddings using OpenAI's API
- Save embeddings to `models/embeddings.json`
- Process all 51 quotes (may take 1-2 minutes)

## Running the Application

### Method 1: Using the run script

```bash
cd rag_quotes
python run.py
```

### Method 2: Direct Streamlit command

```bash
cd rag_quotes
streamlit run app/rag_app.py
```

### Method 3: From project root

```bash
cd rag_quotes && streamlit run app/rag_app.py --server.port 8501
```

The application will be available at: `http://localhost:8501`

## Usage

1. **Open the web app** in your browser
2. **Enter a topic** in the search box (e.g., "business", "leadership", "relationships")
3. **Click Search** or try the example topic buttons
4. **View results** - Top 3 most relevant quotes with similarity scores
5. **Explore** different topics to discover relevant quotes

### Example Topics

Try searching for:
- business
- leadership
- entrepreneurship
- relationships
- growth
- wisdom
- success
- failure
- trust
- communication

## Updating Quotes Data

When you update the quotes in `data/ShailosophyQuotes.csv`:

1. **Regenerate embeddings**:
```bash
cd rag_quotes
python -m models.simple_embeddings
```

2. **Restart the app** - The new embeddings will be loaded automatically

### CSV Format

The CSV file should have the format:
```csv
id,quote
1,"Your quote text here..."
2,"Another quote here..."
```

## Project Structure

```
rag_quotes/
├── app/
│   ├── rag_app.py              # Main Streamlit application
│   └── shailosophy_author.png  # Author image (optional)
├── models/
│   ├── simple_rag.py           # RAG system implementation
│   ├── simple_embeddings.py    # Embeddings generation script
│   └── embeddings.json         # Generated embeddings (auto-created)
├── data/
│   └── ShailosophyQuotes.csv   # Source quotes data
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
└── run.py                      # Convenient run script
```

## Technical Details

### RAG Implementation

- **Embeddings Model**: OpenAI text-embedding-3-small
- **Search Method**: Cosine similarity between query and quote embeddings
- **Results**: Top 3 most similar quotes with similarity scores
- **Caching**: Streamlit resource caching for optimal performance

### Features

- **Semantic Search**: Find quotes by meaning, not just keywords
- **Session State**: Maintains search history and user inputs
- **Error Handling**: Graceful handling of API errors and missing data
- **Modern UI**: Custom CSS styling and responsive design
- **Social Integration**: Links to author's social media profiles

## Troubleshooting

### Common Issues

**1. "Embeddings not found" error**
```bash
# Solution: Generate embeddings first
cd rag_quotes
python -m models.simple_embeddings
```

**2. OpenAI API errors**
- Check your API key is correct
- Ensure you have sufficient API credits
- Verify network connectivity

**3. Import errors**
```bash
# Solution: Install requirements
pip install -r rag_quotes/requirements.txt
```

**4. Port already in use**
```bash
# Solution: Use a different port
streamlit run app/rag_app.py --server.port 8502
```

## API Usage and Costs

- **Embeddings**: ~$0.02 per 1M tokens (one-time cost for setup)
- **Search**: ~$0.02 per 1M tokens for query embeddings (minimal cost per search)
- **Current Dataset**: 51 quotes ≈ minimal cost for embeddings

## License

This project is open-source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the project structure
3. Open an issue in the repository

---

**Built with ❤️ using Streamlit, OpenAI, and modern RAG techniques**
