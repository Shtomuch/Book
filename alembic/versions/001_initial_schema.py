"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            biography TEXT,
            birth_year INTEGER,
            nationality VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute("CREATE INDEX idx_authors_name ON authors(name)")
    
    op.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            author_id INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
            genre VARCHAR(50) NOT NULL,
            published_year INTEGER NOT NULL,
            isbn VARCHAR(20),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT chk_published_year CHECK (published_year >= 1800 AND published_year <= EXTRACT(YEAR FROM CURRENT_DATE))
        )
    """)
    
    op.execute("CREATE INDEX idx_books_title ON books(title)")
    op.execute("CREATE INDEX idx_books_author_id ON books(author_id)")
    op.execute("CREATE INDEX idx_books_genre ON books(genre)")
    op.execute("CREATE INDEX idx_books_published_year ON books(published_year)")
    op.execute("CREATE INDEX idx_books_isbn ON books(isbn)")
    
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            is_superuser BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    op.execute("CREATE INDEX idx_users_email ON users(email)")
    op.execute("CREATE INDEX idx_users_username ON users(username)")
    
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql'
    """)
    
    op.execute("""
        CREATE TRIGGER update_authors_updated_at BEFORE UPDATE ON authors
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()
    """)
    
    op.execute("""
        CREATE TRIGGER update_books_updated_at BEFORE UPDATE ON books
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()
    """)
    
    op.execute("""
        CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS books CASCADE")
    op.execute("DROP TABLE IF EXISTS authors CASCADE")
    op.execute("DROP TABLE IF EXISTS users CASCADE")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE")