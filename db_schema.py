from db import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                create table if not exists users(   
                id serial primary key,
                username text unique,
                password text,
                bio text,
                age integer,
                profile_pic text
                )
            """)
    cur.execute("""
                create table if not exists favourites (
                id serial primary key,
                username text not null,
                filename text not null,
                unique(username, filename)
                )
            """)
    
    conn.commit()
    cur.close()
    conn.close()
