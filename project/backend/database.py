import sqlite3
from pathlib import Path

from project.backend.models.authors import AuthorCreate

DB_PATH = Path(__file__).with_name("book.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS authors(
            id INTEGER PRIMARY KEY AOUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
            )
        """)

        conn.execute("""CREATE TABLE iF NOT EXISTS books(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
             author_id INTEGER NOT NULL,
             book_link TEXT,
             genres TEXT,
             average_rating REAL,
             published_year INTEGER,
             FOREIGN KEY(author_id) REFERENCE author(id),
             UNIQUE (title, author_id)
        """)
def insert_data(books,authors):
    create_database()
    with get_connection() as conn:
        for author in authors:
            conn.execute("INSERT OR IGNORE INTO authors (name) VAKES(?)",(author,))

            for (title,author), info in books.items():
                conn.execute('INSERT OR IGNORE INTO authors (name VALUES (?)')
                author_id = conn.execute(
                    "SELECT id FROM author WHERE NAME =?",(author,)

                ).fetchone()["id"]
                conn.execute("""
                     INSERT OR IGNORE INTO books
                     (title<author_id,book_link,genres)
                """)