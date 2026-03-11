from flask import Flask, request, jsonify
import sqlite3
from contact.contacts_db import *

app = Flask(__name__)

# initialize database
init_db()


def is_valid_email(email):
    return isinstance(email, str) and "@" in email and "." in email


# GET /contacts -> list all contacts
@app.route("/contacts", methods=["GET"])
def list_contacts():
    contacts = get_all_contacts()
    return jsonify(contacts), 200


# POST /contacts -> create contact
@app.route("/contacts", methods=["POST"])
def create_contact():
    data = request.get_json()

    if not data:
        return {"error": "invalid json"}, 400

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    if not name:
        return {"error": "name is required"}, 400

    if not email or not is_valid_email(email):
        return {"error": "invalid email"}, 400

    if not phone:
        return {"error": "phone is required"}, 400

    try:
        contact_id = add_contact(name, email, phone)
        contact = get_contact(contact_id)
        return jsonify(contact), 201
    except sqlite3.IntegrityError:
        return {"error": "duplicate email"}, 400


# GET /contacts/<id>
@app.route("/contacts/<int:contact_id>", methods=["GET"])
def get_single_contact(contact_id):
    contact = get_contact(contact_id)

    if not contact:
        return {"error": "contact not found"}, 404

    return jsonify(contact), 200


# PUT /contacts/<id>
@app.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_single_contact(contact_id):
    existing = get_contact(contact_id)

    if not existing:
        return {"error": "contact not found"}, 404

    data = request.get_json()

    name = data.get("name", existing["name"])
    email = data.get("email", existing["email"])
    phone = data.get("phone", existing["phone"])

    if not name:
        return {"error": "name is required"}, 400

    if not email or not is_valid_email(email):
        return {"error": "invalid email"}, 400

    if not phone:
        return {"error": "phone is required"}, 400

    try:
        update_contact(contact_id, name, email, phone)
        return jsonify(get_contact(contact_id)), 200
    except sqlite3.IntegrityError:
        return {"error": "duplicate email"}, 400


# DELETE /contacts/<id>
@app.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_single_contact(contact_id):
    deleted = delete_contact(contact_id)

    if not deleted:
        return {"error": "contact not found"}, 404

    return {"message": "contact deleted"}, 200


# GET /contacts/search?q=query
@app.route("/contacts/search", methods=["GET"])
def search_for_contacts():
    query = request.args.get("q", "")
    results = search_contacts(query)
    return jsonify(results), 200


if __name__ == "__main__":
    app.run(debug=True)