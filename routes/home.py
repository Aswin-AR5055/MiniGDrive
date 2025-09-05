from flask import redirect, session
from . import app

@app.route("/")
def home():
    if "username" in session and "user_id" in session:
        return redirect("/dashboard")
    return redirect("/logo")
