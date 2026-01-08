from sentence_transformers import SentenceTransformer
from theultimaterag.Database.Connection import get_db_connection

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def add_data(content: str):
    """
    Generates an embedding for the content and stores it in the database.
    """
    conn = get_db_connection()
    if conn is None:
        return

    try:
        # Generate embedding
        embedding = model.encode(content).tolist()
        
        cursor = conn.cursor()
        
        # Insert into database
        cursor.execute(
            "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
            (content, embedding)
        )
        
        conn.commit()
        print(f"✅ Added document: '{content[:30]}...'")
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error adding data: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    # Test adding data
    # add_data("This is a test sentence for the vector database.")
    pass
