"""Create and fill a small SQLite database."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("books.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_database():
    with get_connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            book_link TEXT,
            genres TEXT,
            average_rating REAL,
            published_year INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            UNIQUE (title, author_id)
        )""")


def insert_data(books, authors):
    create_database()
    with get_connection() as conn:
        for author in authors:
            conn.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (author,))
        for (title, author), info in books.items():
            conn.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (author,))
            author_id = conn.execute(
                "SELECT id FROM authors WHERE name = ?", (author,)
            ).fetchone()["id"]
            conn.execute("""INSERT OR IGNORE INTO books
                (title, author_id, book_link, genres, average_rating, published_year)
                VALUES (?, ?, ?, ?, ?, ?)""", (
                    title, author_id, info["link"], ", ".join(info["genres"]),
                    info["avg_rating"], info["published"]
                ))


if __name__ == "__main__":
    from books_scraper import scrape_books
    books, authors = scrape_books()
    insert_data(books, authors)
    print(f"Saved {len(books)} books to {DB_PATH}")
