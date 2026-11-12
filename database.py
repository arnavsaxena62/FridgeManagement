import sqlite3

DB_NAME = "recipes.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)


def add_ingredient(name):
    name = name.strip().lower()

    if not name:
        return False

    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT OR IGNORE INTO ingredients (name) VALUES (?)",
            (name,)
        )

        return cursor.rowcount > 0


def remove_ingredient(name):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM ingredients WHERE name = ?",
            (name.strip().lower(),)
        )

        return cursor.rowcount > 0


def get_ingredients():
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT name FROM ingredients ORDER BY name"
        )

        return [row[0] for row in cursor.fetchall()]