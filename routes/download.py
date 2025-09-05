from flask import request, send_from_directory, redirect, session, abort
import os, mimetypes
from . import app
from werkzeug.utils import secure_filename
from file_utils import get_user_folder, normalize_filename

@app.route("/download/<filename>")
def download_file(filename):
    if "username" not in session or "user_id" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    path = os.path.join(get_user_folder(), safe_filename)
    if not os.path.exists(path):
        abort(404)
    ext = os.path.splitext(safe_filename)[-1].lower().lstrip(".")
    preview_exts = {"txt", "md", "py", "js", "css", "html"}
    mimetype, _ = mimetypes.guess_type(path)
    if ext in preview_exts:
        return send_from_directory(
            get_user_folder(),
            safe_filename,
            as_attachment=False,
            mimetype=mimetype or "text/plain"
        )
    return send_from_directory(
        get_user_folder(),
        safe_filename,
        as_attachment=True
    )
