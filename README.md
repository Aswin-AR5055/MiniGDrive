# <img src="assets/ars_logo_32x32.png" alt="ARS" width="24" height="24"> MiniGDrive          

![Deploy](https://github.com/Aswin-AR5055/MiniGDrive/actions/workflows/pytest-update-ec2.yml/badge.svg)

![Status](https://img.shields.io/badge/status-completed-green)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**MiniGDrive** is a lightweight, responsive cloud storage application powered by Flask + SQLite, now with voice command support. Users can register, log in, upload, download, and manage files — all within a clean and intuitive UI.

---

## 📑 Table of Contents

- [Screenshots](#screenshots)
- [Live Demo](#live-demo)
- [Features](#features)
- [ER Diagram](#entity-relationshiper-diagram)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Voice Commands Supported](#voice-commands-supported)
- [How to Run Locally](#how-to-run-locally)
- [Run with Docker](#run-with-docker)
- [Deployment Pipeline](#deployment-pipeline)
- [Infrastructure Setup](#infrastructure-setup)
- [Security Notes](#security-notes)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Screenshots

Dashboard (PC view):

![Dashboard](assets/dashboard.png)

Dashboard (Mobile view):

<img src="assets/dashboardmobile2.jpg" width="200"/> 
<img src="assets/dashboardmobile.jpg" width="200"/>

---

## Live Demo

[![Live Demo](https://img.shields.io/badge/Live%20Demo-CLICK%20HERE-blue)](https://d2r6fbb0wu8aqt.cloudfront.net)
> **Hosted:** AWS EC2 instance using Docker, Gunicorn, and Nginx 
> **Secured via:** CloudFront CDN (HTTPS)  
> **Note:** This is a demo site. Please avoid uploading sensitive or personal data.  
> **Disclaimer:** I am not responsible for any data theft, loss, or misuse.

---

## Features

- **Voice Command Support**: 
Use browser-based voice commands, hands-free interaction powered by Web Speech API.
- **User Registration and Login**: Secure authentication with password hashing.
- **File Upload and Download**: Users can upload and download files easily.
- **Trash System**: Deleted files go to trash instead of being permanently removed.
- **Restore and Permanent Delete**: Restore files from trash or delete them forever.
- **Bulk Actions**: Select multiple files to delete, restore, or download as ZIP.
- **Star Files as Favourites**: Mark important files with a star to easily access and manage your favourite files in a dedicated Favourites page.
- **Optimized Static Delivery**: Static files and user profile pictures are served directly via Nginx for faster performance. - **Result**: Static assets now load almost instantly compared to Flask serving.
- **Storage Monitoring**: View used storage with a visual progress bar.
- **Responsive UI**: Works well on both desktop and mobile screens.
- **Profile Customization**: Add bio, age, and profile picture.
- **Multilingual Support**: UI available in English, Tamil, and Hindi.

---

## Entity Relationship(ER) Diagram

<div align="center">
  <img src="assets/ER%20Diagram.svg" alt="ER Diagram" width="250"/>
</div>

---

## Tech Stack

| Layer                  | Technology Used                                                   | Purpose                                               |
|------------------------|-------------------------------------------------------------------|-------------------------------------------------------|
| **Backend**            | Python + Flask                                                    |Application logic                      |
| **Database**           | SQLite                                                            | Storing user accounts, favourite files and profiles                    |
| **Frontend**           | HTML (Flask templates), Bootstrap 5, Vanilla JavaScript, Web Speech API | Responsive UI, modals, voice commands, sorting/filtering, interactivity |
| **Security**           | Werkzeug (secure filename + password hashing)                     | Secure file uploads and password management           |
| **File Handling**      | Python libraries (`os`, `shutil`, `zipfile`, `uuid`, `unicodedata`)| File operations (uploads, storage, trash)             |
| **Session Management** | Flask + `datetime`                                                | Managing user sessions (login duration)               |
| **Application Server** | Gunicorn                                                          | WSGI server for running the Flask app                 |
| **Web Server / Proxy** | Nginx                                                             | Reverse proxy, Serve static files   |
| **Hosting**            | AWS EC2                                                           | Server for running the app                            |
| **HTTPS/CDN**          | AWS CloudFront                                                    | Secure global access over HTTPS with CDN caching      |
| **Containerization**   | Docker                                                            | Packaging and running the app                         |
| **CI/CD**              | GitHub Actions                                                    | Automating tests and deployment                       |

---

## Project Structure

```plaintext
MiniGDrive/
│
├── .github/
│   └── workflows/pytest-update-ec2.yml        # GitHub Actions workflows
├── app.py               # Main Flask application
├── db_schema.py         # Database schema definitions
├── file_utils.py        # File handling utilities
├── translations.py      # Internationalization support
├── test_app.py          # Unit tests
├── users.db             # SQLite database (created at runtime)
├── routes/              # Route handlers
│   ├── __init__.py
│   ├── dashboard.py
│   ├── del_restore_permadelete.py
│   ├── download.py
│   ├── favourites.py
│   ├── home.py
│   ├── login.py
│   ├── logo.py
│   ├── permadelete.py
│   ├── profile.py
│   ├── register.py
│   ├── share.py
│   ├── star_unstar.py
│   ├── trash_del_restore.py
│   ├── trash.py
│   ├── upload.py
│   └── zip.py
├── static/             # Static assets
│   ├── script.js
│   ├── style.css
│   ├── voicecommands.js
    └── profiles/        #
    User profile pictures(Generated Dynamically) 
├── templates/           # HTML templates
│   ├── favourites.html
│   ├── index.html
│   ├── login.html
│   ├── logo.html
│   ├── profile.html
│   ├── register.html
│   └── trash.html
├── assets/              # Images and logos
│   ├── ars_logo_32x32.png
│   ├── dashboard.png
│   ├── dashboardmobile.jpg
│   ├── dashboardmobile2.jpg
│   └── ER Diagram.svg
├── nginx/               #
Nginx config
    ├── minigdrive.conf 
├── uploads/             # User uploaded files
├── trash/               # Deleted files
├── storage/             # User storage directory
├── Dockerfile           # Docker configuration
└── requirements.txt     # Python dependencies 

```

---

## Voice Commands Supported

Below are the voice commands you can use in **MiniGDrive**:

| Command Example                            | Action                                      |
|--------------------------------------------|---------------------------------------------|
| `upload file`                              | Open file upload dialog                     |
| `delete file [filename]`                   | Delete the specified file                   |
| `list files`                               | Highlight/list all files                    |
| `logout` / `log me out` / `sign out`       | Log out of your account                     |
| `trash` / `go to trash` / `view/open/show trash` | Go to Trash page                    |
| `go to dashboard` / `view/open dashboard`  | Go to Dashboard page                        |
| `go to profile` / `view/open profile`      | Go to Profile page                          |
| `switch language to english`               | Change app language to English              |
| `switch language to tamil`                 | Change app language to Tamil                |
| `switch language to hindi`                 | Change app language to Hindi                |
| `switch to dark mode` / `enable dark mode` | Switch to Dark Mode                         |
| `switch to light mode` / `enable light mode`| Switch to Light Mode                        |
| `search for [filename]`                    | Search for a file by name                   |
| `favourites` / `open/view/show my favourites` | Go to Favourites page                    |

> 🔎 **Note:** Replace `[filename]` with the actual file name, e.g., `delete file report.pdf`.


---

## How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aswin-AR5055/MiniGDrive.git
   cd MiniGDrive
   ```

2. **Install the dependencies** (use a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```
   OR:
   ```bash
   python3 app.py
   ```

4. **Visit the application**:
   ```bash
   http://127.0.0.1:6000 
   ```

---

## Run with Docker

If you have Docker installed, you can run MiniGDrive without installing dependencies manually.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aswin-AR5055/MiniGDrive.git
   cd MiniGDrive
   ```

2. **Build the Docker image**:
   ```bash
   docker build -t minigdrive .
   ```

3. **Run the container**:
   ```bash
   docker run -d -p 6000:6000 minigdrive
   ```

4. **Configure Nginx**:
   ```bash
   server {
      listen 80;
      server_name yourdomain.com;

      location /static/ {
         alias /home/ubuntu/MiniGDrive/static/;
         expires 30d;
         access_log off;
      }

      location /static/profiles/ {
         alias /home/ubuntu/minigdrive_data/profiles/;
         expires 30d;
         access_log off;
      }

      location / {
         proxy_pass http://127.0.0.1:6000;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      }
   }

   ```

5. **Restart Nginx**:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```


6. **Access the app via your domain or EC2 public IP**:
   ```bash
   http://yourdomain.com
   ```

---

## Deployment Pipeline

- Push code to master branch

- GitHub Actions runs unit tests

- SSH into AWS EC2 instance

- Docker image rebuilds with latest code

- Existing container is stopped and removed

- New container starts on port 6000

- Nginx proxies requests from port 80 → 6000

- Hosted securely via AWS CloudFront (HTTPS)

---

## Infrastructure Setup

We use **Terraform** to provision AWS resources, with secrets securely managed via **GitHub Actions**:

- **Infrastructure as Code (IaC):** All AWS resources are defined in Terraform configuration files.  
- **Secure Secrets:** AWS credentials and other sensitive values are stored in **GitHub Secrets**, never in code.  
- **Automated Provisioning:** GitHub Actions workflow(on Ec2 branch) automatically runs Terraform to apply infrastructure changes.  
- **Consistency:** Ensures the same environment setup across dev, staging, and production.

---

## Security Notes

- **Password Security**: Passwords are hashed securely before being stored in the database using Werkzeug.  
- **Session Management**: Session tokens ensure users stay logged in securely for up to 7 days.  
- **Important:** For your safety, **do not use your real personal email address or password** when registering on this site. Use a secondary or disposable email, and a unique password that you do not use elsewhere.

---

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to use, modify, and distribute this project — just keep the license file and give proper credit.  
Built for the community, with ❤️ by [Aswin Raj](https://github.com/Aswin-AR5055).

---

## Acknowledgements

Full Stack Development and DevOps: [Aswin Raj A](https://www.instagram.com/ar_aswinraj)  
Design Suggestions: [Mohamed Suhail S](https://github.com/octatrix008)  

Built with love, sweat and coffee ☕


