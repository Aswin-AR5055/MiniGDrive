MiniGDrive 📁✨
MiniGDrive is a lightweight cloud storage application built using Flask and SQLite, designed to mimic the basic functionality of Google Drive. Users can register, log in, upload, download, and manage their files — all within a simple and secure environment.

🚀 Features
User Registration and Login (with password hashing)

Upload, Download, and Delete files

Personal Storage management

Trash system (deleted files are moved to trash)

Session management (auto-expiry after a week)

Profile customization (Bio, Age, Profile Picture)

🛠️ Tech Stack

Layer	Technology Used	Purpose
Backend	Python + Flask	Web server and application logic
Database	SQLite	Storing user accounts and profiles
Frontend	HTML (Flask templates)	User interface rendering
Security	Werkzeug (secure filename + password hashing)	Secure file uploads and password management
File Handling	Python libraries (os, shutil, zipfile, uuid, unicodedata)	File operations (uploads, storage, trash)
Session Management	Flask + datetime	Managing user sessions (login duration)
📂 Project Structure
bash
Copy
Edit
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
⚙️ How to Run Locally
Clone the repository


git clone https://github.com/Aswin-AR5055/MiniGDrive.git

cd MiniGDrive

Install the dependencies
pip install flask werkzeug

Run the application
python app.py

Access it in your browser
http://127.0.0.1:5000/

🔒 Security Notes
Passwords are hashed securely before being stored in the database using Werkzeug.

Session tokens ensure users stay logged in securely for up to 7 days.

🙏 Acknowledgements
Built with ❤️ by Aswin Raj (@Aswin-AR5055)
