from flask import redirect, session
import os, shutil
from . import app
from werkzeug.utils import secure_filename
from file_utils import normalize_filename, get_trash_folder

@app.route("/permadelete/<filename>")
def permadelete(filename):
    if "username" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    path = os.path.join(get_trash_folder(), normalize_filename(filename))
    if os.path.exists(path):
        os.remove(path)
    return redirect("/dashboard")