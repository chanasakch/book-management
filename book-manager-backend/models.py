# ==========================
# Importing Libraries
# ==========================
from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

# ==========================
# Book Model
# ==========================
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)  # Primary key for book
    title = Column(String(255), nullable=False)  # Book title
    author = Column(String(255), nullable=False)  # Book author
    published_year = Column(Integer)  # Year the book was published
    genre = Column(String(100))  # Genre of the book
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Creation timestamp
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # Update timestamp

# ==========================
# User Model
# ==========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Primary key for user
    username = Column(String(50), unique=True, nullable=False, index=True)  # Unique username for user
    password = Column(String(255), nullable=False)  # User password
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Account creation timestamp
