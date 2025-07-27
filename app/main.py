from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from app import models, database
from app.schemas import Item, ItemCreate
from fastapi.requests import Request



# Main app
app = FastAPI()

dist_path = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if dist_path.exists():
    app.mount("/static", StaticFiles(directory=dist_path, html=True), name="static")
else:
    print("⚠️  DIST folder NOT found at", dist_path)

# 👇 Always define this route

api_router = APIRouter(prefix="/api", tags=["API"])

# CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api_router.get("/", response_model=dict)
def root():
    return {"message": "Hello, World"}

@api_router.post("/items", response_model=Item)
def create_todo(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Todo(text=item.text, is_done=item.is_done)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@api_router.get("/items", response_model=List[Item])
def read_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

@api_router.get("/items/{item_id}", response_model=Item)
def read_todo(item_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == item_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Not Found")
    return todo

# Mount API router to the main app
app.include_router(api_router)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    if full_path.startswith("api"):
        return JSONResponse(status_code=404, content={"detail": "API endpoint not found"})

    if dist_path.exists():
        return FileResponse(dist_path / "index.html")
    return JSONResponse(status_code=500, content={"detail": "Frontend not available"})


