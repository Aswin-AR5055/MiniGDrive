from flask import session, redirect, request, flash, render_template
from . import app, UPLOAD_BASE, TRASH_BASE
from db import get_connection
import os
from werkzeug.security import generate_password_hash

@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session and "user_id" in session:
        return redirect("/dashboard")
    
    if request.method == "POST":
        uname = request.form.get("username", "").strip().lower()
        passwd = request.form.get("password", "").strip()

        if not uname or not passwd:
            flash("Username and password are required.", "danger")
            return redirect("/register")

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM users WHERE username=%s", (uname,))
                if cur.fetchone():
                    flash("Username already taken.", "danger")
                    return redirect("/register")
                
                hashed = generate_password_hash(passwd)
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
                    (uname, hashed)
                )
                user_id = cur.fetchone()[0]
                conn.commit()
        finally:
            conn.close()

        try:
            os.makedirs(os.path.join(UPLOAD_BASE, uname), exist_ok=True)
            os.makedirs(os.path.join(TRASH_BASE, uname), exist_ok=True)
        except Exception as e:
            flash(f"Failed to create user directories: {e}", "warning")

        flash("Account created successfully. Please login.", "success")
        return redirect("/login")
    
    return render_template("register.html")
