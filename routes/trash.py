from flask import render_template, session, request, redirect
import os
from . import app
from file_utils import get_storage_info, get_trash_folder
from .profile import get_user_profile
from translations import get_translations

@app.route("/trash")
def trash():
    if "username" not in session or "user_id" not in session:
        return redirect("/login")

    lang = request.args.get("lang", "en")
    translations = get_translations(lang)

    trashed = os.listdir(get_trash_folder())
    profile = get_user_profile()
    used_mb, max_mb, percent_used = get_storage_info()

    return render_template(
        "trash.html",
        user=session["username"],
        trashed=trashed,
        bio=profile.get("bio", ""),
        profile_pic=profile.get("profile_pic"),
        used_mb=used_mb,
        max_mb=max_mb,
        percent_used=percent_used,
        translations=translations,
        lang=lang,
        active_page="trash",
    )
