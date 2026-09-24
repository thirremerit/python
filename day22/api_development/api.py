from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class User(BaseModel):
    id: int
    name:str
    age:int
    email:str


class User(BaseModel):
    age: int
    name:str

class PersonResponse(BaseModel):
    message:str

@app.post("/users/")
async def create_user(user:User):
    return user
