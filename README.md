# <img src="assets/ars_logo_32x32.png" alt="ARS" width="24" height="24"> MiniGDrive          

![Deploy](https://github.com/Aswin-AR5055/MiniGDrive/actions/workflows/pytest-update-ec2.yml/badge.svg)
![Status](https://img.shields.io/badge/status-completed-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**MiniGDrive** is a lightweight, responsive cloud storage application powered by Flask + SQLite, now with voice command support. Users can register, log in, upload, download, and manage files — all within a clean and intuitive UI.  
Now includes **Prometheus + Grafana monitoring dashboards** for performance and usage metrics.

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

- **Voice Command Support**: Browser-based voice commands powered by Web Speech API.  
- **User Registration and Login**: Secure authentication with password hashing.  
- **File Upload and Download**: Easy file management.  
- **Trash System**: Deleted files go to trash instead of being permanently removed.  
- **Restore and Permanent Delete**: Restore files from trash or delete permanently.  
- **Bulk Actions**: Delete, restore, or download multiple files as ZIP.  
- **Star Files as Favourites**: Mark important files for easy access.  
- **Optimized Static Delivery**: Static assets served via Nginx for faster loading.  
- **Storage Monitoring**: View used storage with visual progress bar.  
- **Responsive UI**: Works on both desktop and mobile.  
- **Profile Customization**: Add bio, age, and profile picture.  
- **Multilingual Support**: English, Tamil, Hindi.  
- **Monitoring**: Real-time metrics via **Prometheus + Grafana** dashboards.

---

## Entity Relationship(ER) Diagram

<div align="center">
  <img src="assets/ER%20Diagram.svg" alt="ER Diagram" width="250"/>
</div>

---

## Tech Stack

| Layer                  | Technology Used                                                   | Purpose                                               |
|------------------------|-------------------------------------------------------------------|-------------------------------------------------------|
| **Backend**            | Python + Flask                                                    | Application logic                                     |
| **Database**           | SQLite                                                            | Storing user accounts, favourite files, and profiles |
| **Frontend**           | HTML (Flask templates), Bootstrap 5, Vanilla JavaScript, Web Speech API | Responsive UI, modals, voice commands, sorting/filtering, interactivity |
| **Security**           | Werkzeug (secure filename + password hashing)                     | Secure file uploads and password management          |
| **File Handling**      | Python libraries (`os`, `shutil`, `zipfile`, `uuid`, `unicodedata`) | File operations (uploads, storage, trash)           |
| **Session Management** | Flask + `datetime`                                                | Managing user sessions (login duration)              |
| **Application Server** | Gunicorn                                                          | WSGI server for running the Flask app                |
| **Web Server / Proxy** | Nginx                                                             | Reverse proxy, serve static files                     |
| **Hosting**            | AWS EC2                                                           | Server for running the app                            |
| **HTTPS/CDN**          | AWS CloudFront                                                    | Secure global access over HTTPS with CDN caching     |
| **Containerization**   | Docker                                                            | Packaging and running the app                         |
| **CI/CD**              | GitHub Actions                                                    | Automating tests and deployment                       |
| **Monitoring**         | Prometheus + Grafana                                              | Metrics collection, visualization, and performance monitoring |

---

## Deployment Pipeline (Updated)

1. Push code to **master branch** triggers GitHub Actions.  
2. Automated **tests run** using pytest.  
3. SSH into **AWS EC2 instance**.  
4. Docker stack rebuilds using `docker-compose` with updated services:
   - **MiniGDrive app**  
   - **Prometheus** for metrics collection  
   - **Grafana** for dashboard visualization  
5. Old containers are stopped and removed.  
6. **App data volumes are preserved**; **Grafana volume** can be optionally reset for fresh dashboards.  
7. New containers start with ports exposed:
   - App: **6000**
   - Prometheus: **9090**
   - Grafana: **3000**  
8. Nginx proxies requests from **port 80 → app 6000**.  
9. **Access monitoring dashboards**:
   - Prometheus: `http://yourdomain.com:9090`
   - Grafana: `http://yourdomain.com:3000`

---

## How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aswin-AR5055/MiniGDrive.git
   cd MiniGDrive
   ```

2. **Install dependencies** (virtual environment recommended):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Visit the application**:
   ```bash
   http://127.0.0.1:6000
   ```

---

## Run with Docker

1. **Build the Docker image**:
   ```bash
   docker build -t minigdrive .
   ```

2. **Run the stack with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Access app and monitoring dashboards**:
   - App: `http://localhost:6000`
   - Prometheus: `http://localhost:9090`
   - Grafana: `http://localhost:3000`

---

## Infrastructure Setup

- **Terraform** provisions AWS resources.  
- **Secrets** managed securely via **GitHub Actions**.  
- **Automated provisioning** ensures consistent dev/staging/production environments.  

---

## Security Notes

- **Password Security**: Passwords hashed via Werkzeug.  
- **Session Management**: Secure login sessions up to 7 days.  
- **Important**: Do not use personal credentials; use disposable accounts for testing.

---

## License

MIT License — built with ❤️ by [Aswin Raj](https://github.com/Aswin-AR5055).

---

## Acknowledgements

- Full Stack Development and DevOps: [Aswin Raj A](https://www.instagram.com/ar_aswinraj)  
- Design Suggestions: [Mohamed Suhail S](https://github.com/octatrix008)  
- Built with love, sweat, and coffee ☕

