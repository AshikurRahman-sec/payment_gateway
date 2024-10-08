
# Payment Gateway API

This is a backend API for a Payment Gateway system built with FastAPI. The project is structured to ensure scalability, separation of concerns, and easy maintainability.

## Project Structure

```bash
payment_gateway/
│
├── app/
│   ├── api.py          # Contains all the API route definitions and endpoint logic
│   ├── crud.py         # Handles CRUD operations for the database (Create, Read, Update, Delete)
│   ├── database.py     # Configures the database connection and session handling
│   ├── main.py         # The entry point of the FastAPI application
│   ├── model.py        # Defines the database models (SQLAlchemy models)
│   ├── schemas.py      # Defines the Pydantic schemas for request and response validation
│   ├── security.py     # Handles security features such as password hashing and JWT token generation
```

### File Descriptions:

- **api.py**:  
  This file defines the various API endpoints using FastAPI’s routing mechanisms. It connects HTTP requests to the appropriate CRUD operations.

- **crud.py**:  
  This file contains the logic for interacting with the database. It includes functions for creating, reading, updating, and deleting entries from the database.

- **database.py**:  
  This file sets up the database connection using SQLAlchemy. It also provides a session management mechanism for database transactions.

- **main.py**:  
  This is the main entry point for running the FastAPI application. It initializes the app and includes middleware, routes, and configuration settings.

- **model.py**:  
  This file defines the database models using SQLAlchemy ORM. These models represent the structure of the database tables.

- **schemas.py**:  
  Pydantic models used for data validation and serialization. These schemas define the structure of incoming requests and outgoing responses.

- **security.py**:  
  This file contains functions for handling authentication and security, such as password hashing and JWT token creation and verification.

## Environment Variables

You need to create a `.env` file in the root of the project to configure environment variables. This file will store sensitive information like the database URL and secret keys.

### Sample `.env` file:

```bash
DATABASE_URL=mysql+pymysql://<username>:<password>@<host>/<database_name>
SECRET_KEY=<your-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- `DATABASE_URL`: The connection URL for your MySQL database.
- `SECRET_KEY`: A secret key used for encrypting the JWT tokens.
- `ALGORITHM`: The algorithm used for encrypting tokens (usually HS256).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: The lifespan of the access token.

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/payment_gateway.git
cd payment_gateway
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 3. Install Required Libraries

Make sure you have `pip` installed. Add the necessary libraries to the requirements.txt file. Then, install the necessary dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with the required environment variables as described above.

### 5. Run Database Migrations (Optional)

### 6. Run the Application

To start the FastAPI server, run:

```bash
uvicorn app.main:app --reload
```

The API will now be running at `http://127.0.0.1:8000`.

## API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can visit:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)


