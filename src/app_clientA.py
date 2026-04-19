import chromadb
from chromadb.utils import embedding_functions

# 1. Setup Chroma (Persist to local folder)
client = chromadb.PersistentClient(path="./chroma_data")

# 2. Define the embedding model (Standard for ADHD/ESL text)
default_ef = embedding_functions.DefaultEmbeddingFunction()

# 3. Create or get your collection
collection = client.get_or_create_collection(
    name="adhd_study_guides", 
    embedding_function=default_ef
)

def get_study_guide(user_text):
    # Search for the top 1 result within a distance threshold
    results = collection.query(
        query_texts=[user_text],
        n_results=1
    )
    
    # Check if we have a match and if it's "close enough" 
    # (Distance < 0.4 usually means very similar meaning)
    if results['ids'][0] and results['distances'][0][0] < 0.4:
        print("🎯 Semantic Match Found! Returning cached guide.")
        return results['metadatas'][0][0]['study_guide_json']
    
    # Otherwise, generate new one
    print("🤖 New Content Detected. Calling LLM...")
    new_guide_json = call_llm_api(user_text)
    
    # Save to Chroma for next time
    collection.add(
        documents=[user_text],
        metadatas=[{"study_guide_json": new_guide_json}],
        ids=[generate_unique_id()] # e.g., a timestamp or hash
    )
    
    return new_guide_json