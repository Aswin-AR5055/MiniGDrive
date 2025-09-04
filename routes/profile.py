from flask import request, redirect, render_template, session
from . import app
from translations import get_translations
from db import get_connection
from werkzeug.utils import secure_filename
import os
from psycopg2.extras import RealDictCursor

PROFILE_FOLDER = os.path.join(app.static_folder, "profiles")
os.makedirs(PROFILE_FOLDER, exist_ok=True)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect("/login")

    lang = request.args.get("lang", "en")
    translations = get_translations(lang)
    username = session["username"]

    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if request.method == "POST":
                bio = request.form.get("bio", "")
                age = request.form.get("age")
                age = int(age) if age and age.isdigit() else None
                remove_pic = request.form.get("remove_pic") == "on"
                profile_pic = request.files.get("profile_pic")

                # Handle new profile picture
                if profile_pic and profile_pic.filename:
                    filename = secure_filename(profile_pic.filename)
                    profile_pic_path = os.path.join(PROFILE_FOLDER, filename)
                    profile_pic.save(profile_pic_path)
                    cur.execute(
                        "UPDATE users SET bio=%s, age=%s, profile_pic=%s WHERE username=%s",
                        (bio, age, filename, username)
                    )
                else:
                    cur.execute(
                        "UPDATE users SET bio=%s, age=%s WHERE username=%s",
                        (bio, age, username)
                    )

                # Handle remove picture
                if remove_pic:
                    cur.execute("SELECT profile_pic FROM users WHERE username=%s", (username,))
                    row = cur.fetchone()
                    if row and row.get("profile_pic"):
                        try:
                            os.remove(os.path.join(PROFILE_FOLDER, row["profile_pic"]))
                        except FileNotFoundError:
                            pass
                    cur.execute("UPDATE users SET profile_pic=NULL WHERE username=%s", (username,))

                conn.commit()

            # Fetch current profile data
            cur.execute("SELECT bio, age, profile_pic FROM users WHERE username=%s", (username,))
            row = cur.fetchone()

    finally:
        conn.close()

    return render_template(
        "profile.html",
        user=username,
        bio=row.get("bio") if row else "",
        age=row.get("age") if row else "",
        profile_pic=row.get("profile_pic") if row else None,
        translations=translations,
        lang=lang
    )


def get_user_profile():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT bio, profile_pic FROM users WHERE username=%s", (session["username"],))
            row = cur.fetchone()
    finally:
        conn.close()

    return {"bio": row.get("bio"), "profile_pic": row.get("profile_pic")} if row else {"bio": "", "profile_pic": None}
