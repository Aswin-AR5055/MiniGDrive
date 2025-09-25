from flask import render_template, request, redirect, flash
from . import app
from db_schema import get_db_connection
from werkzeug.security import generate_password_hash

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        uname = request.form["username"]
        new_pass = request.form["new_password"]
        confirm_pass = request.form["confirm_password"]

        if new_pass != confirm_pass:
            flash("passwords doesn't match", "danger")
            return redirect("/reset_password")
    
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("select * from users where username=%s", (uname,))
        if not c.fetchone():
            conn.close()
            flash("User not found", "danger")
            return redirect("/reset_password")
        
        hashed = generate_password_hash(new_pass)
        c.execute("update users set password=%s where username=%s", (hashed, uname))
        conn.commit()
        conn.close()

        flash("Password reset successfull. Please login.", "success")
        return redirect("/login")

    return render_template("reset_password.html")