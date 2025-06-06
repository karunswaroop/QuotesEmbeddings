import streamlit as st
import sys
import os
import base64

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.simple_rag import SimpleRAG

def get_base64_image(image_path):
    """Convert image to base64 string for HTML embedding"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set page config
st.set_page_config(
    page_title="Shailosophy Quotes Finder - RAG Powered",
    page_icon="📚",
    layout="centered"
)

# Initialize session state for topic
if 'topic' not in st.session_state:
    st.session_state.topic = "Business"

# Initialize the RAG system
@st.cache_resource
def get_rag_system():
    return SimpleRAG()

# App header with author image
col1, col2 = st.columns([2, 3])

with col1:
    # Try to display the author image if available
    import os
    image_path = os.path.join(os.path.dirname(__file__), "shailosophy_author.png")
    
    # Add some vertical spacing to center the image better
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    
    if os.path.exists(image_path):
        # Convert to relative path for HTML
        relative_path = "shailosophy_author.png"
        st.markdown(f"""
        <a href="https://www.threads.com/@shailosophy" target="_blank">
            <img src="data:image/png;base64,{get_base64_image(image_path)}" style="width: 100%; cursor: pointer;">
        </a>
        """, unsafe_allow_html=True)
    else:
        # Placeholder for when image is added
        st.markdown("""
        <div style='width: 150px; height: 150px; border: 2px dashed #ccc; 
                    display: flex; align-items: center; justify-content: center; 
                    border-radius: 10px; margin: 10px 0;'>
            <span style='color: #666; text-align: center;'>Shailosophy<br/>Author Image</span>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("# <a href='https://www.threads.com/@shailosophy' target='_blank' style='text-decoration: none; color: inherit;'>Shailosophy</a><br/>Quotes Finder", unsafe_allow_html=True)
    st.markdown("""
    Find meaningful Shailosophy quotes that are actually related to your topic of interest.
    Enter a topic below to discover the most relevant quotes using AI-powered semantic search.
    """)

st.markdown("---")

# Initialize RAG
try:
    rag = get_rag_system()
    if rag.embeddings_data is None:
        st.error("⚠️ Embeddings not found. Please run the embeddings creation script first.")
        st.stop()
    
    st.success(f"✅ System loaded with {len(rag.embeddings_data)} quotes")
except Exception as e:
    st.error(f"❌ Error loading RAG system: {e}")
    st.stop()

# Input section
st.markdown("### 🔍 Search for Quotes")
topic = st.text_input(
    "Enter a topic (e.g., business, leadership, growth, relationships, wisdom):", 
    value=st.session_state.topic,
    key="topic_input",
    placeholder="Type your topic here..."
)

# Update session state when text input changes
if topic != st.session_state.topic:
    st.session_state.topic = topic

col1, col2 = st.columns([1, 4])
with col1:
    search_button = st.button("🔍 Search", type="primary")

# Example topics
with st.expander("💡 Try these example topics"):
    example_topics = [
        "business", "leadership", "entrepreneurship", "relationships", 
        "growth", "wisdom", "success", "failure", "trust", "communication"
    ]
    
    cols = st.columns(5)
    for i, example in enumerate(example_topics):
        with cols[i % 5]:
            if st.button(f"#{example}", key=f"example_{i}"):
                st.session_state.topic = example
                st.rerun()

# Use the topic from session state
current_topic = st.session_state.topic

# Results section
if (search_button or current_topic) and current_topic.strip():
    with st.spinner("🔍 Searching for relevant quotes using AI..."):
        result = rag.query(current_topic.strip())
    
    if result['success']:
        st.markdown(f"### Here are the top 3 quotes related to '{current_topic}':")
        st.markdown("")  # Add some space
        
        # Display quotes in a clean, numbered format
        for i, quote_data in enumerate(result['quotes'], 1):
            # Format the quote with proper line breaks
            lines = quote_data['quote'].split('\n')
            formatted_lines = [line.strip() for line in lines if line.strip()]
            
            if len(formatted_lines) > 1:
                formatted_quote = '<br><br>'.join(formatted_lines)
            else:
                formatted_quote = formatted_lines[0] if formatted_lines else ""
            
            # Display quote header with similarity score
            similarity_pct = f"{quote_data['similarity']:.1%}"
            st.markdown(f"**Quote #{quote_data['id']} (Similarity: {similarity_pct})**")
            
            # Display the quote content with styling
            quote_html = f"""
            <blockquote style='border-left: 3px solid #ccc; padding-left: 15px; margin-left: 0; font-style: italic; line-height: 1.6; margin-top: 10px; margin-bottom: 20px;'>
                {formatted_quote}
            </blockquote>
            """
            st.markdown(quote_html, unsafe_allow_html=True)
            
            # Add separator line between quotes (except after the last one)
            if i < len(result['quotes']):
                st.markdown("---")
    
    else:
        st.error(f"❌ {result['error']}")

elif search_button and not current_topic.strip():
    st.warning("⚠️ Please enter a topic to search for quotes.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    🚀 <strong>Full Semantic Implementation</strong> - Powered by <a href="https://www.colaberry.com/" target="_blank">Colaberry Inc</a>, using OpenAI's LLM
</div>
""", unsafe_allow_html=True) 