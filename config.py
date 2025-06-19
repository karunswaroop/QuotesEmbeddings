"""
Configuration settings for Shailosophy Quotes Finder
"""

import os
import streamlit as st

# API Settings
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "your-api-key-here")

# Model Settings
EMBEDDING_MODEL = "text-embedding-3-small"

# File Paths
DATA_DIR = "data"
ASSETS_DIR = "assets"
QUOTES_FILE = os.path.join(DATA_DIR, "ShailosophyQuotes.csv")
EMBEDDINGS_FILE = "embeddings.json"

# Application Settings
TOP_N_RESULTS = 3
DEFAULT_TOPIC = "Business" 