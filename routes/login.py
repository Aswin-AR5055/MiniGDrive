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
        uname = request.form["username"]
        passwd = request.form["password"]
        remember = request.form.get("remember")

        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("select password from users where username=%s", (uname,))
        row = cur.fetchone()
        conn.close()

        if row and check_password_hash(row['password'], passwd):
            session["username"] = uname
            session.permanent = True if remember else False
            return redirect("/dashboard")
    
        flash("invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")