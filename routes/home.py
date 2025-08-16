from flask import redirect
from . import app

@app.route("/")
def home():
    return redirect("/logo")

