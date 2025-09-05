from flask import redirect, session, url_for
from . import app
from werkzeug.utils import secure_filename
from file_utils import normalize_filename

@app.route("/share/<filename>")
def share(filename):
    if "username" not in session or "user_id" not in session:
        return redirect("/login")

    safe_filename = secure_filename(normalize_filename(filename))
    file_url = url_for("download_file", filename=safe_filename, _external=True)

    return (
        f"<h3>Share this link:</h3>"
        f"<a href='{file_url}'>{file_url}</a>"
        f"<br><br><a href='/dashboard'>⬅ Back</a>"
    )
