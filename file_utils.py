import unicodedata, os, shutil
from routes import UPLOAD_BASE, TRASH_BASE
from flask import session

def normalize_filename(name):
    return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')

def get_user_folder():
    return os.path.join(UPLOAD_BASE, session["username"])

def get_trash_folder():
    return os.path.join(TRASH_BASE, session["username"])

def get_storage_info():
    total_bytes = 0
    user_dir = get_user_folder()
    if not os.path.exists(user_dir):
        return 0, 1024, 0
    for f in os.listdir(user_dir):
        total_bytes += os.path.getsize(os.path.join(user_dir, f))
    used_mb = round(total_bytes / (1024 * 1024), 2)
    max_mb = 4096
    percent = min(int((used_mb / max_mb) * 100), 100)
    max_mb = round(max_mb / 1024, 2)
    return used_mb, max_mb, percent
