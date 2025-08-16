from flask import session, request, redirect, render_template
import os, shutil
from werkzeug.utils import secure_filename
from file_utils import normalize_filename, get_user_folder
from . import app

@app.route("/upload", methods=["POST"])
def upload():
    if "username" not in session:
        return redirect("/login")
    files = request.files.getlist("file")
    for file in files:
        if file and file.filename:
            filename = secure_filename(normalize_filename(file.filename))
            file.save(os.path.join(get_user_folder(), filename))
    return redirect("/dashboard")