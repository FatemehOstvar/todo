# app/schemas.py (or just schemas.py if small project)
from pydantic import BaseModel

# Common base
class ItemBase(BaseModel):
    text: str
    is_done: bool = False

# For incoming requests (e.g. POST)
class ItemCreate(ItemBase):
    pass

# For responses (includes `id` from DB)
class Item(ItemBase):
    id: int

    model_config = {
        "from_attributes": True  # Pydantic v2 replacement for orm_mode
    }
