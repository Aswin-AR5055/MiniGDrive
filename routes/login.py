from flask import render_template, flash, session, redirect, request
from . import app
from db import get_connection
from werkzeug.security import check_password_hash
from psycopg2.extras import RealDictCursor

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/dashboard")
    
    if request.method == "POST":
        uname = request.form.get("username", "").strip()
        passwd = request.form.get("password", "")
        remember = request.form.get("remember")

        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT password FROM users WHERE username=%s", (uname,))
                row = cur.fetchone()
        finally:
            conn.close()

        if row and check_password_hash(row['password'], passwd):
            session["username"] = uname
            session.permanent = bool(remember)
            return redirect("/dashboard")
        
        flash("Invalid credentials", "danger")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")
