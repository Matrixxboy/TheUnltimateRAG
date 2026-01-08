import psycopg2
import os
import sys
from dotenv import load_dotenv
from theultimaterag.config.settings import settings
load_dotenv()



def get_db_connection():
    conn = None
    try:
        # Define connection parameters (replace placeholders)
        conn_params = {
            "host": settings.POSTGRES_HOST,
            "database": settings.POSTGRES_DB,
            "user": settings.POSTGRES_USER,
            "password": settings.POSTGRES_PASSWORD,
            "port": settings.POSTGRES_PORT
        }

        conn = psycopg2.connect(**conn_params)
        if conn.closed == 0:
            pass # Silent success
            # print("PostgreSQL connected successfully ✅")

    except (Exception, psycopg2.DatabaseError) as error:
        # print(f"An error occurred: {error}")
        return None
    
    return conn

if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        conn.close()
        print('Database connection closed.')
