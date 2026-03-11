from database import *
import pytest
import os
from api_service import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_all_users(client):
    init_db()
    add_user("Ali")
    add_user("Sara")

    response = client.get("/get_users")

    assert response.status_code == 200
    assert "users" in response.json
    assert len(response.json["users"]) >= 2


def test_add_user(client):
    init_db()

    response = client.post("/add_user", json={"name": "Amina"})

    assert response.status_code == 200
    assert response.json == {"message": "User Amina added successfully"}


def test_delete_user(client):
    init_db()
    add_user("Ahmed")

    users = get_all_users()
    user_id = users[-1][0]

    response = client.post("/delete_user", json={"id": user_id})

    assert response.status_code == 200
    assert response.json == {"message": f"User with id {user_id} deleted successfully"}