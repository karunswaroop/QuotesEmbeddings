import streamlit as st
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.rag_system import QuotesRAG

# Set page config
st.set_page_config(
    page_title="Shailosophy Quotes Finder",
    page_icon="📚",
    layout="centered"
)

# Initialize the RAG system
@st.cache_resource
def get_rag_system():
    return QuotesRAG()

rag = get_rag_system()

# App header
st.title("Shailosophy Quotes Finder")
st.markdown("""
Find meaningful Shailosophy quotes related to your topic of interest.
Enter a topic below to discover relevant quotes.
""")

# Input section
topic = st.text_input("Enter a topic (e.g., business, leadership, growth):", "Business")
search_button = st.button("Find Quotes")

# Results section
if search_button or topic:
    with st.spinner("Searching for quotes..."):
        response = rag.query(topic)
    
    st.subheader(f"Top Quotes Related to '{topic}'")
    
    # Display the response
    if hasattr(response, 'content'):
        st.write(response.content)
    elif isinstance(response, dict) and 'error' in response:
        st.error(response['error'])
    else:
        st.write(response)

# Footer
st.markdown("---")
st.markdown("Powered by OpenAI Agents SDK and text-embedding-3-small") 