from flask import (
    Flask, render_template, request, redirect,
    send_from_directory, url_for, session, flash
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os
import shutil
import zipfile
import sqlite3
import uuid
import unicodedata


app = Flask(__name__)
app.secret_key = "supersecretkey"
app.permanent_session_lifetime = timedelta(days=7)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_BASE = os.path.join(BASE_DIR, "uploads")
TRASH_BASE = os.path.join(BASE_DIR, "trash")
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)


def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            bio TEXT,
            age INTEGER,
            profile_pic TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


def normalize_filename(name):
    return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')


def get_user_folder():
    return os.path.join(UPLOAD_BASE, session["username"])


def get_trash_folder():
    return os.path.join(TRASH_BASE, session["username"])


def get_storage_info():
    total_bytes = 0
    user_dir = get_user_folder()
    for f in os.listdir(user_dir):
        total_bytes += os.path.getsize(os.path.join(user_dir, f))
    used_mb = round(total_bytes / (1024 * 1024), 2)
    max_mb = 1024
    percent = min(int((used_mb / max_mb) * 100), 100)
    return used_mb, max_mb, percent


@app.route("/")
def home():
    return redirect("/logo")


@app.route("/logo")
def logo():
    is_logged_in = "username" in session
    return render_template("logo.html", logged_in=is_logged_in)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form["username"]
        passwd = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (uname,))
        if c.fetchone():
            conn.close()
            flash("Username already taken", "danger")
            return redirect("/register")

        hashed = generate_password_hash(passwd)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, hashed))
        conn.commit()
        conn.close()

        os.makedirs(os.path.join(UPLOAD_BASE, uname), exist_ok=True)
        os.makedirs(os.path.join(TRASH_BASE, uname), exist_ok=True)
        flash("Account created. Please log in.", "success")
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        passwd = request.form["password"]
        remember = request.form.get("remember")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (uname,))
        row = c.fetchone()
        conn.close()

        if row and check_password_hash(row[0], passwd):
            session["username"] = uname
            session.permanent = True if remember else False
            return redirect("/dashboard")

        flash("Invalid credentials", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")


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

    files = os.listdir(upload_folder)
    trashed = os.listdir(trash_folder)
    used_mb, max_mb, percent_used = get_storage_info()
    profile = get_user_profile()

    return render_template(
        "index.html",
        user=session["username"],
        files=files,
        trashed=trashed,
        used_mb=used_mb,
        max_mb=max_mb,
        percent_used=percent_used,
        translations=translations,
        lang=lang,
        bio=profile["bio"],
        profile_pic=profile["profile_pic"]
    )


@app.route("/upload", methods=["POST"])
def upload():
    if "username" not in session:
        return redirect("/login")
    file = request.files["file"]
    if file and file.filename:
        filename = secure_filename(normalize_filename(file.filename))
        file.save(os.path.join(get_user_folder(), filename))
    return redirect("/dashboard")


@app.route("/download/<filename>")
def download_file(filename):
    if "username" not in session:
        return redirect("/login")
    return send_from_directory(get_user_folder(), filename, as_attachment=True)


@app.route("/trash/<filename>")
def download_trash_file(filename):
    if "username" not in session:
        return redirect("/login")
    return send_from_directory(get_trash_folder(), filename, as_attachment=True)


@app.route("/delete/<path:filename>")
def delete(filename):
    if "username" not in session:
        return redirect("/login")
    src = os.path.join(get_user_folder(), filename)
    dst = os.path.join(get_trash_folder(), filename)
    if os.path.exists(src):
        shutil.move(src, dst)
    return redirect("/dashboard")


@app.route("/restore/<filename>")
def restore(filename):
    if "username" not in session:
        return redirect("/login")
    src = os.path.join(get_trash_folder(), normalize_filename(filename))
    dst = os.path.join(get_user_folder(), normalize_filename(filename))
    if os.path.exists(src):
        shutil.move(src, dst)
    return redirect("/dashboard")


@app.route("/permadelete/<filename>")
def permadelete(filename):
    if "username" not in session:
        return redirect("/login")
    path = os.path.join(get_trash_folder(), normalize_filename(filename))
    if os.path.exists(path):
        os.remove(path)
    return redirect("/dashboard")


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


@app.route("/share/<filename>")
def share(filename):
    if "username" not in session:
        return redirect("/login")
    file_url = url_for("download_file", filename=filename, _external=True)
    return f"<h3>Share this link:</h3><a href='{file_url}'>{file_url}</a><br><br><a href='/dashboard'>⬅ Back</a>"


def get_user_profile():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT bio, profile_pic FROM users WHERE username=?", (session["username"],))
    row = c.fetchone()
    conn.close()
    return {"bio": row[0], "profile_pic": row[1]} if row else {"bio": "", "profile_pic": None}


def get_translations(lang):
    translations = {
        "hello": {"en": "Hello", "ta": "வணக்கம்", "hi": "नमस्ते"},
        "logout": {"en": "Logout", "ta": "வெளியேறு", "hi": "लॉगआउट"},
        "storage": {"en": "Storage:", "ta": "சேமிப்பு:", "hi": "स्टोरेज:"},
        "drop_here": {
            "en": "Drop files here or click to upload",
            "ta": "கோப்புகளை இங்கே விடுக அல்லது கிளிக் செய்யவும்",
            "hi": "फ़ाइलें यहाँ छोड़ें या अपलोड करने के लिए क्लिक करें"
        },
        "my_files": {"en": "My Files", "ta": "எனது கோப்புகள்", "hi": "मेरी फाइलें"},
        "download": {"en": "Download", "ta": "பதிவிறக்கு", "hi": "डाउनलोड"},
        "trash": {"en": "Trash", "ta": "அகற்றுக", "hi": "ट्रैश"},
        "share": {"en": "Share", "ta": "பகிர்", "hi": "साझा करें"},
        "no_files": {"en": "No files uploaded.", "ta": "எந்த கோப்புகளும் இல்லை.", "hi": "कोई फ़ाइल अपलोड नहीं की गई है।"},
        "download_selected": {"en": "Download Selected as ZIP", "ta": "ZIP ஆக பதிவிறக்கு", "hi": "चयनित ज़िप डाउनलोड करें"},
        "trash_bin": {"en": "Trash", "ta": "அகற்றியவை", "hi": "कचरा पात्र"},
        "restore": {"en": "Restore", "ta": "மீட்டமை", "hi": "पुनर्स्थापित"},
        "delete_forever": {"en": "Delete Permanently", "ta": "நிரந்தரமாக நீக்கு", "hi": "स्थायी रूप से हटाएं"},
        "used": {"en": "used", "ta": "பயன்பட்டது", "hi": "उपयोग किया गया"},
        "profile": {"en": "Profile", "ta": "சுயவிவரம்", "hi": "प्रोफ़ाइल"},
        "bio": {"en": "Bio", "ta": "வாழ்க்கை வரலாறு", "hi": "जीवनी"},
        "bio_placeholder": {"en": "Tell us something about you...", "ta": "உங்களைப் பற்றி எங்களிடம் சொல்லுங்கள்...", "hi": "हमें अपने बारे में कुछ बताएं..."},
        "age": {"en": "Age", "ta": "வயது", "hi": "उम्र"},
        "age_placeholder": {"en": "Your age", "ta": "உங்கள் வயது", "hi": "आपकी उम्र"},
        "profile_pic": {"en": "Profile Picture", "ta": "சுயவிவர படம்", "hi": "प्रोफ़ाइल चित्र"},
        "remove_pic": {"en": "Remove current profile picture", "ta": "தற்போதைய சுயவிவர படத்தை அகற்று", "hi": "वर्तमान प्रोफ़ाइल चित्र हटाएं"},
        "save_changes": {"en": "Save Changes", "ta": "மாற்றங்களை சேமிக்கவும்", "hi": "परिवर्तनों को सुरक्षित करें"},
        "back_to_dashboard": {"en": "Back to Dashboard", "ta": "டாஷ்போர்டுக்கு திரும்புக", "hi": "डैशबोर्ड पर वापस जाएं"}
    }
    return {key: val.get(lang, val["en"]) for key, val in translations.items()}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)