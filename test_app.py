import pytest
import os
import io
import psycopg2
import shutil
from app import app

# --- Test credentials (hardcoded for pipeline) ---
TEST_USER = "testuser"
TEST_PASS = "testpass"
TEST_DB = "test_db"
TEST_HOST = "localhost"
TEST_PORT = 5432

# --- Test DB fixture ---
@pytest.fixture(scope="module")
def db_conn():
    # Connect directly using test credentials
    conn = psycopg2.connect(
        host=TEST_HOST,
        database=TEST_DB,
        user=TEST_USER,
        password=TEST_PASS,
        port=TEST_PORT
    )
    cursor = conn.cursor()

    # Create tables only for testing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            bio TEXT,
            age INTEGER,
            profile_pic TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favourites (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            filename TEXT NOT NULL
        )
    """)
    conn.commit()
    yield conn

    # Cleanup only test user data
    cursor.execute("DELETE FROM favourites WHERE username = %s;", (TEST_USER,))
    cursor.execute("DELETE FROM users WHERE username = %s;", (TEST_USER,))
    conn.commit()
    cursor.close()
    conn.close()

# --- Flask test client fixture ---
@pytest.fixture
def client(db_conn):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.secret_key = "test_secret_key"
    app.config['UPLOAD_FOLDER'] = os.path.join("uploads", TEST_USER)

    # Ensure isolated folders for testing
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    trash_folder = os.path.join("trash", TEST_USER)
    os.makedirs(trash_folder, exist_ok=True)

    with app.test_client() as client:
        yield client

    # Cleanup test folders
    shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=True)
    shutil.rmtree(trash_folder, ignore_errors=True)

# --- Helper functions ---
def login(client):
    return client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

def register(client):
    return client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

# --- TESTS ---
def test_home_redirect(client):
    resp = client.get('/')
    assert resp.status_code == 302
    assert '/logo' in resp.headers['Location']

def test_logo_page(client):
    resp = client.get('/logo')
    assert resp.status_code == 200

def test_register_and_login_logout(client):
    register(client)
    resp = login(client)
    assert b'Dashboard' in resp.data or b'My Files' in resp.data

    resp = client.get('/logout', follow_redirects=True)
    assert b'Login' in resp.data

def test_dashboard_requires_login(client):
    resp = client.get('/dashboard', follow_redirects=True)
    assert b'Login' in resp.data

def test_upload_file(client):
    login(client)
    test_file = (io.BytesIO(b"hello world"), "hello.txt")
    resp = client.post('/upload', data={'file': test_file}, content_type='multipart/form-data', follow_redirects=True)
    assert b"Cloud Drive" in resp.data or b"My Files" in resp.data

def test_file_download(client):
    login(client)
    filepath = os.path.join("uploads", TEST_USER, "dltest.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("download me")
    resp = client.get('/download/dltest.txt')
    assert resp.status_code == 200
    assert b"download me" in resp.data

def test_trash_and_restore_file(client):
    login(client)
    upload_path = os.path.join("uploads", TEST_USER, "trashme.txt")
    with open(upload_path, "w") as f:
        f.write("to be trashed")
    client.get('/delete/trashme.txt', follow_redirects=True)
    assert not os.path.exists(upload_path)
    client.get('/restore/trashme.txt', follow_redirects=True)
    assert os.path.exists(upload_path)
    client.get('/delete/trashme.txt', follow_redirects=True)
    client.get('/permadelete/trashme.txt', follow_redirects=True)
    assert not os.path.exists(os.path.join("trash", TEST_USER, "trashme.txt"))

def test_download_zip_empty(client):
    login(client)
    resp = client.post('/download_zip', data={'selected_files': []}, follow_redirects=True)
    assert resp.status_code == 200

def test_download_zip_with_file(client):
    login(client)
    filename = "zipme.txt"
    file_path = os.path.join("uploads", TEST_USER, filename)
    with open(file_path, "w") as f:
        f.write("zip content")
    resp = client.post('/download_zip', data={'selected_files': [filename]}, follow_redirects=False)
    assert resp.status_code == 200
    assert resp.headers['Content-Type'] == 'application/zip'

def test_share_link(client):
    login(client)
    filepath = os.path.join("uploads", TEST_USER, "share.txt")
    with open(filepath, "w") as f:
        f.write("shareable")
    resp = client.get('/share/share.txt')
    assert b'Share this link' in resp.data

def test_profile_update_text_only(client):
    login(client)
    resp = client.post('/profile', data={'bio': 'Tester bio', 'age': '99'}, follow_redirects=True)
    assert b'Tester bio' in resp.data or b'Profile' in resp.data

def test_delete_restore_selected(client):
    login(client)
    filename = "bulkdel.txt"
    file_path = os.path.join("uploads", TEST_USER, filename)
    with open(file_path, "w") as f:
        f.write("bulk delete test")
    resp = client.post('/delete_selected', json={'files': [filename]})
    assert resp.status_code == 200
    assert not os.path.exists(file_path)
    resp = client.post('/restore_selected', json={'files': [filename]})
    assert resp.status_code == 200
    assert os.path.exists(file_path)
    resp = client.post('/delete_selected', json={'files': [filename]})
    resp = client.post('/permadelete_selected', json={'files': [filename]})
    assert not os.path.exists(os.path.join("trash", TEST_USER, filename))
