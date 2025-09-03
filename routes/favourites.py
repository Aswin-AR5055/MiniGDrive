from flask import render_template, redirect, session, request
import os, shutil, datetime
from translations import get_translations
from .profile import get_user_profile
from file_utils import get_user_folder, get_storage_info
from . import app
import psycopg2
from psycopg2.extras import RealDictCursor

database_url = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

@app.route('/favourites')
def favourites():
    if "username" not in session:
        return redirect("/login")

    lang = request.args.get("lang", "en")
    translations = get_translations(lang)

    files = get_user_favourites()
    upload_folder = get_user_folder()
    file_dates = {}
    file_sizes = {}

    for f in files:
        try:
            path = os.path.join(upload_folder, f)
            file_dates[f] = datetime.datetime.utcfromtimestamp(os.path.getmtime(path)).isoformat()
            file_sizes[f] = os.path.getsize(path)
        except Exception:
            file_dates[f] = ""
            file_sizes[f] = 0

    profile = get_user_profile()
    used_mb, max_mb, percent_used = get_storage_info()

    return render_template(
        "favourites.html",
        user=session["username"],
        files=files,
        file_dates=file_dates,
        file_sizes=file_sizes,
        bio=profile["bio"],
        profile_pic=profile["profile_pic"],
        used_mb=used_mb,
        max_mb=max_mb,
        percent_used=percent_used,
        translations=translations,
        lang=lang,
        active_page="favourites"
    )

def get_user_favourites():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT filename FROM favourites WHERE username=%s", (session["username"],))
    rows = c.fetchall()
    conn.close()
    
    upload_folder = get_user_folder()
    existing_files = []
    for row in rows:
        filename = row["filename"]
        file_path = os.path.join(upload_folder, filename)
        if os.path.exists(file_path):
            existing_files.append(filename)
        else:
            remove_favourite(filename) 
    return existing_files

def add_favourite(filename):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO favourites (username, filename)
        VALUES (%s, %s)
        ON CONFLICT (username, filename) DO NOTHING
    """, (session["username"], filename))
    conn.commit()
    conn.close()

def remove_favourite(filename):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM favourites WHERE username=%s AND filename=%s", (session["username"], filename))
    conn.commit()
    conn.close()
