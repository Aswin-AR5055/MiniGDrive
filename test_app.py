import pytest
import os
import shutil
import io
import psycopg2
from app import app, init_db

TEST_USER = "testuser"
TEST_PASS = "testpass"

# ---------- Fixtures & Setup ----------

@pytest.fixture(scope="session")
def test_db():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        database=os.getenv("POSTGRES_DB", "minidrive"),
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", "supersecret")
    )
    yield conn
    conn.close()

@pytest.fixture
def client(test_db):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    app.secret_key = 'testkey'

    # Reset DB schema before each test
    with test_db.cursor() as cur:
        cur.execute("TRUNCATE users RESTART IDENTITY CASCADE")
        cur.execute("TRUNCATE favourites RESTART IDENTITY CASCADE")
        test_db.commit()

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    cleanup_dirs(TEST_USER)

def cleanup_dirs(username):
    shutil.rmtree(os.path.join("uploads", username), ignore_errors=True)
    shutil.rmtree(os.path.join("trash", username), ignore_errors=True)


# ---------- Tests ----------

def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/logo' in response.headers['Location']

def test_logo_page(client):
    response = client.get('/logo')
    assert response.status_code == 200

def test_register_and_login_logout(client):
    response = client.post('/register', data={
        'username': TEST_USER,
        'password': TEST_PASS
    }, follow_redirects=True)
    assert b'Account created' in response.data

    response = client.post('/login', data={
        'username': TEST_USER,
        'password': TEST_PASS
    }, follow_redirects=True)
    assert b'Dashboard' in response.data or b'My Files' in response.data

    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data

def test_dashboard_requires_login(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert b'Login' in response.data

def test_upload_file(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    test_file = (io.BytesIO(b"hello world"), "hello.txt")
    response = client.post('/upload', data={'file': test_file}, content_type='multipart/form-data', follow_redirects=True)
    assert b"Cloud Drive" in response.data or b"My Files" in response.data

def test_file_download(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    filepath = os.path.join("uploads", TEST_USER, "dltest.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("download me")

    response = client.get('/download/dltest.txt')
    assert response.status_code == 200
    assert b"download me" in response.data

def test_trash_and_restore_file(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

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
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    response = client.post('/download_zip', data={'selected_files': []}, follow_redirects=True)
    assert response.status_code == 200

def test_download_zip_with_file(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    filename = "zipme.txt"
    file_path = os.path.join("uploads", TEST_USER, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write("zip content")

    response = client.post('/download_zip', data={'selected_files': [filename]}, follow_redirects=False)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/zip'

def test_share_link(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    filepath = os.path.join("uploads", TEST_USER, "share.txt")
    with open(filepath, "w") as f:
        f.write("shareable")

    response = client.get('/share/share.txt')
    assert b'Share this link' in response.data

def test_profile_update_text_only(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    response = client.post('/profile', data={'bio': 'Tester bio', 'age': '99'}, follow_redirects=True)
    assert b'Tester bio' in response.data or b'Profile' in response.data

def test_delete_restore_selected(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    filename = "bulkdel.txt"
    filepath = os.path.join("uploads", TEST_USER, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("bulk delete test")

    response = client.post('/delete_selected', json={'files': [filename]})
    assert response.status_code == 200
    assert not os.path.exists(filepath)

    response = client.post('/restore_selected', json={'files': [filename]})
    assert response.status_code == 200
    assert os.path.exists(filepath)

    response = client.post('/delete_selected', json={'files': [filename]})
    response = client.post('/permadelete_selected', json={'files': [filename]})
    assert not os.path.exists(os.path.join("trash", TEST_USER, filename))
