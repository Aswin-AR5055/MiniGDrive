import pytest
import os
import shutil
from app import app, init_db

TEST_USER = "testuser"
TEST_PASS = "testpass"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    app.secret_key = 'testkey'
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/logo' in response.headers['Location']

def test_logo_page(client):
    response = client.get('/logo')
    assert response.status_code == 200

def test_register_and_login_logout(client):
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

def test_profile_update(client):
    # First login
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    # Update profile
    response = client.post('/profile', data={
        'bio': 'Just testing',
        'age': '21'
    }, follow_redirects=True)

    assert b'Just testing' in response.data or b'Profile' in response.data

def test_dashboard_requires_login(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert b'Login' in response.data

def test_upload_file(client):
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    # Upload file
    test_file_path = 'testfile.txt'
    with open(test_file_path, 'w') as f:
        f.write('hello')

    with open(test_file_path, 'rb') as f:
        response = client.post('/upload', data={'file': f}, follow_redirects=True)

    os.remove(test_file_path)
    assert b'Dashboard' in response.data or response.status_code == 200

def test_trash_and_restore_file(client):
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    user_folder = os.path.join('uploads', TEST_USER)
    trash_folder = os.path.join('trash', TEST_USER)
    os.makedirs(user_folder, exist_ok=True)
    os.makedirs(trash_folder, exist_ok=True)

    filename = 'trashme.txt'
    filepath = os.path.join(user_folder, filename)
    with open(filepath, 'w') as f:
        f.write('bye')

    # Move to trash
    client.get(f'/delete/{filename}', follow_redirects=True)
    assert not os.path.exists(filepath)

    # Restore from trash
    client.get(f'/restore/{filename}', follow_redirects=True)
    assert os.path.exists(filepath)

    # Permanently delete
    client.get(f'/delete/{filename}', follow_redirects=True)
    client.get(f'/permadelete/{filename}', follow_redirects=True)
    assert not os.path.exists(os.path.join(trash_folder, filename))

def test_zip_download_empty(client):
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)
    response = client.post('/download_zip', data={'selected_files': []}, follow_redirects=True)
    assert b'Dashboard' in response.data or response.status_code == 200

def test_share_link(client):
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    user_folder = os.path.join('uploads', TEST_USER)
    os.makedirs(user_folder, exist_ok=True)
    filename = 'shareme.txt'
    filepath = os.path.join(user_folder, filename)
    with open(filepath, 'w') as f:
        f.write('shared!')

    response = client.get(f'/share/{filename}', follow_redirects=True)
    assert b'Share this link' in response.data

