"""
Configuration settings for Shailosophy Quotes Finder
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# Model Settings
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"

# File Paths
DATA_DIR = "data"
ASSETS_DIR = "assets"
QUOTES_FILE = os.path.join(DATA_DIR, "ShailosophyQuotes.csv")
EMBEDDINGS_FILE = "embeddings.json"

# Application Settings
TOP_N_RESULTS = 3
DEFAULT_TOPIC = "Business" 