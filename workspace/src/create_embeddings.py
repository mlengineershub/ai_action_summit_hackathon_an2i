from sentence_transformers import SentenceTransformer
from typing import List
from workspace.src.db_utils import (
    get_database, 
    get_table 
)


# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str) -> List[float]:
    """Generate embedding for a given text using Sentence Transformers."""
    return model.encode(text).tolist()  # Convert numpy array to list for MongoDB

def add_embeddings_to_collection(table_name: str = "Consultation") -> None:
    """
    Iterate through all documents in the collection, generate embeddings for the
    'intelligent_summary' field, and add the 'embedding' attribute to each document.
    """
    # Get MongoDB client, database, and collection
    db = get_database()
    table = get_table(db, table_name)
    # Find all documents in the collection
    documents = table.find({})

    for doc in documents:
        # Check if the document already has an embedding (to avoid reprocessing)
        if 'embedding' not in doc:
            # Generate embedding for the 'intelligent_summary' field
            embedding = generate_embedding(doc['intelligent_summary'])
            
            # Update the document with the new 'embedding' attribute
            table.update_one(
                {'_id': doc['_id']},  # Match the document by its unique ID
                {'$set': {'embedding': embedding}}  # Add the embedding
            )
            print(f"Added embedding to document with reportID: {doc['reportID']}")
        else:
            print(f"Document with reportID: {doc['reportID']} already has an embedding.")

# Example usage
if __name__ == "__main__":
    add_embeddings_to_collection()