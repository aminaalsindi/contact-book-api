import pytest
from contact.contacts_app import app
from contact.contacts_db import init_db, get_connection


@pytest.fixture
def client():
    init_db()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts")
    conn.commit()
    conn.close()

    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_contact(client):
    response = client.post("/contacts", json={
        "name": "Amina",
        "email": "amina@test.com",
        "phone": "1234"
    })
    return response.get_json()


# POST tests

def test_post_valid_contact(client):
    response = client.post("/contacts", json={
        "name": "Ali",
        "email": "ali@test.com",
        "phone": "1111"
    })

    assert response.status_code == 201
    assert response.get_json()["name"] == "Ali"


def test_post_missing_name(client):
    response = client.post("/contacts", json={
        "email": "test@test.com",
        "phone": "1111"
    })

    assert response.status_code == 400


def test_post_invalid_email(client):
    response = client.post("/contacts", json={
        "name": "Ali",
        "email": "invalid",
        "phone": "1111"
    })

    assert response.status_code == 400


def test_post_duplicate_email(client):
    client.post("/contacts", json={
        "name": "Ali",
        "email": "ali@test.com",
        "phone": "1111"
    })

    response = client.post("/contacts", json={
        "name": "Ali2",
        "email": "ali@test.com",
        "phone": "2222"
    })

    assert response.status_code == 400


# GET tests

def test_get_empty_list(client):
    response = client.get("/contacts")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_list_after_adding_contacts(client):
    client.post("/contacts", json={"name": "A", "email": "a@test.com", "phone": "1"})
    client.post("/contacts", json={"name": "B", "email": "b@test.com", "phone": "2"})
    client.post("/contacts", json={"name": "C", "email": "c@test.com", "phone": "3"})

    response = client.get("/contacts")

    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_fetch_by_id(client, sample_contact):
    response = client.get(f"/contacts/{sample_contact['id']}")

    assert response.status_code == 200
    assert response.get_json()["email"] == "amina@test.com"


def test_fetch_non_existing_id(client):
    response = client.get("/contacts/999")

    assert response.status_code == 404


# PUT tests

def test_update_name(client, sample_contact):
    response = client.put(f"/contacts/{sample_contact['id']}", json={
        "name": "Amina Updated",
        "email": "amina@test.com",
        "phone": "1234"
    })

    assert response.status_code == 200
    assert response.get_json()["name"] == "Amina Updated"


def test_update_phone(client, sample_contact):
    response = client.put(f"/contacts/{sample_contact['id']}", json={
        "name": "Amina",
        "email": "amina@test.com",
        "phone": "9999"
    })

    assert response.status_code == 200
    assert response.get_json()["phone"] == "9999"


def test_update_non_existing_contact(client):
    response = client.put("/contacts/999", json={
        "name": "Test",
        "email": "test@test.com",
        "phone": "0000"
    })

    assert response.status_code == 404


# DELETE tests

def test_delete_existing_contact(client, sample_contact):
    response = client.delete(f"/contacts/{sample_contact['id']}")

    assert response.status_code == 200

    response2 = client.get(f"/contacts/{sample_contact['id']}")
    assert response2.status_code == 404


def test_delete_non_existing_contact(client):
    response = client.delete("/contacts/999")

    assert response.status_code == 404


# SEARCH tests

def test_search_by_name(client):
    client.post("/contacts", json={"name": "Amina", "email": "amina@test.com", "phone": "1"})
    client.post("/contacts", json={"name": "Sara", "email": "sara@test.com", "phone": "2"})

    response = client.get("/contacts/search?q=Amina")

    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_search_by_email(client):
    client.post("/contacts", json={"name": "Amina", "email": "amina@test.com", "phone": "1"})

    response = client.get("/contacts/search?q=amina@test.com")

    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_search_no_results(client):
    client.post("/contacts", json={"name": "Amina", "email": "amina@test.com", "phone": "1"})

    response = client.get("/contacts/search?q=zzz")

    assert response.status_code == 200
    assert response.get_json() == []


# Full workflow test

def test_full_workflow(client):
    create = client.post("/contacts", json={
        "name": "Noor",
        "email": "noor@test.com",
        "phone": "5555"
    })

    assert create.status_code == 201
    contact = create.get_json()
    cid = contact["id"]

    read = client.get(f"/contacts/{cid}")
    assert read.status_code == 200

    update = client.put(f"/contacts/{cid}", json={
        "name": "Noor Updated",
        "email": "noor@test.com",
        "phone": "7777"
    })

    assert update.status_code == 200

    delete = client.delete(f"/contacts/{cid}")
    assert delete.status_code == 200

    check = client.get(f"/contacts/{cid}")
    assert check.status_code == 404