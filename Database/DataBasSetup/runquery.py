import os
from dotenv import load_dotenv
from Database.Connection import get_db_connection

load_dotenv()

conn = get_db_connection()

if not conn:
    print("❌ Database connection failed")
    exit(1)

cursor = conn.cursor()

print("✅ Database connection successful")

try:
    # ---- Embedding dimension ----
    embedding_dimension = int(os.getenv("EMBEDDING_DIMENSION", 384))

    # ---- Enable pgvector extension ----
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()
    print("✅ pgvector extension ensured")

    # ---- Check if table exists ----
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'documents'
        );
    """)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        cursor.execute(f"""
            CREATE TABLE documents (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding VECTOR({embedding_dimension})
            );
        """)
        conn.commit()
        print("✅ documents table created")
    else:
        print("ℹ️ documents table already exists")

except Exception as e:
    conn.rollback()
    print(f"❌ Error occurred: {e}")

finally:
    cursor.close()
    conn.close()
