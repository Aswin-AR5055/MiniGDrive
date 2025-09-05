from flask import send_from_directory, session, redirect
from file_utils import normalize_filename, get_trash_folder, get_user_folder
import os, shutil
from . import app
from werkzeug.utils import secure_filename

@app.route("/trash/<filename>")
def download_trash_file(filename):
    if "username" not in session or "user_id" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    return send_from_directory(get_trash_folder(), safe_filename, as_attachment=True)


@app.route("/delete/<filename>")
def delete(filename):
    if "username" not in session or "user_id" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    src = os.path.join(get_user_folder(), safe_filename)
    dst = os.path.join(get_trash_folder(), safe_filename)
    if os.path.exists(src):
        shutil.move(src, dst)
    return redirect("/dashboard")


@app.route("/restore/<filename>")
def restore(filename):
    if "username" not in session or "user_id" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    src = os.path.join(get_trash_folder(), safe_filename)
    dst = os.path.join(get_user_folder(), safe_filename)
    if os.path.exists(src):
        shutil.move(src, dst)
    return redirect("/dashboard")
