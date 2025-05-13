import pytest
import os
import shutil
from app import app, init_db

# Test constants
TEST_USER = "testuser"
TEST_PASS = "testpass"
TEST_UPLOAD_FOLDER = "test_uploads"
TEST_TRASH_FOLDER = "test_trash"


@pytest.fixture
def client():
    """
    Fixture to set up and tear down the test client and environment.
    """
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = TEST_UPLOAD_FOLDER
    app.secret_key = 'testkey'
    app.permanent_session_lifetime = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    # Cleanup after tests
    if os.path.exists(TEST_UPLOAD_FOLDER):
        shutil.rmtree(TEST_UPLOAD_FOLDER)
    if os.path.exists(TEST_TRASH_FOLDER):
        shutil.rmtree(TEST_TRASH_FOLDER)
    if os.path.exists("testfile.txt"):
        os.remove("testfile.txt")


def test_home_redirect_to_logo(client):
    """
    Test that the home page redirects to the logo page.
    """
    response = client.get('/')
    assert response.status_code == 302
    assert '/logo' in response.headers['Location']


def test_logo_page_loads_successfully(client):
    """
    Test that the logo page loads successfully.
    """
    response = client.get('/logo')
    assert response.status_code == 200
    assert b'ARS Cloud Drive' in response.data  # Updated to match the page title


def test_user_register_login_logout_workflow(client):
    """
    Test the entire workflow of user registration, login, and logout.
    """
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
    assert b"My Files" in response.data  # Updated to check for the correct dashboard content

    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data


def test_profile_update(client):
    """
    Test updating the user's profile.
    """
    # Login first
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    # Update profile
    response = client.post('/profile', data={
        'bio': 'Just testing',
        'age': '21'
    }, follow_redirects=True)

    assert b'Just testing' in response.data
    assert b'21' in response.data


def test_dashboard_requires_authentication(client):
    """
    Test that accessing the dashboard redirects to login if not authenticated.
    """
    response = client.get('/dashboard', follow_redirects=True)
    assert b'Login' in response.data


def test_file_upload_functionality(client):
    """
    Test uploading a file to the user's folder.
    """
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    test_file_path = 'testfile.txt'
    with open(test_file_path, 'w') as f:
        f.write('Test content')

    with open(test_file_path, 'rb') as f:
        response = client.post('/upload', data={'file': f}, follow_redirects=True)

    assert b"My Files" in response.data  # Updated to check for the correct dashboard content
    assert os.path.exists(os.path.join(TEST_UPLOAD_FOLDER, TEST_USER, 'testfile.txt'))

    os.remove(test_file_path)


def test_trash_restore_and_permanent_delete(client):
    """
    Test trashing, restoring, and permanently deleting a file.
    """
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    user_folder = os.path.join(TEST_UPLOAD_FOLDER, TEST_USER)
    trash_folder = os.path.join(TEST_TRASH_FOLDER, TEST_USER)
    os.makedirs(user_folder, exist_ok=True)
    os.makedirs(trash_folder, exist_ok=True)

    filename = 'trashme.txt'
    filepath = os.path.join(user_folder, filename)
    with open(filepath, 'w') as f:
        f.write('To be trashed')

    # Move to trash
    client.get(f'/delete/{filename}', follow_redirects=True)
    assert not os.path.exists(filepath)
    assert os.path.exists(os.path.join(trash_folder, filename))

    # Restore from trash
    client.get(f'/restore/{filename}', follow_redirects=True)
    assert os.path.exists(filepath)
    assert not os.path.exists(os.path.join(trash_folder, filename))

    # Permanently delete
    client.get(f'/delete/{filename}', follow_redirects=True)
    client.get(f'/permadelete/{filename}', follow_redirects=True)
    assert not os.path.exists(os.path.join(trash_folder, filename))


def test_zip_download_with_no_files(client):
    """
    Test attempting to download a ZIP file with no selected files.
    """
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    response = client.post('/download_zip', data={'selected_files': []}, follow_redirects=True)
    assert b"My Files" in response.data  # Updated to check for the correct dashboard content


def test_file_sharing_link_generation(client):
    """
    Test generating a shareable link for a file.
    """
    client.post('/login', data={'username': TEST_USER, 'password': TEST_PASS}, follow_redirects=True)

    user_folder = os.path.join(TEST_UPLOAD_FOLDER, TEST_USER)
    os.makedirs(user_folder, exist_ok=True)
    filename = 'shareme.txt'
    filepath = os.path.join(user_folder, filename)
    with open(filepath, 'w') as f:
        f.write('Shared content')

    response = client.get(f'/share/{filename}', follow_redirects=True)
    assert b'Share this link' in response.data