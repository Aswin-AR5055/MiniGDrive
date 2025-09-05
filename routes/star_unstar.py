from flask import session, jsonify
from . import app
from .favourites import add_favourite, remove_favourite
from werkzeug.utils import secure_filename
from file_utils import normalize_filename

@app.route('/star/<filename>', methods=['POST'])
def star_file(filename):
    if "username" not in session or "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    safe_filename = secure_filename(normalize_filename(filename))
    try:
        add_favourite(safe_filename)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/unstar/<filename>', methods=['POST'])
def unstar_file(filename):
    if "username" not in session or "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    safe_filename = secure_filename(normalize_filename(filename))
    try:
        remove_favourite(safe_filename)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
