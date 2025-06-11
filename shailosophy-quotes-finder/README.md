# Shailosophy Quotes Finder 📚

A RAG-powered application that finds meaningful Shailosophy quotes using AI semantic search.

## ✨ Features

- **Semantic Search**: Find quotes that truly relate to your topics using OpenAI embeddings
- **AI Insights**: Get intelligent responses about how quotes relate to your search
- **Beautiful UI**: Clean Streamlit interface with author branding
- **Fast & Accurate**: Vector-based similarity search with cosine similarity

## 🚀 Quick Start

### 1. Set up your environment

```bash
# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key
echo "OPENAI_API_KEY=your-actual-api-key-here" > .env
```

### 2. Generate embeddings

```bash
python generate_embeddings.py
```

### 3. Run the application

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501` and start searching for quotes!

## 📁 Project Structure

```
shailosophy-quotes-finder/
├── app.py                  # Main Streamlit application
├── config.py              # Configuration settings
├── rag_system.py          # RAG system logic
├── generate_embeddings.py # Embeddings generation script
├── data/
│   └── ShailosophyQuotes.csv  # Source quotes (51 quotes)
├── assets/
│   └── shailosophy_author.png # Author image
├── tests/
│   └── test_api.py        # API connection tests
├── embeddings.json        # Generated embeddings file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API key)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Configuration

The application uses environment variables for configuration:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- Models used: `text-embedding-3-small` for embeddings, `gpt-4o-mini` for chat

## 🧪 Testing

Test your API connection:

```bash
python tests/test_api.py
```

## 📊 How It Works

1. **Data Loading**: Reads quotes from `data/ShailosophyQuotes.csv`
2. **Embeddings**: Converts quotes to vectors using OpenAI's embedding model
3. **Search**: Uses cosine similarity to find most relevant quotes
4. **Response**: Generates AI insights about the quotes and your topic

## 🛠️ Development

### Regenerate embeddings after updating quotes:

```bash
python generate_embeddings.py
```

### Add new quotes:

1. Update `data/ShailosophyQuotes.csv`
2. Run `python generate_embeddings.py`
3. Restart the Streamlit app

## 🔒 Security

- API keys are stored in `.env` file (not committed to git)
- All sensitive files are protected by `.gitignore`
- No hardcoded credentials in source code

## 📝 Dependencies

- `streamlit` - Web application framework
- `openai` - OpenAI API client (via requests)
- `pandas` - Data manipulation
- `python-dotenv` - Environment variable management
- `requests` - HTTP client

## 🎯 Usage Examples

Search for quotes about:
- "business strategy"
- "leadership principles"
- "entrepreneurial mindset"
- "building trust"
- "personal growth"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python tests/test_api.py`
5. Submit a pull request

## 📄 License

This project is for educational and personal use.

---

🚀 **Powered by**: [Colaberry Inc](https://www.colaberry.com/) | **Author**: [@shailosophy](https://www.threads.com/@shailosophy) 