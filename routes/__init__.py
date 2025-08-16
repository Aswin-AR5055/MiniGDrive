from flask import Flask
import os
from datetime import timedelta

# Create Flask app first
app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
           static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"))
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
app.permanent_session_lifetime = timedelta(days=7)

# Directory Configuration
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_BASE = os.path.join(BASE_DIR, "uploads")
TRASH_BASE = os.path.join(BASE_DIR, "trash")
STORAGE_DIR = os.path.join(BASE_DIR, "storage")

# Create necessary directories
os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(UPLOAD_BASE, exist_ok=True)
os.makedirs(TRASH_BASE, exist_ok=True)

# Make variables available for import
__all__ = ['app', 'UPLOAD_BASE', 'TRASH_BASE', 'STORAGE_DIR', 'BASE_DIR']


# Import all routes
from . import home
from . import login
from . import register
from . import dashboard
from . import upload
from . import download
from . import trash
from . import favourites
from . import profile
from . import share
from . import star_unstar
from . import trash_del_restore
from . import del_restore_permadelete
from . import permadelete
from . import zip
from . import logo  # Since home redirects to /logo
