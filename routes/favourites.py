from flask import render_template, redirect, session, request
import os, datetime
from db import get_connection
from translations import get_translations
from .profile import get_user_profile
from file_utils import get_user_folder, get_storage_info
from . import app
from psycopg2.extras import RealDictCursor

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
        bio=profile.get("bio", ""),
        profile_pic=profile.get("profile_pic"),
        used_mb=used_mb,
        max_mb=max_mb,
        percent_used=percent_used,
        translations=translations,
        lang=lang,
        active_page="favourites"
    )


def get_user_favourites():
    """Fetch favourite files that actually exist on disk."""
    username = session.get("username")
    if not username:
        return []

    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT filename FROM favourites WHERE username=%s", (username,))
            rows = cur.fetchall()
    finally:
        conn.close()

    upload_folder = get_user_folder()
    existing_files = []

    for row in rows:
        filename = row["filename"]  # access by column name
        file_path = os.path.join(upload_folder, filename)
        if os.path.exists(file_path):
            existing_files.append(filename)
        else:
            # Remove broken favourite safely
            try:
                remove_favourite(filename)
            except Exception:
                pass

    return existing_files



def add_favourite(filename):
    """Add a file to user's favourites (idempotent)."""
    username = session.get("username")
    if not username or not filename:
        return

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO favourites (username, filename)
                VALUES (%s, %s)
                ON CONFLICT (username, filename) DO NOTHING
                """,
                (username, filename)
            )
            conn.commit()
    finally:
        conn.close()


def remove_favourite(filename):
    """Remove a file from user's favourites."""
    username = session.get("username")
    if not username or not filename:
        return

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM favourites WHERE username=%s AND filename=%s",
                (username, filename)
            )
            conn.commit()
    finally:
        conn.close()
