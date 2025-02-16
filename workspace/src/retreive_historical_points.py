from typing import List
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from db_utils import get_mongo_client, get_database, get_table  # Import your utility functions

# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str) -> List[float]:
    """Generate embedding for a given text using Sentence Transformers."""
    return model.encode(text).tolist()  # Convert numpy array to list for MongoDB

def similarity_search(query: str, table_name: str = "consultation_data", top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a similarity search on the 'intelligent_summary' field using embeddings stored in MongoDB.
    Returns the top-k most similar documents.
    """
    # Get MongoDB client, database, and collection
    client = get_mongo_client()
    db = get_database(client)
    table = get_table(db, table_name)

    # Generate embedding for the query
    query_embedding = generate_embedding(query)
    
    # Retrieve all embeddings and relevant fields from MongoDB
    embeddings = []
    documents = []
    for doc in table.find({}, {'embedding': 1, 'intelligent_summary': 1, 'reportID': 1}):
        embeddings.append(doc['embedding'])
        documents.append(doc)
    
    # Convert embeddings to numpy array
    embeddings = np.array(embeddings)
    
    # Calculate cosine similarity between query embedding and all stored embeddings
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    
    # Sort documents by similarity score
    sorted_indices = np.argsort(similarities)[::-1]
    
    # Return top_k most similar documents
    results = []
    for i in sorted_indices[:top_k]:
        results.append({
            'reportID': documents[i]['reportID'],
            'intelligent_summary': documents[i]['intelligent_summary'],
            'similarity_score': float(similarities[i])  # Convert numpy float to Python float
        })
    
    return results

# Example usage
if __name__ == "__main__":
    # Perform a similarity search
    query = "Patient with high fever and persistent cough"
    results = similarity_search(query, top_k=3)
    for result in results:
        print(f"Report ID: {result['reportID']}, Similarity Score: {result['similarity_score']}")
        print(f"Summary: {result['intelligent_summary']}\n")