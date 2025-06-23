from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session, flash, jsonify, abort
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
import os, shutil, zipfile, sqlite3, uuid, unicodedata, mimetypes

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
app.permanent_session_lifetime = timedelta(days=7)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_BASE = os.path.join(BASE_DIR, "uploads")
TRASH_BASE = os.path.join(BASE_DIR, "trash")
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(UPLOAD_BASE, exist_ok=True)
os.makedirs(TRASH_BASE, exist_ok=True)

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
    if not os.path.exists(user_dir):
        return 0, 1024, 0
    for f in os.listdir(user_dir):
        total_bytes += os.path.getsize(os.path.join(user_dir, f))
    used_mb = round(total_bytes / (1024 * 1024), 2)
    max_mb = 4096
    percent = min(int((used_mb / max_mb) * 100), 100)
    max_mb = round(max_mb / 1024, 2)
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

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect("/login")

    lang = request.args.get("lang", "en")
    translations = get_translations(lang)

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    if request.method == "POST":
        bio = request.form.get("bio", "")
        age = request.form.get("age", "")
        remove_pic = request.form.get("remove_pic") == "on"
        profile_pic = request.files.get("profile_pic")

        filename = None
        if profile_pic and profile_pic.filename:
            filename = secure_filename(profile_pic.filename)
            profile_pic_path = os.path.join("static", "profiles", filename)
            os.makedirs(os.path.dirname(profile_pic_path), exist_ok=True)
            profile_pic.save(profile_pic_path)
            c.execute("UPDATE users SET bio=?, age=?, profile_pic=? WHERE username=?",
                      (bio, age, filename, session["username"]))
        else:
            c.execute("UPDATE users SET bio=?, age=? WHERE username=?",
                      (bio, age, session["username"]))

        if remove_pic:
            c.execute("SELECT profile_pic FROM users WHERE username=?", (session["username"],))
            current_pic = c.fetchone()[0]
            if current_pic:
                try:
                    os.remove(os.path.join("static", "profiles", current_pic))
                except FileNotFoundError:
                    pass
            c.execute("UPDATE users SET profile_pic=NULL WHERE username=?", (session["username"],))

        conn.commit()

    c.execute("SELECT bio, age, profile_pic FROM users WHERE username=?", (session["username"],))
    row = c.fetchone()
    conn.close()

    return render_template("profile.html", 
                         user=session["username"], 
                         bio=row[0], 
                         age=row[1], 
                         profile_pic=row[2],
                         translations=translations,
                         lang=lang)

def get_user_profile():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT bio, profile_pic FROM users WHERE username=?", (session["username"],))
    row = c.fetchone()
    conn.close()
    return {"bio": row[0], "profile_pic": row[1]} if row else {"bio": "", "profile_pic": None}

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
                           active_page="dashboard")


@app.route("/upload", methods=["POST"])
def upload():
    if "username" not in session:
        return redirect("/login")
    files = request.files.getlist("file")
    for file in files:
        if file and file.filename:
            filename = secure_filename(normalize_filename(file.filename))
            file.save(os.path.join(get_user_folder(), filename))
    return redirect("/dashboard")

@app.route("/download/<filename>")
def download_file(filename):
    if "username" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    path = os.path.join(get_user_folder(), safe_filename)
    if not os.path.exists(path):
        abort(404)
    # Serve text files as plain text for preview, otherwise as attachment
    ext = safe_filename.split('.')[-1].lower()
    as_attachment = not ext in ['txt', 'md', 'py', 'js', 'css', 'html']
    mimetype, _ = mimetypes.guess_type(path)
    if ext in ['txt', 'md', 'py', 'js', 'css', 'html']:
        return send_from_directory(get_user_folder(), safe_filename, as_attachment=False, mimetype=mimetype or 'text/plain')
    return send_from_directory(get_user_folder(), safe_filename, as_attachment=True)

@app.route("/trash/<filename>")
def download_trash_file(filename):
    if "username" not in session:
        return redirect("/login")
    return send_from_directory(get_trash_folder(), filename, as_attachment=True)

@app.route("/delete/<path:filename>")
def delete(filename):
    if "username" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    src = os.path.join(get_user_folder(), filename)
    dst = os.path.join(get_trash_folder(), filename)
    if os.path.exists(src):
        shutil.move(src, dst)
    return redirect("/dashboard")

@app.route("/restore/<filename>")
def restore(filename):
    if "username" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
    src = os.path.join(get_trash_folder(), normalize_filename(filename))
    dst = os.path.join(get_user_folder(), normalize_filename(filename))
    if os.path.exists(src):
        shutil.move(src, dst)
    return redirect("/dashboard")

@app.route("/permadelete/<filename>")
def permadelete(filename):
    if "username" not in session:
        return redirect("/login")
    safe_filename = secure_filename(normalize_filename(filename))
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

@app.route("/trash")
def trash():
    if "username" not in session:
        return redirect("/login")

    lang = request.args.get("lang", "en")
    translations = get_translations(lang)

    trashed = os.listdir(get_trash_folder())
    profile = get_user_profile()
    used_mb, max_mb, percent_used = get_storage_info()

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
                           active_page="trash")


def get_translations(lang):
    translations = {
        "select_all": {
            "en": "Select All",
            "ta": "அனைத்தையும் தேர்ந்தெடு",
            "hi": "सभी चुनें"
        },
        "delete_selected": {
            "en": "Delete Selected",
            "ta": "தேர்ந்தெடுத்தவற்றை நீக்கு",
            "hi": "चयनित हटाएँ"
        },
        "restore_selected": {
            "en": "Restore selected",
            "ta": "தேர்ந்தெடுக்கப்பட்டவை மீட்க",
            "hi": "चयनित बहाल करें"
        },
        "sort_by_name": {
            "en": "Sort by Name",
            "ta": "பெயரால் வரிசைப்படுத்து",
            "hi": "नाम से छाँटें"
        },
        "sort_by_date": {
            "en": "Sort by Date",
            "ta": "தேதியால் வரிசைப்படுத்து",
            "hi": "तारीख से छाँटें"
        },
        "sort_by_size": {
            "en": "Sort by Size",
            "ta": "அளவால் வரிசைப்படுத்து",
            "hi": "आकार से छाँटें"
        },
        "sort_by_type": {
            "en": "Sort by Type",
            "ta": "வகையால் வரிசைப்படுத்து",
            "hi": "प्रकार से छाँटें"
        },
        "search_files": {
            "en": "Search files...",
            "ta": "கோப்புகளை தேடு...",
            "hi": "फ़ाइलें खोजें..."
        },
        "my_drive": {"en": "My Drive", "ta": "எனது டிரைவ்", "hi": "मेरा ड्राइव"},
        "hello": {"en": "Hello", "ta": "வணக்கம்", "hi": "नमस्ते"},
        "logout": {"en": "Logout", "ta": "வெளியேறு", "hi": "लॉगआउट"},
        "storage": {"en": "Storage:", "ta": "ஸ்டோரேஜ்:", "hi": "स्टोरेज:"},
        "drop_here": {
            "en": "Drop files here or click to upload",
            "ta": "இங்கே கோப்புகளை இடுக அல்லது கிளிக் செய்யவும்",
            "hi": "फ़ाइलें यहाँ छोड़ें या अपलोड करने के लिए क्लिक करें"
        },
        "my_files": {"en": "My Files", "ta": "எனது கோப்புகள்", "hi": "मेरी फाइलें"},
        "download": {"en": "Download", "ta": "பதிவிறக்கு", "hi": "डाउनलोड"},
        "trash": {"en": "Trash", "ta": "அகற்றுக", "hi": "ट्रैश"},
        "share": {"en": "Share", "ta": "பகிர்", "hi": "साझा करें"},
        "no_files": {"en": "No files uploaded.", "ta": "எந்த கோப்புகளும் இல்லை.", "hi": "कोई फ़ाइल अपलोड नहीं की गई"},
        "download_selected": {"en": "Download Selected as ZIP", "ta": "ZIP ஆக பதிவிறக்கு", "hi": "चयनित ज़िप डाउनलोड करें"},
        "trash_bin": {"en": "Trash", "ta": "அகற்றியவை", "hi": "कचरा पात्र"},
        "restore": {"en": "Restore", "ta": "மீட்டமை", "hi": "पुनर्स्थापित"},
        "delete_forever": {"en": "Delete Permanently", "ta": "நிரந்தரமாக நீக்கு", "hi": "स्थायी रूप से हटाएं"},
        "used": {"en": "used", "ta": "பயன்பட்டது", "hi": "उपयोग किया गया"},
        "profile": {"en": "Profile", "ta": "சுயவிவரம்", "hi": "प्रोफ़ाइल"},
        "bio": {"en": "Bio", "ta": "வாழ்க்கை வரலாறு", "hi": "जीवनी"},
        "bio_placeholder": {"en": "Tell us something about you...", "ta": "உங்களைப் பற்றி எங்களிடம் சொல்லுங்கள்...", "hi": "हमें अपने बारे में बताएं..."},
        "age": {"en": "Age", "ta": "வயது", "hi": "उम्र"},
        "age_placeholder": {"en": "Your age", "ta": "உங்கள் வயது", "hi": "आपकी उम्र"},
        "profile_pic": {"en": "Profile Picture", "ta": "சுயவிவர படம்", "hi": "प्रोफ़ाइल चित्र"},
        "remove_pic": {"en": "Remove current profile picture", "ta": "தற்போதைய சுயவிவர படத்தை அகற்று", "hi": "वर्तमान प्रोफ़ाइल चित्र हटाएं"},
        "save_changes": {"en": "Save Changes", "ta": "மாற்றங்களை சேமிக்கவும்", "hi": "परिवर्तनों को सुरक्षित करें"},
        "back_to_dashboard": {"en": "Back to Dashboard", "ta": "டாஷ்போர்டுக்கு திரும்புக", "hi": "डैशबोर्ड पर वापस जाएं"},
    }
    return {key: val.get(lang, val["en"]) for key, val in translations.items()}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
