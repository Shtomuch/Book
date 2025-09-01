# Book Management System

FastAPI-based book management system with Clean Architecture, PostgreSQL, and JWT authentication.

## Features

- CRUD operations for books and authors
- JWT-based authentication
- Pagination and filtering
- Bulk import from JSON/CSV
- Clean Architecture with Repository Pattern
- Raw SQL queries with asyncpg
- Comprehensive test coverage

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Poetry (for dependency management)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd book-management-system
```

2. Install dependencies:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run database migrations:
```bash
poetry run alembic upgrade head
```

5. Start the application:
```bash
poetry run uvicorn src.main:app --reload
```

## API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with:
```bash
poetry run pytest
```

With coverage:
```bash
poetry run pytest --cov=src
```

## Docker

Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Architecture

The project follows Clean Architecture principles:

- **Domain Layer**: Business entities and rules
- **Repository Layer**: Data access with raw SQL
- **Service/Use Case Layer**: Business logic
- **API Layer**: FastAPI routes and schemas
- **Infrastructure Layer**: Database connections and external services