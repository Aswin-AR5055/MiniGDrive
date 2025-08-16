from flask import request, redirect, render_template, session, flash
from . import app
from translations import get_translations
import sqlite3, os, shutil
from werkzeug.utils import secure_filename

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect("/login")

    lang = request.args.get("lang", "en")
    translations = get_translations(lang)

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    if request.method == "POST":
        bio = request.form.get("bio", "")
        age = request.form.get("age", "")
        remove_pic = request.form.get("remove_pic") == "on"
        profile_pic = request.files.get("profile_pic")

        filename = None
        if profile_pic and profile_pic.filename:
            filename = secure_filename(profile_pic.filename)
            profile_pic_path = os.path.join("static", "profiles", filename)
            os.makedirs(os.path.dirname(profile_pic_path), exist_ok=True)
            profile_pic.save(profile_pic_path)
            c.execute("UPDATE users SET bio=?, age=?, profile_pic=? WHERE username=?",
                      (bio, age, filename, session["username"]))
        else:
            c.execute("UPDATE users SET bio=?, age=? WHERE username=?",
                      (bio, age, session["username"]))

        if remove_pic:
            c.execute("SELECT profile_pic FROM users WHERE username=?", (session["username"],))
            current_pic = c.fetchone()[0]
            if current_pic:
                try:
                    os.remove(os.path.join("static", "profiles", current_pic))
                except FileNotFoundError:
                    pass
            c.execute("UPDATE users SET profile_pic=NULL WHERE username=?", (session["username"],))

        conn.commit()

    c.execute("SELECT bio, age, profile_pic FROM users WHERE username=?", (session["username"],))
    row = c.fetchone()
    conn.close()

    return render_template("profile.html", 
                         user=session["username"], 
                         bio=row[0], 
                         age=row[1], 
                         profile_pic=row[2],
                         translations=translations,
                         lang=lang)

def get_user_profile():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT bio, profile_pic FROM users WHERE username=?", (session["username"],))
    row = c.fetchone()
    conn.close()
    return {"bio": row[0], "profile_pic": row[1]} if row else {"bio": "", "profile_pic": None}
