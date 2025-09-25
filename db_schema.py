import psycopg2
from psycopg2 import sql
import os

def get_db_connection():
    conn = psycopg2.connect(
        host = "postgres",
        database = os.getenv("POSTGRES_DB"),
        user = os.getenv("POSTGRES_USER"),
        password = os.getenv("POSTGRES_PASSWORD")
    )
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            bio TEXT,
            age INTEGER,
            profile_pic TEXT
        )
    """)
    
    # Create favourites table
    c.execute("""
        CREATE TABLE IF NOT EXISTS favourites (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            filename TEXT NOT NULL
        )
    """)
    
    conn.commit()
    c.close()
    conn.close()

# Initialize tables on import
init_db()