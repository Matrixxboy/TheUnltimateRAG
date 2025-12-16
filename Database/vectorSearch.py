from sentence_transformers import SentenceTransformer
from Database.Connection import get_db_connection

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_similar_documents(query: str, top_k: int = 5):
    """
    Searches for the most similar documents to the query string.
    Returns a list of (id, content, score) tuples.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    try:
        # Generate embedding for the query
        query_embedding = model.encode(query).tolist()

        cursor = conn.cursor()

        # Search query using Cosine Distance (<=>)
        # Note: We order by distance ascending (closest first)
        cursor.execute(f"""
            SELECT id, content, (embedding <=> %s::vector) as distance
            FROM documents
            ORDER BY distance ASC
            LIMIT %s;
        """, (query_embedding, top_k))

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    except Exception as e:
        print(f"❌ Error searching documents: {e}")
        if conn:
            conn.close()
        return []

# if __name__ == "__main__":
    # Test search
    # results = search_similar_documents("test vector")
    # for res in results:
    #     print(res)
