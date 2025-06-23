# Importing necessary functions and classes from SQLAlchemy
from sqlalchemy import create_engine  # To create a connection to the database
from sqlalchemy.orm import declarative_base  # For creating base class for models
from sqlalchemy.orm import sessionmaker  # For creating session to interact with the DB

# ==========================
# Database URL Configuration
# ==========================
DATABASE_URL = "sqlite:///./books.db"  # URL of the database (SQLite in this case)

# ==========================
# Creating the Database Engine
# ==========================
engine = create_engine(
    DATABASE_URL,  # Use the DATABASE_URL defined above
    connect_args={"check_same_thread": False}  # Ensure thread safety for SQLite
)

# ==========================
# SessionLocal Configuration
# ==========================
SessionLocal = sessionmaker(
    bind=engine,        # The engine to bind the session to
    autoflush=False,    # Don't auto-flush after every transaction
    autocommit=False    # Don't auto-commit after each transaction
)

# ==========================
# Base class for models
# ==========================
Base = declarative_base()  # Base class that all models will inherit from
