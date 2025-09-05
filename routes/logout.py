from flask import session, redirect
from . import app

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
