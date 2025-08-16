from flask import session, redirect, request, flash, render_template
from . import app, UPLOAD_BASE, TRASH_BASE
import sqlite3
import os, shutil
from werkzeug.security import generate_password_hash


@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect("/dashboard")
    
    if request.method == "POST":
        uname = request.form["username"]
        passwd = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("select * from users where username=?", (uname,))
        if c.fetchone():
            conn.close()
            flash("Username already taken", "danger")
            return redirect("/register")
        hashed = generate_password_hash(passwd)
        c.execute("insert into users (username, password) values (?, ?)", (uname, hashed))
        conn.commit()
        conn.close()

        os.makedirs(os.path.join(UPLOAD_BASE, uname), exist_ok=True)
        os.makedirs(os.path.join(TRASH_BASE, uname), exist_ok=True)
        flash("Account created. Please Login.", "success")
        return redirect("/login")
    
    return render_template("register.html")