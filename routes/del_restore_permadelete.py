from flask import jsonify, session, request, redirect
from file_utils import get_storage_info, get_trash_folder, get_user_folder, normalize_filename
import os, shutil
from . import app
from werkzeug.utils import secure_filename

@app.route("/delete_selected", methods=["POST"])
def delete_selected():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    files = data.get("files", [])
    user_folder = get_user_folder()
    trash_folder = get_trash_folder()
    for filename in files:
        safe_filename = secure_filename(normalize_filename(filename))
        src = os.path.join(user_folder, safe_filename)
        dst = os.path.join(trash_folder, safe_filename)
        if os.path.exists(src):
            shutil.move(src, dst)
    return jsonify({"success": True})

@app.route("/permadelete_selected", methods=["POST"])
def permadelete_selected():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    files = data.get("files", [])
    trash_folder = get_trash_folder()
    for filename in files:
        safe_filename = secure_filename(normalize_filename(filename))
        file_path = os.path.join(trash_folder, safe_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    return jsonify({"success": True})

@app.route("/restore_selected", methods=["POST"])
def restore_selected():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    files = data.get("files", [])
    trash_folder = get_trash_folder()
    user_folder = get_user_folder()
    for filename in files:
        safe_filename = secure_filename(normalize_filename(filename))
        src = os.path.join(trash_folder, safe_filename)
        dst = os.path.join(user_folder, safe_filename)
        if os.path.exists(src):
            shutil.move(src, dst)
    return jsonify({"success": True})