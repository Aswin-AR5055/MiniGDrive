# MiniGDrive

MiniGDrive is a lightweight cloud storage application built using Flask and SQLite, designed to mimic the basic functionality of Google Drive. Users can register, log in, upload, download, and manage their files — all within a simple and secure environment.

---

## 🚀 Features

- **User Registration and Login**: Secure authentication with password hashing.
- **File Management**: Upload, download, and delete files.
- **Trash System**: Deleted files are moved to a trash folder for recovery.
- **Personal Storage Management**: Monitor storage usage with a progress bar.
- **Session Management**: Auto-expiry of sessions after 7 days.
- **Profile Customization**: Update bio, age, and profile picture.

---

## 🛠️ Tech Stack

| Layer               | Technology Used                     | Purpose                                      |
|---------------------|-------------------------------------|----------------------------------------------|
| **Backend**         | Python + Flask                     | Web server and application logic             |
| **Database**        | SQLite                             | Storing user accounts and profiles           |
| **Frontend**        | HTML (Flask templates)             | User interface rendering                     |
| **Security**        | Werkzeug (secure filename + password hashing) | Secure file uploads and password management |
| **File Handling**   | Python libraries (`os`, `shutil`, `zipfile`, `uuid`, `unicodedata`) | File operations (uploads, storage, trash)   |
| **Session Management** | Flask + `datetime`               | Managing user sessions (login duration)      |

---

## 📂 Project Structure

```plaintext
MiniGDrive/
│
├── app.py                # Main Flask application
├── users.db              # SQLite Database file
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── logo.html
│   ├── profile.html
│   └── register.html
├── uploads/              # Folder for uploaded files (created dynamically)
├── trash/                # Folder for trashed files (created dynamically)
├── storage/              # Main storage directory (created dynamically)
└── static/               # Static files (e.g., profile pictures)
```

---

## ⚙️ How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aswin-AR5055/MiniGDrive.git
   cd MiniGDrive
   ```

2. **Install the dependencies**:
   ```bash
   pip install flask werkzeug
   ```
   Or use the requirements.txt file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1/
   ```

---

## 🔒 Security Notes

- **Password Security**: Passwords are hashed securely before being stored in the database using Werkzeug.
- **Session Management**: Session tokens ensure users stay logged in securely for up to 7 days.

---

## 🙏 Acknowledgements

Built with ❤️ by [Aswin Raj](https://github.com/Aswin-AR5055).
