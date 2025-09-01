from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies import get_book_service, get_current_active_user
from src.api.v1.schemas import (
    BookBulkCreate,
    BookCreate,
    BookPagination,
    BookResponse,
    BookUpdate,
)
from src.core.exceptions import ConflictException, NotFoundException, ValidationException
from src.domain.entities import Book, Genre, User
from src.domain.services import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    book_service: Annotated[BookService, Depends(get_book_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> BookResponse:
    try:
        book = Book(
            id=None,
            title=book_data.title,
            author_id=book_data.author_id,
            genre=book_data.genre,
            published_year=book_data.published_year,
            isbn=book_data.isbn,
            description=book_data.description,
            created_at=None,
            updated_at=None,
        )
        created_book = await book_service.create_book(book)
        return BookResponse.model_validate(created_book)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", response_model=BookPagination)
async def get_books(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 50,
    title: Optional[str] = None,
    author_id: Optional[int] = None,
    genre: Optional[Genre] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    sort_by: Optional[str] = Query(None, pattern="^(title|published_year|created_at|updated_at)$"),
    order: Annotated[str, Query(pattern="^(asc|desc)$")] = "asc",
    book_service: Annotated[BookService, Depends(get_book_service)] = None,
) -> BookPagination:
    result = await book_service.get_books(
        page=page,
        size=size,
        title=title,
        author_id=author_id,
        genre=genre.value if genre else None,
        year_from=year_from,
        year_to=year_to,
        sort_by=sort_by,
        order=order,
    )
    
    return BookPagination(
        items=[BookResponse.model_validate(book) for book in result["items"]],
        total=result["total"],
        page=result["page"],
        size=result["size"],
        pages=result["pages"],
    )


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> BookResponse:
    try:
        book = await book_service.get_book(book_id)
        return BookResponse.model_validate(book)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    book_service: Annotated[BookService, Depends(get_book_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> BookResponse:
    try:
        book = Book(
            id=book_id,
            title=book_data.title,
            author_id=book_data.author_id,
            genre=book_data.genre,
            published_year=book_data.published_year,
            isbn=book_data.isbn,
            description=book_data.description,
            created_at=None,
            updated_at=None,
        )
        updated_book = await book_service.update_book(book_id, book)
        return BookResponse.model_validate(updated_book)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    book_service: Annotated[BookService, Depends(get_book_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> None:
    try:
        await book_service.delete_book(book_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/bulk", response_model=list[BookResponse], status_code=status.HTTP_201_CREATED)
async def bulk_create_books(
    bulk_data: BookBulkCreate,
    book_service: Annotated[BookService, Depends(get_book_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> list[BookResponse]:
    try:
        books = [
            Book(
                id=None,
                title=book_data.title,
                author_id=book_data.author_id,
                genre=book_data.genre,
                published_year=book_data.published_year,
                isbn=book_data.isbn,
                description=book_data.description,
                created_at=None,
                updated_at=None,
            )
            for book_data in bulk_data.books
        ]
        created_books = await book_service.bulk_create_books(books)
        return [BookResponse.model_validate(book) for book in created_books]
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))