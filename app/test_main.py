from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base

# ✔ Create an in-memory SQLite test DB
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"  # use ":memory:" for true temp, but needs extra tweak

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables for the test DB
Base.metadata.create_all(bind=engine)

# Override the `get_db` dependency with test DB session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Now define an actual test
def test_create_todo():
    response = client.post(
        "/items",
        json={"text": "learn testing", "is_done": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "learn testing"
    assert data["is_done"] == False
    assert "id" in data


def test_read_all_todos():
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["text"] == "learn testing" for item in data)


def test_read_single_todo():
    # First, create the todo_item
    create_response = client.post(
        "/items",
        json={"text": "learn testing", "is_done": False}
    )
    assert create_response.status_code == 200
    created = create_response.json()
    created_id = created["id"]

    # Then, fetch that specific todo by ID
    response = client.get(f"/items/{created_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["text"] == "learn testing"
    assert data["is_done"] is False
    assert data["id"] == created_id
