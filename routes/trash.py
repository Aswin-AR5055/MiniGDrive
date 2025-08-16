from flask import render_template, session, request, redirect
import os, shutil
from datetime import datetime, timezone
from . import app
from file_utils import get_storage_info, get_trash_folder, get_user_folder
from .profile import get_user_profile
from translations import get_translations

@app.route("/trash")
def trash():
    if "username" not in session:
        return redirect("/login")

    lang = request.args.get("lang", "en")
    translations = get_translations(lang)

    trashed = os.listdir(get_trash_folder())
    profile = get_user_profile()
    used_mb, max_mb, percent_used = get_storage_info()

    old_files = []
    threshold_days = 7
    now = datetime.now(timezone.utc)
    for f in trashed:
        try:
            path = os.path.join(get_trash_folder(), f)
            mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
            print(f"{f}: {(now - mtime).days} days old")
            if (now - mtime).days >= threshold_days:
                old_files.append(f)
        except Exception:
            pass


    return render_template("trash.html",
                           user=session["username"],
                           trashed=trashed,
                           bio=profile["bio"],
                           profile_pic=profile["profile_pic"],
                           used_mb=used_mb,
                           max_mb=max_mb,
                           percent_used=percent_used,
                           translations=translations,
                           lang=lang,
                           active_page="trash",
                           old_files=old_files)