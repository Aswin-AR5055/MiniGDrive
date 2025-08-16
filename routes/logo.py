from flask import session, render_template
from . import app

@app.route("/logo")
def logo():
    is_logged_in = "username" in session
    return render_template("logo.html", logged_in = is_logged_in)
