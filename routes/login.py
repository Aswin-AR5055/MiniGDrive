from flask import render_template, flash, session, redirect, request
from . import app
import sqlite3
from werkzeug.security import check_password_hash

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/dashboard")
    
    if request.method == "POST":
        uname = request.form["username"]
        passwd = request.form["password"]
        remember = request.form.get("remember")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("select password from users where username=?", (uname,))
        row = c.fetchone()
        conn.close()

        if row and check_password_hash(row[0], passwd):
            session["username"] = uname
            session.permanent = True if remember else False
            return redirect("/dashboard")
    
        flash("invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")