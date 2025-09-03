from flask import session, redirect, request, flash, render_template
from . import app, UPLOAD_BASE, TRASH_BASE
import os
from werkzeug.security import generate_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor

database_url = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect("/dashboard")
    
    if request.method == "POST":
        uname = request.form["username"]
        passwd = request.form["password"]

        conn = get_conn()
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=%s", (uname,))
        if c.fetchone():
            conn.close()
            flash("Username already taken", "danger")
            return redirect("/register")

        hashed = generate_password_hash(passwd)

        c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (uname, hashed))
        conn.commit()
        conn.close()

        os.makedirs(os.path.join(UPLOAD_BASE, uname), exist_ok=True)
        os.makedirs(os.path.join(TRASH_BASE, uname), exist_ok=True)

        flash("Account created. Please Login.", "success")
        return redirect("/login")
    
    return render_template("register.html")
