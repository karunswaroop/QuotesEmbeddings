import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# Model Settings
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"

# Vector Database Settings
CHROMA_PERSIST_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "chroma_db")

# Data Settings
QUOTES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ShailosophyQuotes.csv")

# Application Settings
TOP_N_RESULTS = 3 