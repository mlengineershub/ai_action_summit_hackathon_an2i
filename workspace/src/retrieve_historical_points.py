from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any
from workspace.src.db_utils import get_database, get_table

# Initialize Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> List[float]:
    """Generate embedding for a given text using Sentence Transformers."""
    return model.encode(text).tolist()


def similarity_search(
    query: str, table_name: str = "Consultation", top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    Perform similarity search using stored embeddings.
    Returns top_k most similar documents with scores.
    """
    # Get database connection
    db = get_database()
    table = get_table(db, table_name)

    # Generate query embedding and ensure proper shape
    query_embedding = np.array(generate_embedding(query)).reshape(1, -1)

    # Retrieve documents with embeddings
    documents_with_embeddings = list(
        table.find(
            {"embedding": {"$exists": True}},
            {"embedding": 1, "intelligent_summary": 1, "reportID": 1, "_id": 0},
        )
    )

    # Handle empty collection case
    if not documents_with_embeddings:
        print("No documents with embeddings found in the collection.")
        return []

    # Prepare embeddings matrix
    stored_embeddings = np.array(
        [doc["embedding"] for doc in documents_with_embeddings]
    )

    # Calculate cosine similarities
    similarity_scores = cosine_similarity(query_embedding, stored_embeddings)[0]

    # Get top_k indices
    top_indices = np.argsort(similarity_scores)[-top_k:][::-1]

    # Prepare results
    results = []
    for idx in top_indices:
        doc = documents_with_embeddings[idx]
        results.append(
            {
                "reportID": doc["reportID"],
                "intelligent_summary": doc["intelligent_summary"],
                "similarity_score": float(similarity_scores[idx]),
            }
        )

    return results


# Example usage
if __name__ == "__main__":
    query = "Patient with high fever and persistent cough"
    results = similarity_search(query, top_k=3)

    print(f"Top {len(results)} similar consultations:")
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Report ID: {result['reportID']}")
        print(f"Similarity Score: {result['similarity_score']:.4f}")
        print(f"Summary: {result['intelligent_summary']}")
