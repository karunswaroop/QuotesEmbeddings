# Shailosophy Quotes Finder 📚

A Streamlit application that uses AI-powered semantic search to find relevant Shailosophy quotes based on user topics.

## Features

- AI-powered semantic search using OpenAI's text-embedding-3-small model
- Clean and intuitive user interface
- Real-time quote search based on topics
- Example topics for quick exploration
- Mobile-responsive design

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

5. Run the Streamlit app:
```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Fork this repository to your GitHub account.

2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud) if you haven't already.

3. Create a new app in Streamlit Cloud:
   - Connect your GitHub account
   - Select this repository
   - Set the main file path as `app.py`

4. Set up your secrets in Streamlit Cloud:
   - Go to your app's settings
   - Under "Secrets", add the following:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

5. Deploy! Streamlit Cloud will automatically deploy your app and provide you with a URL.

## Project Structure

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
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Shailosophy for providing the insightful quotes
- OpenAI for the embeddings model
- Streamlit for the amazing web framework

---

🚀 **Powered by**: [Colaberry Inc](https://www.colaberry.com/) | **Author**: [@shailosophy](https://www.threads.com/@shailosophy) 