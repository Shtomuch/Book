# Book Management System

### Core Features 
- **CRUD Operations**: Complete Create, Read, Update, Delete operations for books and authors
- **JWT Authentication**: Secure API with JWT-based authentication and bcrypt password hashing
- **Advanced Filtering**: Filter books by title, author, genre, and year range
- **Pagination & Sorting**: Built-in pagination with sorting by title, year, or author
- **Bulk Import**: Import multiple books from JSON or CSV files
- **Export Functionality**: Export book records in JSON or CSV format
- **Data Validation**: Comprehensive input validation with custom error messages
- **Error Handling**: Robust error handling with appropriate HTTP status codes

### Technical Features 
- **Clean Architecture**: Separation of concerns with Domain, Repository, Service, and API layers
- **Raw SQL Queries**: Direct PostgreSQL interactions using asyncpg
- **Normalized Database**: Separate tables for books and authors with relationships
- **Asynchronous Operations**: Full async/await support for high performance
- **Comprehensive Testing**: Unit and integration tests included
- **API Documentation**: Auto-generated Swagger UI and ReDoc documentation

##  Architecture

```
src/
├── api/                    # API Layer
│   ├── v1/
│   │   ├── endpoints/     # FastAPI routes
│   │   └── schemas/       # Pydantic models
│   ├── dependencies/      # Dependency injection
│   └── middleware/        # Exception handlers
├── core/                  # Core business logic
│   ├── config/           # Application settings
│   ├── exceptions/       # Custom exceptions
│   └── security/         # JWT and password handling
├── domain/               # Domain Layer
│   ├── entities/        # Business entities
│   ├── repositories/    # Repository interfaces
│   └── services/        # Business services
├── infrastructure/       # Infrastructure Layer
│   ├── database/        # Database connection
│   └── repositories/    # Repository implementations
└── tests/               # Test suite
```

##  Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Poetry (for dependency management)

##  Installation

### Local Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Book
```

2. **Install Poetry (if not installed):**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. **Install dependencies:**
```bash
poetry install
```

4. **Set up environment variables:**
```bash
cp .env.example .env
```

5. **Create PostgreSQL database:**
```bash
createdb bookdb
```

6. **Run database migrations:**
```bash
poetry run alembic upgrade head
```

7. **Start the application:**
```bash
poetry run uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

This will start both PostgreSQL and the FastAPI application.

##  API Documentation

Once the application is running, you can access:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

##  API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Books
- `GET /api/v1/books/` - Get all books (with pagination and filtering)
- `GET /api/v1/books/{id}` - Get a specific book
- `POST /api/v1/books/` - Create a new book (requires authentication)
- `PUT /api/v1/books/{id}` - Update a book (requires authentication)
- `DELETE /api/v1/books/{id}` - Delete a book (requires authentication)
- `POST /api/v1/books/bulk` - Bulk import books (requires authentication)

### Authors
- `GET /api/v1/authors/` - Get all authors (with pagination)
- `GET /api/v1/authors/{id}` - Get a specific author
- `POST /api/v1/authors/` - Create a new author (requires authentication)
- `PUT /api/v1/authors/{id}` - Update an author (requires authentication)
- `DELETE /api/v1/authors/{id}` - Delete an author (requires authentication)

### Import/Export
- `POST /api/v1/import-export/import/json` - Import books from JSON (requires authentication)
- `POST /api/v1/import-export/import/csv` - Import books from CSV (requires authentication)
- `GET /api/v1/import-export/export/json` - Export books as JSON
- `GET /api/v1/import-export/export/csv` - Export books as CSV

##  Testing

### Run all tests:
```bash
poetry run pytest
```

### Run with coverage:
```bash
poetry run pytest --cov=src --cov-report=html
```

### Run specific test file:
```bash
poetry run pytest src/tests/test_auth.py -v
```

##  Database Schema

### Authors Table
```sql
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    biography TEXT,
    birth_year INTEGER,
    nationality VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Books Table
```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(id),
    genre VARCHAR(50) NOT NULL,
    published_year INTEGER NOT NULL,
    isbn VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_published_year CHECK (
        published_year >= 1800 AND 
        published_year <= EXTRACT(YEAR FROM CURRENT_DATE)
    )
);
```

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

##  Available Commands

```bash

make install

make run

make test

make migrate

make docker-up

make docker-down

make clean
```

##  Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql+asyncpg://user:password@localhost:5432/bookdb` |
| `SECRET_KEY` | JWT secret key | `change-me-in-production` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `ENVIRONMENT` | Application environment | `development` |



##  Performance Considerations

- Asynchronous operations for better concurrency
- Connection pooling for database connections
- Indexed database columns for faster queries
- Pagination to limit data transfer
- Raw SQL queries for optimal performance
