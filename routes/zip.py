from flask import send_from_directory, session, request, redirect
import os, zipfile, uuid
from . import app, STORAGE_DIR
from file_utils import get_user_folder, normalize_filename
from werkzeug.utils import secure_filename

@app.route("/download_zip", methods=["POST"])
def download_zip():
    if "username" not in session or "user_id" not in session:
        return redirect("/login")

    files = request.form.getlist("selected_files")
    if not files:
        return redirect("/dashboard")

    zip_name = f"{uuid.uuid4().hex}.zip"
    zip_path = os.path.join(STORAGE_DIR, zip_name)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for f in files:
            safe_name = secure_filename(normalize_filename(f))
            file_path = os.path.join(get_user_folder(), safe_name)
            if os.path.exists(file_path):
                zipf.write(file_path, arcname=safe_name)

    # TODO: optionally schedule cleanup of old zips in STORAGE_DIR
    return send_from_directory(STORAGE_DIR, zip_name, as_attachment=True)
