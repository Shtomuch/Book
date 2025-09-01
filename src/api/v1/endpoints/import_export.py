import csv
import json
from io import StringIO
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from src.api.dependencies import get_book_service, get_current_active_user
from src.api.v1.schemas import BookResponse
from src.core.exceptions import ConflictException, ValidationException
from src.domain.entities import Book, Genre, User
from src.domain.services import BookService

router = APIRouter(prefix="/import-export", tags=["import-export"])


@router.post("/import/json", response_model=list[BookResponse], status_code=status.HTTP_201_CREATED)
async def import_books_json(
    file: UploadFile = File(...),
    book_service: Annotated[BookService, Depends(get_book_service)] = None,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
) -> list[BookResponse]:
    if not file.filename.endswith('.json'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be JSON format"
        )
    
    try:
        content = await file.read()
        data = json.loads(content)
        
        if not isinstance(data, list):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="JSON must contain an array of books"
            )
        
        books = []
        for item in data:
            try:
                genre = Genre(item.get("genre"))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid genre: {item.get('genre')}"
                )
            
            book = Book(
                id=None,
                title=item.get("title"),
                author_id=item.get("author_id"),
                genre=genre,
                published_year=item.get("published_year"),
                isbn=item.get("isbn"),
                description=item.get("description"),
                created_at=None,
                updated_at=None,
            )
            books.append(book)
        
        created_books = await book_service.bulk_create_books(books)
        return [BookResponse.model_validate(book) for book in created_books]
    
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON format"
        )
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/import/csv", response_model=list[BookResponse], status_code=status.HTTP_201_CREATED)
async def import_books_csv(
    file: UploadFile = File(...),
    book_service: Annotated[BookService, Depends(get_book_service)] = None,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
) -> list[BookResponse]:
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be CSV format"
        )
    
    try:
        content = await file.read()
        csv_file = StringIO(content.decode('utf-8'))
        reader = csv.DictReader(csv_file)
        
        books = []
        for row in reader:
            try:
                genre = Genre(row.get("genre"))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid genre: {row.get('genre')}"
                )
            
            book = Book(
                id=None,
                title=row.get("title"),
                author_id=int(row.get("author_id")),
                genre=genre,
                published_year=int(row.get("published_year")),
                isbn=row.get("isbn") if row.get("isbn") else None,
                description=row.get("description") if row.get("description") else None,
                created_at=None,
                updated_at=None,
            )
            books.append(book)
        
        created_books = await book_service.bulk_create_books(books)
        return [BookResponse.model_validate(book) for book in created_books]
    
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid CSV data: {str(e)}"
        )
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/export/json")
async def export_books_json(
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> StreamingResponse:
    result = await book_service.get_books(page=1, size=10000)
    books = result["items"]
    
    export_data = [
        {
            "id": book.id,
            "title": book.title,
            "author_id": book.author_id,
            "genre": book.genre.value,
            "published_year": book.published_year,
            "isbn": book.isbn,
            "description": book.description,
        }
        for book in books
    ]
    
    json_str = json.dumps(export_data, indent=2, default=str)
    
    return StreamingResponse(
        StringIO(json_str),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=books_export.json"}
    )


@router.get("/export/csv")
async def export_books_csv(
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> StreamingResponse:
    result = await book_service.get_books(page=1, size=10000)
    books = result["items"]
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["id", "title", "author_id", "genre", "published_year", "isbn", "description"])
    
    for book in books:
        writer.writerow([
            book.id,
            book.title,
            book.author_id,
            book.genre.value,
            book.published_year,
            book.isbn or "",
            book.description or "",
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=books_export.csv"}
    )