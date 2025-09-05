import pytest
import os
import shutil
import io
from app import app
from db_schema import init_db
from db import get_connection

TEST_USER = "testuser"
TEST_PASS = "testpass"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Reset DB and clean test dirs before each test."""
    init_db()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE users, favourites RESTART IDENTITY CASCADE")
            conn.commit()
    finally:
        conn.close()

    yield

    # cleanup after each test
    shutil.rmtree(os.path.join("uploads", TEST_USER), ignore_errors=True)
    shutil.rmtree(os.path.join("trash", TEST_USER), ignore_errors=True)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.secret_key = "testkey"

    with app.test_client() as client:
        yield client


def register_and_login(client, username=TEST_USER, password=TEST_PASS):
    client.post("/register", data={"username": username, "password": password}, follow_redirects=True)
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)


def test_home_redirect(client):
    res = client.get("/")
    assert res.status_code == 302
    assert "/logo" in res.headers["Location"]


def test_logo_page(client):
    res = client.get("/logo")
    assert res.status_code == 200


def test_register_login_logout(client):
    res = register_and_login(client)
    assert b"Dashboard" in res.data or b"My Files" in res.data

    res = client.get("/logout", follow_redirects=True)
    assert b"Login" in res.data


def test_dashboard_requires_login(client):
    res = client.get("/dashboard", follow_redirects=True)
    assert b"Login" in res.data


def test_upload_and_download_file(client):
    register_and_login(client)

    test_file = (io.BytesIO(b"hello world"), "hello.txt")
    client.post("/upload", data={"file": test_file}, content_type="multipart/form-data", follow_redirects=True)

    path = os.path.join("uploads", TEST_USER, "hello.txt")
    assert os.path.exists(path)

    res = client.get("/download/hello.txt")
    assert res.status_code == 200
    assert b"hello world" in res.data


def test_trash_restore_permadelete(client):
    register_and_login(client)

    filepath = os.path.join("uploads", TEST_USER, "trashme.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("to be trashed")

    client.get("/delete/trashme.txt", follow_redirects=True)
    assert not os.path.exists(filepath)

    client.get("/restore/trashme.txt", follow_redirects=True)
    assert os.path.exists(filepath)

    client.get("/delete/trashme.txt", follow_redirects=True)
    client.get("/permadelete/trashme.txt", follow_redirects=True)
    assert not os.path.exists(os.path.join("trash", TEST_USER, "trashme.txt"))


def test_download_zip(client):
    register_and_login(client)

    # empty selection
    res = client.post("/download_zip", data={"selected_files": []}, follow_redirects=True)
    assert res.status_code == 200

    # with file
    filename = "zipme.txt"
    filepath = os.path.join("uploads", TEST_USER, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("zip content")

    res = client.post("/download_zip", data={"selected_files": [filename]}, follow_redirects=False)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/zip"


def test_share_link(client):
    register_and_login(client)

    filepath = os.path.join("uploads", TEST_USER, "share.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("shareable")

    res = client.get("/share/share.txt")
    assert b"Share this link" in res.data


def test_profile_update_text_only(client):
    register_and_login(client)

    res = client.post("/profile", data={"bio": "Tester bio", "age": "99"}, follow_redirects=True)
    assert b"Tester bio" in res.data or b"Profile" in res.data


def test_delete_restore_selected(client):
    register_and_login(client)

    filename = "bulkdel.txt"
    filepath = os.path.join("uploads", TEST_USER, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("bulk delete test")

    res = client.post("/delete_selected", json={"files": [filename]})
    assert res.status_code == 200
    assert not os.path.exists(filepath)

    res = client.post("/restore_selected", json={"files": [filename]})
    assert res.status_code == 200
    assert os.path.exists(filepath)

    res = client.post("/delete_selected", json={"files": [filename]})
    res = client.post("/permadelete_selected", json={"files": [filename]})
    assert not os.path.exists(os.path.join("trash", TEST_USER, filename))
