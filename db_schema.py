import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
            create table if not exists users (
                id integer primary key,
                username text,
                password text,
                bio text,
                age integer,
                profile_pic text
            )
        """)
    c.execute("""
        create table if not exists favourites (
              id integer primary key autoincrement,
              username text not null,
              filename text not null
            )
        """)
    conn.commit()
    conn.close()
    
init_db()