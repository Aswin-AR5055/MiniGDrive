from flask import session, request, redirect, flash
import os
from werkzeug.utils import secure_filename
from file_utils import normalize_filename, get_user_folder
from . import app

@app.route("/upload", methods=["POST"])
def upload():
    if "username" not in session or "user_id" not in session:
        return redirect("/login")

    files = request.files.getlist("file")
    user_folder = get_user_folder()
    os.makedirs(user_folder, exist_ok=True)

    for file in files:
        if file and file.filename:
            filename = secure_filename(normalize_filename(file.filename))
            save_path = os.path.join(user_folder, filename)

            # Prevent overwriting existing files
            if os.path.exists(save_path):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(save_path):
                    filename = f"{base}_{counter}{ext}"
                    save_path = os.path.join(user_folder, filename)
                    counter += 1

            try:
                file.save(save_path)
            except Exception as e:
                flash(f"Failed to upload {file.filename}: {e}", "danger")

    return redirect("/dashboard")
