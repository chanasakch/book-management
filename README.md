Book Manager Web Application

Table of Contents
1. Overview
2. Installation
3. Frontend Setup
4. Backend Setup
5. Running the Application
6. Testing
7. Features Implemented
8. Database Schema
9. API Documentation
10. License

Overview
This is a full-stack web application designed to manage a collection of books for a company.
    It allows users to perform CRUD operations on books stored in a database and provides an intuitive 
    user interface (UI) with API integration for the backend.

    The application is built using the following technologies:

    - **Frontend**: Vue.js (with Vue Router), SCSS for styling
    - **Backend**: FastAPI, SQLAlchemy, SQLite
    - **Authentication**: JWT-based authentication for secure access to API endpoints
    - **Database**: SQLite (used for storage of books and users)

    The application allows users to:
    1. Add books to the system
    2. Fetch a list of books
    3. Edit book details
    4. Delete books from the system
    
Installation
### Prerequisites

    Before running this application, make sure you have the following installed:

    - Python 3.7 or higher
    - Node.js and npm (for frontend)
    - SQLite (pre-configured, but can be installed if not present)

    ### Clone the Repository

    Clone the repository to your local machine using Git:

    ```bash
    git clone https://github.com/chanasakch/book-manager.git
    cd book-manager
    ```

    ### Install Backend Dependencies

    Navigate to the `backend` directory and install the required Python packages using `pip`:

    ```bash
    cd backend
    pip install -r requirements.txt
    ```

    ### Install Frontend Dependencies

    Navigate to the `frontend` directory and install the required JavaScript packages using npm:

    ```bash
    cd frontend
    npm install
    ```
    
Frontend Setup
### Starting the Frontend

    Once the frontend dependencies are installed, you can run the frontend application:

    ```bash
    cd frontend
    npm run serve
    ```

    This will start a development server for the frontend, typically accessible at `http://localhost:8080`.

    ### Files

    - **Login.vue**: The login page component.
    - **HomeView.vue**: The main page where books can be managed (add, edit, delete).
    - **auth.ts**: Utility functions to handle JWT authentication.
    - **bookApi.ts**: API service for interacting with the backend.
    - **router/index.ts**: Vue Router configuration.
    
Backend Setup
### Running the Backend

    To start the backend server, navigate to the `backend` directory and run the following command:

    ```bash
    cd backend
    uvicorn main:app --reload
    ```

    This will start the FastAPI server at `http://localhost:8000`. The `--reload` option allows you to see changes without restarting the server.

    ### Database Schema

    The backend uses SQLite for data storage, and the database is automatically created with the `books.db` file included in the project.

    The database schema for the `books` table is as follows:

    ```sql
    CREATE TABLE books (
      id INTEGER PRIMARY KEY,
      title VARCHAR(255) NOT NULL,
      author VARCHAR(255) NOT NULL,
      published_year INTEGER,
      genre VARCHAR(100),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

    Additionally, the `users` table is required for user authentication, but it is not created automatically. You will need to create the table manually by running the following SQL query in an SQLite client:

    ```sql
    CREATE TABLE users (
      id INTEGER PRIMARY KEY,
      username VARCHAR(50) UNIQUE NOT NULL,
      password VARCHAR(255) NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

    ### API Authentication

    The application uses JWT for authentication. You can register a new user by sending a POST request to `/register` with a username and password. Once registered, you can log in at `/login` to receive a JWT token. This token should be used for authorized API requests.

    ### Running the Backend

    Make sure you have `SQLite` set up correctly and the database (`books.db`) file is present in the `backend` folder. If the `users` table is missing, you will need to create the table manually using the SQL query mentioned above.
    
Running the Application
### Frontend

    1. Start the frontend server as mentioned above.
    2. The frontend application should now be available at `http://localhost:8080`.
    3. Use the login page to log in or register a new user.

    ### Backend

    1. Start the backend server with `uvicorn main:app --reload`.
    2. The backend application should now be available at `http://localhost:8000`.
    3. Use API endpoints to interact with the book data.
    
Testing
To run the tests, navigate to the `backend` directory and run:

    ```bash
    cd backend
    pytest -v
    ```

    The tests will validate the following functionalities:

    - User authentication (register/login)
    - CRUD operations on books
    - Pagination
    - Error handling and toast messages
    
Features Implemented
1. **Authentication (JWT)**: 
       - The app uses JWT to secure the API. After logging in, users receive a token that is stored in local storage and sent with each API request.

    2. **Responsive Design (Mobile-friendly)**: 
       - The frontend uses Tailwind CSS (with SCSS) to ensure the app is responsive and works well on mobile devices.

    3. **Pagination**: 
       - The list of books is paginated. Users can select how many books to display per page and navigate between pages.

    4. **Loading/Error State**: 
       - The app displays a loading message while fetching data and an error message if something goes wrong.

    5. **Logging and Error Handling**: 
       - All actions such as user registration, login, and CRUD operations on books are logged. Any errors are captured and displayed using toast messages.

    6. **Unit Test**: 
       - Unit tests are implemented for all major functions, including user registration, login, and CRUD operations on books.

    7. **API Documentation**: 
       - The FastAPI backend includes auto-generated interactive API documentation at `/docs` where users can see all the endpoints and test them directly.
    
Database Schema
The database schema is structured as follows:

    **Books Table**:

    ```sql
    CREATE TABLE books (
      id INTEGER PRIMARY KEY,
      title VARCHAR(255) NOT NULL,
      author VARCHAR(255) NOT NULL,
      published_year INTEGER,
      genre VARCHAR(100),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

    **Users Table** (Manually created):

    ```sql
    CREATE TABLE users (
      id INTEGER PRIMARY KEY,
      username VARCHAR(50) UNIQUE NOT NULL,
      password VARCHAR(255) NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```
    
API Documentation
The API documentation for this project is auto-generated by FastAPI and can be accessed at the following URL:

    `http://localhost:8000/docs`

    This interactive documentation allows you to view and test all the available API endpoints.
    
License
This project is licensed under the MIT License - see the LICENSE file for details.
    
