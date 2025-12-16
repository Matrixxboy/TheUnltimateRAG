import psycopg2
import os
import sys
from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    conn = None
    try:
        # Define connection parameters (replace placeholders)
        conn_params = {
            "host": os.getenv("POSTGRES_HOST"),
            "database": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "port": os.getenv("POSTGRES_PORT")
        }

        conn = psycopg2.connect(**conn_params)
        print(f'Connected to the PostgreSQL server : {conn}')



    except (Exception, psycopg2.DatabaseError) as error:
        print(f"An error occurred: {error}")
        return None
    
    return conn

if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        conn.close()
        print('Database connection closed.')
