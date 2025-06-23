# ==========================
# Importing Libraries
# ==========================
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic.config import ConfigDict

# --------------------
# Book Schemas
# --------------------

class BookBase(BaseModel):
    title: str
    author: str
    published_year: Optional[int] = None
    genre: Optional[str] = None

class BookCreate(BookBase):
    pass  # Used when creating a new book

class BookUpdate(BookBase):
    pass  # Used for updating book details

class BookOut(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # Use from_attributes to serialize models to Pydantic models
    model_config = ConfigDict(from_attributes=True)

class PaginatedBooks(BaseModel):
    data: list[BookOut]
    total: int  # Used for paginated results (list of books with total count)

# --------------------
# User Schemas
# --------------------

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    # Use from_attributes to serialize models to Pydantic models
    model_config = ConfigDict(from_attributes=True)
