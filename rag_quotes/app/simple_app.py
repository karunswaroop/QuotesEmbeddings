import streamlit as st
import csv
import random
import os

# Set page config
st.set_page_config(
    page_title="Shailosophy Quotes Finder",
    page_icon="📚",
    layout="centered"
)

# Load quotes from CSV
def load_quotes():
    quotes = []
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    csv_path = os.path.join(parent_dir, "data", "ShailosophyQuotes.csv")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                quotes.append({
                    "id": row[0],
                    "quote": row[1]
                })
        return quotes
    except Exception as e:
        st.error(f"Error loading quotes: {e}")
        return []

# App header
st.title("Shailosophy Quotes Finder")
st.markdown("""
Find meaningful Shailosophy quotes related to your topic of interest.
Enter a topic below to discover relevant quotes.
""")

# Load quotes
quotes = load_quotes()

# Input section
topic = st.text_input("Enter a topic (e.g., business, leadership, growth):", "Business")
search_button = st.button("Find Quotes")

# Results section
if search_button or topic:
    st.subheader(f"Quotes Related to '{topic}'")
    
    # Simple implementation - just show random quotes
    if quotes:
        # Select 3 random quotes for demo purposes
        selected_quotes = random.sample(quotes, min(3, len(quotes)))
        
        for quote in selected_quotes:
            st.markdown(f"**Quote #{quote['id']}**")
            
            # Use a container with proper styling for the quote
            with st.container():
                # Split the quote by newlines and create proper paragraphs
                quote_text = quote['quote']
                
                # Replace single newlines with double newlines for better paragraph spacing
                # First, split by existing newlines
                lines = quote_text.split('\n')
                formatted_lines = []
                
                for line in lines:
                    line = line.strip()
                    if line:  # Only add non-empty lines
                        formatted_lines.append(line)
                
                # Join lines with proper spacing
                if len(formatted_lines) > 1:
                    # If multiple lines, add paragraph breaks
                    formatted_quote = '<br><br>'.join(formatted_lines)
                else:
                    formatted_quote = formatted_lines[0] if formatted_lines else ""
                
                quote_html = f"""
                <blockquote style='border-left: 3px solid #ccc; padding-left: 15px; margin-left: 0; font-style: italic; line-height: 1.6;'>
                    {formatted_quote}
                </blockquote>
                """
                
                st.markdown(quote_html, unsafe_allow_html=True)
            
            st.markdown("---")
    else:
        st.warning("No quotes available.")

# Footer
st.markdown("---")
st.markdown("Simple demo version - using random selection instead of embedding search") 