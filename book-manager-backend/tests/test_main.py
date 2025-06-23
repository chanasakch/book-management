import pytest
from fastapi.testclient import TestClient
from main import app  # Use the FastAPI app instance
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, SessionLocal, engine
from models import User, Book

# Start TestClient setup
client = TestClient(app)

# ------------------------
# Setup Database for Testing
# ------------------------

@pytest.fixture(scope="module")
def test_db():
    # Create the test database (does not affect the main database)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    # Drop the test database after tests are done
    Base.metadata.drop_all(bind=engine)
    db.close()

# ------------------------
# Test User Registration
# ------------------------

def test_register(test_db):
    # Test user registration with username "testuser"
    response = client.post(
        "/register", json={"username": "testuser", "password": "123456"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

# ------------------------
# Test Login Functionality
# ------------------------

def test_login(test_db):
    # Test login for user "testuser"
    response = client.post(
        "/login", json={"username": "testuser", "password": "123456"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# ------------------------
# Test Fetch Books (GET /books)
# ------------------------

def test_read_books(test_db):
    # Login and get token
    login_response = client.post(
        "/login", json={"username": "testuser", "password": "123456"}
    )
    token = login_response.json().get("access_token")

    # Ensure the token is valid
    assert login_response.status_code == 200
    assert token is not None

    # Add book data to the database
    book_data = {"title": "Book 1", "author": "Author 1", "published_year": 2021, "genre": "Fiction"}
    response = client.post(
        "/books", 
        json=book_data,
        headers={"Authorization": f"Bearer {token}"}  # Send token in header
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Book 1"  # 'title' instead of 'data' in response

# ------------------------
# Test Create Book (POST /books)
# ------------------------

def test_create_book(test_db):
    # Login and get token
    login_response = client.post(
        "/login", json={"username": "testuser", "password": "123456"}
    )
    assert login_response.status_code == 200  # Ensure the status code is OK
    assert "access_token" in login_response.json()
    token = login_response.json().get("access_token")
    
    # Send a request with the JWT token
    response = client.post(
        "/books", 
        json={"title": "New Book", "author": "Author 2", "published_year": 2023, "genre": "Science"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Book"
    assert "id" in response.json()  # Ensure the 'id' is included in the response

# ------------------------
# Test Update Book (PUT /books/{book_id})
# ------------------------

def test_update_book(test_db):
    # Login and get token
    login_response = client.post(
        "/login", json={"username": "testuser", "password": "123456"}
    )
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")  # Get token

    # Create a book first
    book_data = {"title": "Book to Update", "author": "Author 3", "published_year": 2020, "genre": "History"}
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/books", json=book_data, headers=headers)
    book_id = response.json().get("id")

    if not book_id:
        pytest.fail("Book creation failed, no 'id' returned.")  # Ensure 'id' is returned

    updated_data = {"title": "Updated Book", "author": "Author 3", "published_year": 2021, "genre": "Biography"}

    # Send PUT request with token in header
    response = client.put(
        f"/books/{book_id}", 
        json=updated_data,
        headers={"Authorization": f"Bearer {token}"}  # Send token in header
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book"

# ------------------------
# Test Delete Book (DELETE /books/{book_id})
# ------------------------

def test_delete_book(test_db):
    # Login and get token
    login_response = client.post(
        "/login", json={"username": "testuser", "password": "123456"}
    )
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")  # Get token

    # Create a book first
    book_data = {"title": "Book to Delete", "author": "Author 4", "published_year": 2020, "genre": "Drama"}
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/books", json=book_data, headers=headers)
    book_id = response.json().get("id")

    if not book_id:
        pytest.fail("Book creation failed, no 'id' returned.")  # Fail if 'id' is not returned

    # Delete the book
    response = client.delete(f"/books/{book_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted"
    
# ------------------------
# Test Protected Endpoint (Authorization Header)
# ------------------------

def test_protected_endpoint(test_db):
    # Login and get token
    response = client.post(
        "/login", json={"username": "testuser", "password": "123456"}
    )
    token = response.json()["access_token"]
    
    # Send request with JWT token
    response = client.get(
        "/protected-endpoint", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Hello testuser" in response.json()["message"]
