from flask import redirect, session, url_for
from . import app

@app.route("/share/<filename>")
def share(filename):
    if "username" not in session:
        return redirect("/login")
    file_url = url_for("download_file", filename=filename, _external=True)
    return f"<h3>Share this link:</h3><a href='{file_url}'>{file_url}</a><br><br><a href='/dashboard'>⬅ Back</a>"