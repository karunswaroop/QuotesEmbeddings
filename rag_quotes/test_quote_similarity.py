import sys
import os
sys.path.append('models')
from simple_rag import SimpleRAG

def test_quote_similarity():
    """Test what topics the wealth/prosperity quote is most similar to"""
    rag = SimpleRAG()
    
    # The specific quote we want to analyze
    target_quote = "Wealth is a milestone, prosperity is a mindset."
    target_quote_id = "47"
    
    # Different topics to test
    test_topics = [
        "business",
        "money", 
        "finance",
        "success",
        "mindset",
        "psychology", 
        "philosophy",
        "wealth",
        "prosperity",
        "achievement",
        "goals",
        "thinking",
        "personal development",
        "wisdom",
        "life advice",
        "motivation"
    ]
    
    print(f"Testing similarity for quote: '{target_quote}'\n")
    
    results = []
    
    for topic in test_topics:
        try:
            # Get top quotes for this topic
            quotes = rag.search_quotes(topic, top_n=10)  # Get more quotes to find our target
            
            # Find our target quote in the results
            similarity_score = None
            for quote_data in quotes:
                if quote_data['id'] == target_quote_id:
                    similarity_score = quote_data['similarity']
                    break
            
            if similarity_score is not None:
                results.append((topic, similarity_score))
                print(f"{topic:<20}: {similarity_score:.1%}")
            else:
                print(f"{topic:<20}: Not in top 10 results")
                
        except Exception as e:
            print(f"{topic:<20}: Error - {e}")
    
    # Sort by similarity score
    results.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n🎯 Best semantic matches for this quote:")
    for i, (topic, score) in enumerate(results[:5], 1):
        print(f"{i}. {topic}: {score:.1%}")

if __name__ == "__main__":
    test_quote_similarity() 