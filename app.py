"""
Shailosophy Quotes Finder - RAG Powered Streamlit Application
Find meaningful Shailosophy quotes using AI-powered semantic search.
"""

import streamlit as st
import os
import base64
from rag_system import ShailosophyRAG

def get_base64_image(image_path):
    """Convert image to base64 string for HTML embedding"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set page config
st.set_page_config(
    page_title="sh AI lu - Shailosophy Quotes Finder",
    page_icon="📚",
    layout="centered"
)

# Hide GitHub repo link, fork button, and other Streamlit UI elements
st.markdown("""
<style>
    /* Hide GitHub-related elements */
    .css-1jc7ptx, .css-1p1nwyz, .css-gl881z, .css-zt5igj {
        display: none !important;
    }
    
    /* Hide all GitHub corner elements */
    .github-corner {
        display: none !important;
    }
    
    /* Hide fork button and repo link */
    [data-testid="stGitHubLink"] {
        display: none !important;
    }
    
    /* Hide Streamlit branding and menu */
    #MainMenu, [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Hide footer */
    footer {
        display: none !important;
    }
    
    /* Hide header decoration */
    .decoration {
        display: none !important;
    }
    
    /* Additional selectors for GitHub elements */
    .stGitHubLink {
        display: none !important;
    }
    
    /* Hide any elements with GitHub in their attributes */
    [href*="github"], [src*="github"] {
        display: none !important;
    }

    /* Style for the main title */
    .main-app-title {
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        letter-spacing: -0.02em;
    }
    
    .main-app-title .sh-text {
        background: linear-gradient(135deg, #0396FF, #0D47A1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Style for the AI part of the title */
    .main-app-title .ai-text {
        background: linear-gradient(135deg, #32CD32, #2E8B57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
    }
    
    .main-app-title .lu-text {
        background: linear-gradient(135deg, #0396FF, #0D47A1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Header container styles */
    .header-container {
        display: flex;
        align-items: center;
        padding: 2rem 0 1.5rem;
        gap: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .image-container {
        flex: 1;
        max-width: 220px;
        transition: transform 0.3s ease;
    }
    
    .image-container:hover {
        transform: translateY(-5px);
    }
    
    .text-container {
        flex: 2;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .author-image {
        width: 100%;
        max-width: 200px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    .author-image:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 25px rgba(0,0,0,0.2);
    }
    
    .app-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0.7rem 0 1rem;
        line-height: 1.1;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif;
        letter-spacing: -0.01em;
        color: #E8EAED;
    }
    
    .app-title a {
        display: inline-block;
        text-decoration: none;
        color: inherit;
        transition: opacity 0.2s ease;
    }
    
    .app-title a:hover {
        opacity: 0.9;
    }
    
    .app-title br {
        display: block;
        content: "";
        margin-top: -0.2em;
    }
    
    .main-description {
        font-size: 1.15rem;
        color: #9AA0A6;
        line-height: 1.6;
        margin: 0.8rem 0 0;
        font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif;
        max-width: 90%;
    }
    
    @media (max-width: 768px) {
        .header-container {
            flex-direction: column;
            text-align: center;
            gap: 1.5rem;
            padding: 1.5rem 0;
        }
        
        .image-container {
            max-width: 180px;
        }
        
        .main-app-title {
            font-size: 2.8rem;
        }
        
        .app-title {
            font-size: 2rem;
        }
        
        .main-description {
            font-size: 1.1rem;
            margin: 0.6rem auto 0;
        }
    }
    
    /* Dark theme optimizations */
    @media (prefers-color-scheme: dark) {
        .main-description {
            color: #9AA0A6;
        }
        .app-title {
            color: #E8EAED;
        }
    }
</style>
""", unsafe_allow_html=True)

# Create the header layout
image_path = os.path.join("assets", "shailosophy_author.png")

if os.path.exists(image_path):
    st.markdown(f"""
    <div class="header-container">
        <div class="image-container">
            <a href="https://www.threads.com/@shailosophy" target="_blank">
                <img src="data:image/png;base64,{get_base64_image(image_path)}" 
                     class="author-image" 
                     alt="Shailosophy Author">
            </a>
        </div>
        <div class="text-container">
            <h1 class="main-app-title">
                <span class="sh-text">sh</span> 
                <span class="ai-text">AI</span> 
                <span class="lu-text">lu</span>
            </h1>
            <div class="app-title">
                <a href="https://www.threads.com/@shailosophy" target="_blank">
                    Shailosophy<br/>
                    Quotes Finder
                </a>
            </div>
            <div class="main-description">
                Find meaningful Shailosophy quotes that are actually related to your topic of interest. 
                Enter a topic below to discover the most relevant quotes using AI-powered semantic search.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Fallback layout if image not found
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div style='width: 150px; height: 150px; border: 2px dashed #ccc; 
                    display: flex; align-items: center; justify-content: center; 
                    border-radius: 10px; margin: 20px auto;'>
            <span style='color: #666; text-align: center;'>Shailosophy<br/>Author Image</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <h1 class="main-app-title">
            <span class="sh-text">sh</span> 
            <span class="ai-text">AI</span> 
            <span class="lu-text">lu</span>
        </h1>
        """, unsafe_allow_html=True)
        st.markdown("# Shailosophy\nQuotes Finder")
        st.markdown("""
        Find meaningful Shailosophy quotes that are actually related to your topic of interest.
        Enter a topic below to discover the most relevant quotes using AI-powered semantic search.
        """)

st.markdown("---")

# Initialize session state for topic
if 'topic' not in st.session_state:
    st.session_state.topic = "Business"

# Initialize the RAG system
@st.cache_resource
def get_rag_system():
    return ShailosophyRAG()

# App header with author image - improved layout
st.markdown("---")

# Initialize RAG
try:
    rag = get_rag_system()
    if not rag.is_ready():
        st.error("⚠️ Embeddings not found. Please run the embeddings creation script first.")
        st.code("python generate_embeddings.py")
        st.stop()
    
    st.success(f"✅ System loaded with {rag.get_quotes_count()} quotes")
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
        result = rag.search(current_topic.strip())
    
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

colaberry_icon_path = os.path.join("assets", "ColaberryIcon.webp")
if os.path.exists(colaberry_icon_path):
    st.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        🚀 <strong>Full Semantic Search Implementation</strong> - Powered by 
        <a href="https://www.colaberry.com/" target="_blank" style="text-decoration: none;">
            <img src="data:image/webp;base64,{get_base64_image(colaberry_icon_path)}" 
                 style="height: 20px; vertical-align: middle; margin: 0 5px;" 
                 alt="Colaberry Inc">
        </a>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        🚀 <strong>Full Semantic Implementation</strong> - Powered by 
        <a href="https://www.colaberry.com/" target="_blank">Colaberry Inc</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    pass 