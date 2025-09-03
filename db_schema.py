import psycopg2
from psycopg2.extras import RealDictCursor
import os

database_url = os.environ.get("DATABASE_URL", "postgresql://gdriveuser:romanempire@localhost:5432/minigdrive")

def init_db():
    try:
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        c = conn.cursor()

        c.execute("""create table if not exists users (
                  id serial primary key,
                  username text,
                  password text,
                  bio text,
                  age integer,
                  profile_pic text
                )
            """)
            
        c.execute("""create table if not exists favourites (
                      id serial primary key,
                      username text not null,
                      filename text not null
                      )
            """)
        
        conn.commit()
        print("Database tables created successfully!")
        
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()