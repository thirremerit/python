from fastapi import FastAPI,HTTPException, Depends

from fastapi.security import APIKeyHeader

from pydantic import BaseModel

from typing import Optional
from dotenv import load_dontenv
import os
from app.database import get_db, init_db

load_dotenv()

app=FastAPI()
init_db()

api_key_header =  APIKeyHeader(name="api-key")

def check_key(key:str = Depends(api_key_header)):
    allowed_keys = os.getenv("API_KEYS").split(",")
    if not key or key not in allowed_keys:
        raise HTTPException(401,"Invalid API Key")


class Item(BaseModel):
    name:str
    description:Optional[str]=None


@app.post("/items", dependencies=[Depends(check_key())])
def create_item(item:Item):
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO items(names,description) VALUES)(?,?)",
            (item.name, item.description)
        )
        return {"id":cursor.lastrowid, **item.mode_dump()}
