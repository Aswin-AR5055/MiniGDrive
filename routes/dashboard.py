from flask import render_template, session, redirect, request
import os, shutil, datetime
from file_utils import get_user_folder, get_trash_folder, get_storage_info
from .profile import get_user_profile
from translations import get_translations
from .favourites import get_user_favourites
from . import app

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    lang = request.args.get("lang", "en")
    translations = get_translations(lang)

    upload_folder = get_user_folder()
    trash_folder = get_trash_folder()
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(trash_folder, exist_ok=True)

    all_files = os.listdir(upload_folder)
    trashed = os.listdir(trash_folder)
    files = [f for f in all_files if f not in trashed]

    used_mb, max_mb, percent_used = get_storage_info()
    profile = get_user_profile()

    file_dates = {}
    file_sizes = {}
    for f in files:
        try:
            path = os.path.join(upload_folder, f)
            file_dates[f] = datetime.utcfromtimestamp(os.path.getmtime(path)).isoformat()
            file_sizes[f] = os.path.getsize(path)
        except Exception:
            file_dates[f] = ""
            file_sizes[f] = 0

    favourites = get_user_favourites()

    return render_template("index.html",
                           user=session["username"],
                           files=files,
                           used_mb=used_mb,
                           max_mb=max_mb,
                           percent_used=percent_used,
                           translations=translations,
                           lang=lang,
                           bio=profile["bio"],
                           profile_pic=profile["profile_pic"],
                           file_dates=file_dates,
                           file_sizes=file_sizes,
                           trashed=trashed,
                           favourites=favourites,
                           active_page="dashboard")

