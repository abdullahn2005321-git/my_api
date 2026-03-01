import os
import pytest

from app import app
from db import set_db_path, init_db


@pytest.fixture()
def client():
    test_db = "test.db"

    if os.path.exists(test_db):
        os.remove(test_db)

    set_db_path(test_db)
    init_db()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    if os.path.exists(test_db):
        os.remove(test_db)

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_me_requires_token(client):
    res = client.get("/me")
    assert res.status_code == 401

def test_register_login_me(client):

    r = client.post("/register", json={"username": "abdullah", "password": "1234"})
    assert r.status_code == 201

    l = client.post("/login", json={"username": "abdullah", "password": "1234"})
    assert l.status_code == 200
    token = l.get_json()["token"]

    res = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.get_json()["user"]
    assert data["username"] == "abdullah"

def test_users_pagination(client):

    client.post("/users", json={"name": "Ali"})
    client.post("/users", json={"name": "Omar"})
    client.post("/users", json={"name": "Sara"})

    res = client.get("/users", query_string={"page": 1, "limit": 2})
    assert res.status_code == 200
    data = res.get_json()
    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["total"] == 3
    assert len(data["users"]) == 2