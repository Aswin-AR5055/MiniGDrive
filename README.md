<img src="assets/ars_logo_32x32.png" alt="ARS" width="24" height="24"> MiniGDrive          

MiniGDrive is a lightweight cloud storage application built using Flask and SQLite, designed to mimic the basic functionality of Google Drive. Users can register, log in, upload, download, and manage their files — all within a simple and secure environment.


---

📁 Table of Contents

Screenshots

Live Demo

Features

Tech Stack

Project Structure

How to Run Locally

Run with Docker

Deployment Pipeline

Security Notes

Acknowledgements



---

Screenshots

Dashboard (PC view):



Dashboard (Mobile view):

<img src="assets/dashboardmobile2.jpg" width="200"/> <img src="assets/dashboardmobile.jpg" width="200"/>


---

Live Demo

👉 

> ⚙️ Hosted live on an AWS EC2 instance using Docker & GitHub Actions CI/CD.
🔒 Note: This demo runs on plain HTTP and is intended for testing purposes only. Do not upload sensitive or personal data.




---

Features

User Registration and Login: Secure authentication with password hashing.

File Management: Upload, download, and delete files.

Trash System: Deleted files are moved to a trash folder for recovery.

Personal Storage Management: Monitor storage usage with a progress bar.

Session Management: Auto-expiry of sessions after 7 days.

Profile Customization: Update bio, age, and profile picture.



---

Tech Stack

Layer	Technology Used	Purpose

Backend	Python + Flask	Web server and application logic
Database	SQLite	Storing user accounts and profiles
Frontend	HTML (Flask templates), Bootstrap 5, Vanilla JavaScript	Responsive UI, modals, sorting/filtering, interactivity
Security	Werkzeug (secure filename + password hashing)	Secure file uploads and password management
File Handling	Python libraries (os, shutil, zipfile, uuid, unicodedata)	File operations (uploads, storage, trash)
Session Management	Flask + datetime	Managing user sessions (login duration)
Deployment	AWS EC2	Hosting the application
Containerization	Docker	Packaging and running the app
CI/CD	GitHub Actions	Automating tests and deployment



---

Project Structure

MiniGDrive/
│
├── .github/workflows/pytest-update-ec2.yml   # GitHub Actions workflow file
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
├── assets/               # Logo and Screenshots
├── app.py                # Main Flask application
├── users.db              # SQLite DB (created at runtime)
├── test_app.py           # Unit tests
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── logo.html
│   ├── profile.html
│   └── register.html
├── uploads/             # Uploaded files (generated)
├── trash/               # Trashed files (generated)
├── storage/             # User storage dir (generated)
└── static/              # Static assets (profile images, etc.)


---

How to Run Locally

1. Clone the repository:

git clone https://github.com/Aswin-AR5055/MiniGDrive.git
cd MiniGDrive


2. Install the dependencies (use a virtual environment):

pip install -r requirements.txt


3. Run the application:

python app.py

OR:

python3 app.py


4. Visit the application:

http://127.0.0.1:5000




---

Run with Docker

If you have Docker installed, you can run MiniGDrive without installing dependencies manually.

1. Clone the repository:

git clone https://github.com/Aswin-AR5055/MiniGDrive.git
cd MiniGDrive


2. Build the Docker image:

docker build -t minigdrive .


3. Run the container:

docker run -p 5000:5000 minigdrive


4. Access the application:

http://localhost:5000




---

🚀 Deployment Pipeline

Code pushed to master branch

GitHub Actions runs unit tests

SSH into AWS EC2 instance

Docker image is rebuilt using latest code

Existing container is stopped and removed

New container is started on port 80



---

Security Notes

Password Security: Passwords are hashed securely before being stored in the database using Werkzeug.

Session Management: Session tokens ensure users stay logged in securely for up to 7 days.

Important: For your safety, do not use your real personal email address or password when registering on this site. Use a secondary or disposable email, and a unique password that you do not use elsewhere.



---

Acknowledgements

Full Stack Development and DevOps by Aswin Raj A
Design Support by Mohamed Suhail S

Built with ❤️

