from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies import get_author_service, get_current_active_user
from src.api.v1.schemas import (
    AuthorCreate,
    AuthorPagination,
    AuthorResponse,
    AuthorUpdate,
)
from src.core.exceptions import ConflictException, NotFoundException, ValidationException
from src.domain.entities import Author, User
from src.domain.services import AuthorService

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
async def create_author(
    author_data: AuthorCreate,
    author_service: Annotated[AuthorService, Depends(get_author_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> AuthorResponse:
    try:
        author = Author(
            id=None,
            name=author_data.name,
            biography=author_data.biography,
            birth_year=author_data.birth_year,
            nationality=author_data.nationality,
            created_at=None,
            updated_at=None,
        )
        created_author = await author_service.create_author(author)
        return AuthorResponse.model_validate(created_author)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", response_model=AuthorPagination)
async def get_authors(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 50,
    name: Optional[str] = None,
    nationality: Optional[str] = None,
    author_service: Annotated[AuthorService, Depends(get_author_service)] = None,
) -> AuthorPagination:
    result = await author_service.get_authors(
        page=page,
        size=size,
        name=name,
        nationality=nationality,
    )
    
    return AuthorPagination(
        items=[AuthorResponse.model_validate(author) for author in result["items"]],
        total=result["total"],
        page=result["page"],
        size=result["size"],
        pages=result["pages"],
    )


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_id: int,
    author_service: Annotated[AuthorService, Depends(get_author_service)],
) -> AuthorResponse:
    try:
        author = await author_service.get_author(author_id)
        return AuthorResponse.model_validate(author)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: int,
    author_data: AuthorUpdate,
    author_service: Annotated[AuthorService, Depends(get_author_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> AuthorResponse:
    try:
        author = Author(
            id=author_id,
            name=author_data.name,
            biography=author_data.biography,
            birth_year=author_data.birth_year,
            nationality=author_data.nationality,
            created_at=None,
            updated_at=None,
        )
        updated_author = await author_service.update_author(author_id, author)
        return AuthorResponse.model_validate(updated_author)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    author_id: int,
    author_service: Annotated[AuthorService, Depends(get_author_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> None:
    try:
        await author_service.delete_author(author_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))