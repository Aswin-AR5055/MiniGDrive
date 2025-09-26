from flask import request, redirect, render_template, session
from . import app
from translations import get_translations
import os
from db_schema import get_db_connection
from werkzeug.utils import secure_filename

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect("/login")

    lang = request.args.get("lang", "en")
    translations = get_translations(lang)

    conn = get_db_connection()
    c = conn.cursor()

    if request.method == "POST":
        bio = request.form.get("bio", "").strip()
        age = request.form.get("age", "")
        try:
            age = int(age) if age else None
        except ValueError:
            age = None

        remove_pic = request.form.get("remove_pic") == "on"
        profile_pic = request.files.get("profile_pic")

        if profile_pic and profile_pic.filename:
            filename = secure_filename(profile_pic.filename)
            profile_pic_dir = os.path.join(app.static_folder, "profiles")
            os.makedirs(profile_pic_dir, exist_ok=True)
            profile_pic_path = os.path.join(profile_pic_dir, filename)
            profile_pic.save(profile_pic_path)

            c.execute(
                "UPDATE users SET bio=%s, age=%s, profile_pic=%s WHERE username=%s",
                (bio, age, filename, session["username"])
            )
        else:
            c.execute(
                "UPDATE users SET bio=%s, age=%s WHERE username=%s",
                (bio, age, session["username"])
            )

        if remove_pic:
            c.execute("SELECT profile_pic FROM users WHERE username=%s", (session["username"],))
            current_pic = c.fetchone()[0]
            if current_pic:
                try:
                    os.remove(os.path.join(app.static_folder, "profiles", current_pic))
                except FileNotFoundError:
                    pass
            c.execute("UPDATE users SET profile_pic=NULL WHERE username=%s", (session["username"],))

        conn.commit()

    c.execute("SELECT bio, age, profile_pic FROM users WHERE username=%s", (session["username"],))
    row = c.fetchone()
    conn.close()

    return render_template(
        "profile.html",
        user=session["username"],
        bio=row[0] if row else "",
        age=row[1] if row else None,
        profile_pic=row[2] if row else None,
        translations=translations,
        lang=lang
    )


def get_user_profile():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT bio, profile_pic FROM users WHERE username=%s", (session["username"],))
    row = c.fetchone()
    conn.close()
    return {"bio": row[0], "profile_pic": row[1]} if row else {"bio": "", "profile_pic": None}