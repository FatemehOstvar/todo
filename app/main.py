from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# import os
# DB_URL = os.environ["DATABASE_URL"]


class Item(BaseModel):
    text: str = None
    is_done: bool = False

app = FastAPI()
items = []

# defining a path in fastapi
@app.get("/", response_model= dict)
def root():
    return {"Hello": "World"}

@app.post("/items", response_model= Item)
def todo(item : Item):
    items.append(item)
    return items


@app.get("/items", response_model=list[Item])
def search_todo(item_id : int) -> List:
    try:
        return items[item_id]
    except "e":
        raise HTTPException(status_code=404,detail="Not Found")

def get_todo() -> List:
    return items[:]

