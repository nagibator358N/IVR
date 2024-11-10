import pytest
from app.main import app
from app.db.database import engine, Base
from fastapi.testclient import TestClient
import os
TEST_DB_FILE = "test.db"
SQLITE_DATABASE_URL_TEST = f"sqlite:///{TEST_DB_FILE}"
os.environ['TESTING'] = 'True'
os.environ['SQLITE_TEST'] = SQLITE_DATABASE_URL_TEST

new_user_correct = {"mail": "Admin8@gmail.com", "password": "Aboba2007!"}
new_user_correct_2 = {"mail": "Admin4@gmail.com", "password": "Aboba2007!"}
new_user_incorrect_email = {"mail": "Admin8", "password": "Aboba2007!"}
new_user_incorrect_pass = {"mail": "Admin8@gmail.com", "password": "aboba2007"}
new_user_incorrect_both = {"mail": "Admin8", "password": "aboba2007"}
update_user_correct_all = {"mail": "Admin5@gmail.com",
                           "new_password": "Aboba2002!",
                           "old_password": "Aboba2007!"}
update_user_used_em = {"mail": "Admin4@gmail.com",
                       "new_password": "Aboba2002!",
                       "old_password": "Aboba2007!"}
update_user_without_data = {"mail": None,
                            "new_password": None,
                            "old_password": "Aboba2007!"}
update_user_incorrect_em = {"mail": "Admin4",
                            "new_password": None,
                            "old_password": None}
update_user_incorrect_pas = {"mail": None,
                             "new_password": "Aboba2007!",
                             "old_password": "Aboba2011!"}
update_user_incorrect_non = {"mail": None,
                             "new_password": None,
                             "old_password": None}
update_user_correct_pas = {"mail": None,
                           "new_password": "Aboba2002!",
                           "old_password": "Aboba2007!"}
get_user_correct_email = "Admin8@gmail.com"
get_user_incorrect_email = "Admin5@gmail.com"
get_user_unexist_email = "Admin5"


@pytest.fixture()
def temp_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture()
def add_user():
    with TestClient(app) as client:
        client.post("/user/add/", json=new_user_correct)


@pytest.fixture()
def add_user_2():
    with TestClient(app) as client:
        client.post("/user/add/", json=new_user_correct_2)


def test_registration_correct(temp_db):
    with TestClient(app) as client:
        response = client.post("/user/add/", json=new_user_correct)
    assert response.status_code == 201
    data = response.json()
    assert data["success"]
    assert data["data"]["id"] == 1
    assert data["data"]["email"] == new_user_correct["mail"]


def test_registration_correct_2(temp_db, add_user):
    with TestClient(app) as client:
        response = client.post("/user/add/", json=new_user_correct_2)
    assert response.status_code == 201
    data = response.json()
    assert data["success"]
    assert data["data"]["id"] == 2
    assert data["data"]["email"] == new_user_correct_2["mail"]


def test_registration_incorrect_email_format(temp_db):
    with TestClient(app) as client:
        response = client.post("/user/add/", json=new_user_incorrect_email)
    assert response.status_code == 422


def test_registration_incorrect_password_format(temp_db):
    with TestClient(app) as client:
        response = client.post("/user/add/", json=new_user_incorrect_pass)
    assert response.status_code == 422


def test_registration_incorrect_both_format(temp_db):
    with TestClient(app) as client:
        response = client.post("/user/add/", json=new_user_incorrect_both)
    assert response.status_code == 422


def test_update_user_correct(temp_db, add_user):
    with TestClient(app) as client:
        response = client.put("/user/update/1", json=update_user_correct_all)
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["data"]["id"] == 1
    assert data["data"]["email"] == update_user_correct_all["mail"]


def test_update_user_used_em(temp_db, add_user, add_user_2):
    with TestClient(app) as client:
        response = client.put("/user/update/1", json=update_user_used_em)
    assert response.status_code == 403


def test_update_user_without_data(temp_db, add_user):
    with TestClient(app) as client:
        response = client.put("/user/update/1", json=update_user_without_data)
    assert response.status_code == 403


def test_update_user_incorrect_email(temp_db, add_user):
    with TestClient(app) as client:
        response = client.put("/user/update/1", json=update_user_incorrect_em)
    assert response.status_code == 422


def test_update_user_incorrect_password(temp_db, add_user):
    with TestClient(app) as client:
        response = client.put("/user/update/1", json=update_user_incorrect_pas)
    assert response.status_code == 403


def test_update_user_incorrect_none_filled(temp_db, add_user):
    with TestClient(app) as client:
        response = client.put("/user/update/1", json=update_user_incorrect_non)
    assert response.status_code == 403


def test_update_user_correct_password(temp_db, add_user):
    with TestClient(app) as client:
        response = client.put("/user/update/1", json=update_user_correct_all)
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["data"]["id"] == 1
    assert data["data"]["email"] == update_user_correct_all["mail"]


def test_get_user_by_em_correct(temp_db, add_user):
    with TestClient(app) as client:
        response = client.get(f"/user/mail/{get_user_correct_email}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["data"]["id"] == 1
    assert data["data"]["email"] == get_user_correct_email


def test_get_user_by_em_incorrect(temp_db, add_user):
    with TestClient(app) as client:
        response = client.get(f"/user/mail/{get_user_incorrect_email}")
    assert response.status_code == 404


def test_get_user_by_em_unexist(temp_db, add_user):
    with TestClient(app) as client:
        response = client.get(f"/user/mail/{get_user_unexist_email}")
    assert response.status_code == 422


def test_get_user_by_id_correct(temp_db, add_user):
    with TestClient(app) as client:
        response = client.get(f"/user/{1}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["data"]["id"] == 1


def test_get_user_by_id_incorrect(temp_db, add_user):
    with TestClient(app) as client:
        response = client.get(f"/user/{100}")
    assert response.status_code == 404


def test_get_user_by_id_unexist(temp_db, add_user):
    with TestClient(app) as client:
        response = client.get("/user/{100}")
    assert response.status_code == 422
