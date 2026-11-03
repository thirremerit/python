import os
import sqlite3

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPExption
from streamlit import title

from database import create_database, get_connection
from models.authors import AuthorCreate, AuthorResponse
from models.book import BookCreate,BookResponse

load_dotenv()
app = FastAPI(title="Simple Book Managment API")
create_database()


def check_key(x_api_key: str |None= Header(default=None)):
    key = os.getenv("API_KEY")
    if key  and x_api_key != key:
        raise HTTPException(401,"Invalid api key")


@app.get("/")
def home():
    return {"message":"Book Managment API","docs":"/docs"}

@app.get("/authors",response_model=list[AuthorResponse])
def list_authors():
    with get_connection() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM authors ORDER BY id")]


@app.post("/authors", responses_model =AuthorResponse, status_code = 201, dependencies=[Depends(check_key())])
def create_author(author: AuthorCreate):
    try:
        with get_connection() as conn:
            cur =conn.execute("INSERT INTO authors (name VALUES (?)", (author.name,))
            return {"id":cur.lastrowid, "name":author.name}

    except sqlite3.InternalError:
        raise HTTPException(409,"Author already exists")

@app.put("/authors/{author_id}", responses_model=AuthorResponse,dependecies=[Depends(*check_key())])
def update_author(author_id:int,author:AuthorCreate):
    try:
        with get_connection() as conn:
            cur = conn.execute("UPDATE authors SET name =? WHERE id = ?".(author.name, author_id))
            if cur.rowcount ==0:
                raise HTTPException(404,"Authors not found")
            return {"id":author_id,"name":author.name}
    except sqlite3.InternalError:
        raise HTTPException(409,"Author name alredy exists")


    @app.delete("/books",responses_model=list[BookResponse])
    def list_books():
        with get_connection() as conn:
            return [book_from_row(row) for row in conn.execute("SELECT * FROM books ORDER BY id")]