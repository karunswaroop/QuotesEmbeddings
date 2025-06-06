import os
from openai import OpenAI

# Set API key
api_key = "sk-svcacct-AlOr9iIw9iHN7b74ktBWT3BlbkFJcWnle5crbd0pvzMYQKBF"
os.environ["OPENAI_API_KEY"] = api_key

client = OpenAI(api_key=api_key)

try:
    # Test embedding generation
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="This is a test"
    )
    print("Embedding generated successfully!")
    print(f"Embedding dimensions: {len(response.data[0].embedding)}")
    
    # Test chat completions
    chat_response = client.chat.completions.create(
        model="o4-mini-2025-04-16",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides quotes."},
            {"role": "user", "content": "Give me a quote about perseverance."}
        ],
        max_tokens=100
    )
    
    print("\nChat completion generated successfully!")
    print(f"Response: {chat_response.choices[0].message.content}")
    
except Exception as e:
    print(f"Error: {e}") 