from flask import request, send_from_directory, redirect, session, render_template, abort
import os, shutil, mimetypes
from . import app
from werkzeug.utils import secure_filename
from file_utils import get_storage_info, get_trash_folder, get_user_folder, normalize_filename


@app.route("/download/<filename>")
def download_file(filename):
    if "username" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    path = os.path.join(get_user_folder(), safe_filename)
    if not os.path.exists(path):
        abort(404)
    # Serve text files as plain text for preview, otherwise as attachment
    ext = safe_filename.split('.')[-1].lower()
    as_attachment = not ext in ['txt', 'md', 'py', 'js', 'css', 'html']
    mimetype, _ = mimetypes.guess_type(path)
    if ext in ['txt', 'md', 'py', 'js', 'css', 'html']:
        return send_from_directory(get_user_folder(), safe_filename, as_attachment=False, mimetype=mimetype or 'text/plain')
    return send_from_directory(get_user_folder(), safe_filename, as_attachment=True)