"""Run with: uvicorn main:app --reload"""
import os
import sqlite3

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException

from database import create_database, get_connection
from models.author import AuthorCreate, AuthorResponse
from models.book import BookCreate, BookResponse

load_dotenv()
app = FastAPI(title="Simple Book Management API")
create_database()


def check_key(x_api_key: str | None = Header(default=None)):
    key = os.getenv("API_KEY")
    if key and x_api_key != key:
        raise HTTPException(401, "Invalid API key")


def book_from_row(row):
    return {**dict(row), "genres": row["genres"].split(", ") if row["genres"] else []}


@app.get("/")
def home():
    return {"message": "Book Management API", "docs": "/docs"}


@app.get("/authors", response_model=list[AuthorResponse])
def list_authors():
    with get_connection() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM authors ORDER BY id")]


@app.post("/authors", response_model=AuthorResponse, status_code=201, dependencies=[Depends(check_key)])
def create_author(author: AuthorCreate):
    try:
        with get_connection() as conn:
            cur = conn.execute("INSERT INTO authors (name) VALUES (?)", (author.name,))
            return {"id": cur.lastrowid, "name": author.name}
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Author already exists")


@app.put("/authors/{author_id}", response_model=AuthorResponse, dependencies=[Depends(check_key)])
def update_author(author_id: int, author: AuthorCreate):
    try:
        with get_connection() as conn:
            cur = conn.execute("UPDATE authors SET name = ? WHERE id = ?", (author.name, author_id))
            if cur.rowcount == 0:
                raise HTTPException(404, "Author not found")
            return {"id": author_id, "name": author.name}
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Author name already exists")


@app.delete("/authors/{author_id}", dependencies=[Depends(check_key)])
def delete_author(author_id: int):
    with get_connection() as conn:
        try:
            cur = conn.execute("DELETE FROM authors WHERE id = ?", (author_id,))
        except sqlite3.IntegrityError:
            raise HTTPException(409, "Delete this author's books first")
        if cur.rowcount == 0:
            raise HTTPException(404, "Author not found")
    return {"message": "Author deleted"}


@app.get("/books", response_model=list[BookResponse])
def list_books():
    with get_connection() as conn:
        return [book_from_row(row) for row in conn.execute("SELECT * FROM books ORDER BY id")]


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if row is None:
        raise HTTPException(404, "Book not found")
    return book_from_row(row)


@app.post("/books", response_model=BookResponse, status_code=201, dependencies=[Depends(check_key)])
def create_book(book: BookCreate):
    try:
        with get_connection() as conn:
            cur = conn.execute("""INSERT INTO books
                (title, author_id, book_link, genres, average_rating, published_year)
                VALUES (?, ?, ?, ?, ?, ?)""", (
                book.title, book.author_id, book.book_link,
                ", ".join(book.genres), book.average_rating, book.published_year
            ))
            row = conn.execute("SELECT * FROM books WHERE id = ?", (cur.lastrowid,)).fetchone()
            return book_from_row(row)
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Book already exists or author ID is invalid")


@app.put("/books/{book_id}", response_model=BookResponse, dependencies=[Depends(check_key)])
def update_book(book_id: int, book: BookCreate):
    try:
        with get_connection() as conn:
            cur = conn.execute("""UPDATE books SET title=?, author_id=?, book_link=?,
                genres=?, average_rating=?, published_year=? WHERE id=?""", (
                book.title, book.author_id, book.book_link, ", ".join(book.genres),
                book.average_rating, book.published_year, book_id
            ))
            if cur.rowcount == 0:
                raise HTTPException(404, "Book not found")
            row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
            return book_from_row(row)
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Duplicate book or invalid author ID")


@app.delete("/books/{book_id}", dependencies=[Depends(check_key)])
def delete_book(book_id: int):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        if cur.rowcount == 0:
            raise HTTPException(404, "Book not found")
    return {"message": "Book deleted"}
