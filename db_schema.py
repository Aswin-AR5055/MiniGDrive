import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        host = "postgres",
        database = os.getenv("POSTGRES_DB"),
        user = os.getenv("POSTGRES_USER"),
        password = os.getenv("POSTGRES_PASSWORD")
    )
    return conn