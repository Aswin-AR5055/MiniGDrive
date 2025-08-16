from flask import send_from_directory, session, request, redirect
import os, shutil, zipfile, uuid
from . import app, STORAGE_DIR
from file_utils import get_user_folder, normalize_filename

@app.route("/download_zip", methods=["POST"])
def download_zip():
    if "username" not in session:
        return redirect("/login")
    files = request.form.getlist("selected_files")
    if not files:
        return redirect("/dashboard")
    zip_name = f"{uuid.uuid4().hex}.zip"
    zip_path = os.path.join(STORAGE_DIR, zip_name)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for f in files:
            file_path = os.path.join(get_user_folder(), normalize_filename(f))
            if os.path.exists(file_path):
                zipf.write(file_path, arcname=f)
    return send_from_directory(STORAGE_DIR, zip_name, as_attachment=True)