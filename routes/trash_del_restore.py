from flask import send_from_directory, session, request, redirect, render_template
from file_utils import normalize_filename, get_storage_info, get_trash_folder, get_user_folder
import os, shutil
from . import app
from werkzeug.utils import secure_filename

@app.route("/trash/<filename>")
def download_trash_file(filename):
    if "username" not in session:
        return redirect("/login")
    return send_from_directory(get_trash_folder(), filename, as_attachment=True)

@app.route("/delete/<path:filename>")
def delete(filename):
    if "username" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    src = os.path.join(get_user_folder(), filename)
    dst = os.path.join(get_trash_folder(), filename)
    if os.path.exists(src):
        shutil.move(src, dst)
    return redirect("/dashboard")

@app.route("/restore/<filename>")
def restore(filename):
    if "username" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    src = os.path.join(get_trash_folder(), normalize_filename(filename))
    dst = os.path.join(get_user_folder(), normalize_filename(filename))
    if os.path.exists(src):
        shutil.move(src, dst)
    return redirect("/dashboard")