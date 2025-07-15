from app.database import Base, engine
from app.models import Todo

print("Creating tables...")
Base.metadata.create_all(bind=engine)
