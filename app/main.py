from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from app import models, database
from app.schemas import Item, ItemCreate

app = FastAPI()


# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=dict)
def root():
    return {"Hello": "World"}


@app.post("/items", response_model=Item)
def create_todo(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Todo(text=item.text, is_done=item.is_done)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



@app.get("/items", response_model=List[Item])
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return todos


@app.get("/items/{item_id}", response_model=Item)
def read_todo(item_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == item_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Not Found")
    return todo
