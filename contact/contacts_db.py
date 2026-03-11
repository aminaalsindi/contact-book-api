import sqlite3

DB_NAME = "contacts.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL
        )
        """)
        conn.commit()


def get_all_contacts():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def add_contact(name, email, phone):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone)
        )
        conn.commit()
        return cursor.lastrowid


def get_contact(contact_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_contact(contact_id, name, email, phone):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contacts SET name = ?, email = ?, phone = ? WHERE id = ?",
            (name, email, phone, contact_id)
        )
        conn.commit()
        return cursor.rowcount


def delete_contact(contact_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        return cursor.rowcount


def search_contacts(query):
    with get_connection() as conn:
        cursor = conn.cursor()
        like_query = f"%{query}%"
        cursor.execute(
            "SELECT * FROM contacts WHERE name LIKE ? OR email LIKE ?",
            (like_query, like_query)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]