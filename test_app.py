import pytest
import os
import shutil
import io
from app import app
from db_schema import get_db_connection

TEST_USER = "testuser"
TEST_PASS = "testpass"
TEST_FILE_CONTENT = b"Hello World!"
TEST_FILE_NAME = "testfile.txt"


# ---------- Fixtures ----------

@pytest.fixture(scope="session")
def conn():
    connection = get_db_connection()
    yield connection
    connection.close()


@pytest.fixture
def client(conn):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    app.secret_key = 'testkey'

    # Reset DB tables before each test
    with conn.cursor() as cur:
        cur.execute("TRUNCATE users RESTART IDENTITY CASCADE")
        cur.execute("TRUNCATE favourites RESTART IDENTITY CASCADE")
        conn.commit()

    # Clean up filesystem
    cleanup_dirs(TEST_USER)

    with app.test_client() as client:
        yield client

    cleanup_dirs(TEST_USER)


def cleanup_dirs(username):
    shutil.rmtree(os.path.join("uploads", username), ignore_errors=True)
    shutil.rmtree(os.path.join("trash", username), ignore_errors=True)


# ---------- Basic Routes ----------

def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/logo' in response.headers['Location']


def test_logo_page(client):
    response = client.get('/logo')
    assert response.status_code == 200


# ---------- Auth Tests ----------

def test_register_login_logout(client):
    # Register
    response = client.post('/register', data={
        'username': TEST_USER,
        'password': TEST_PASS
    }, follow_redirects=True)
    assert b'Account created' in response.data

    # Login
    response = client.post('/login', data={
        'username': TEST_USER,
        'password': TEST_PASS
    }, follow_redirects=True)
    assert b'Dashboard' in response.data or b'My Files' in response.data

    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data


# ---------- File Operations ----------

def test_file_upload(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    data = {'file': (io.BytesIO(TEST_FILE_CONTENT), TEST_FILE_NAME)}
    response = client.post('/upload', data=data, follow_redirects=True, content_type='multipart/form-data')
    assert b'File uploaded' in response.data


def test_file_download(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    # Upload first
    client.post('/upload', data={'file': (io.BytesIO(TEST_FILE_CONTENT), TEST_FILE_NAME)},
                follow_redirects=True, content_type='multipart/form-data')

    response = client.get(f'/download/{TEST_FILE_NAME}')
    assert response.data == TEST_FILE_CONTENT


def test_add_to_favourites(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    # Upload first
    client.post('/upload', data={'file': (io.BytesIO(TEST_FILE_CONTENT), TEST_FILE_NAME)},
                follow_redirects=True, content_type='multipart/form-data')

    response = client.get(f'/favourite/{TEST_FILE_NAME}', follow_redirects=True)
    assert b'Added to favourites' in response.data


def test_delete_file(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    # Upload first
    client.post('/upload', data={'file': (io.BytesIO(TEST_FILE_CONTENT), TEST_FILE_NAME)},
                follow_redirects=True, content_type='multipart/form-data')

    # Delete
    response = client.get(f'/delete/{TEST_FILE_NAME}', follow_redirects=True)
    assert b'File deleted' in response.data


def test_restore_file(client):
    client.post('/register', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    # Upload first
    client.post('/upload', data={'file': (io.BytesIO(TEST_FILE_CONTENT), TEST_FILE_NAME)},
                follow_redirects=True, content_type='multipart/form-data')

    # Delete
    client.get(f'/delete/{TEST_FILE_NAME}', follow_redirects=True)
    # Restore
    response = client.get(f'/restore/{TEST_FILE_NAME}', follow_redirects=True)
    assert b'Restored file' in response.data
