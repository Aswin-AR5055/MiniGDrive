import psycopg2
import psycopg2.extras

def get_connection():
    return psycopg2.connect(
        dbname = "minigdrive",
        user = "minigdrive_user",
        password = "romanempire",
        host = "localhost",
        port = "5432",
    )