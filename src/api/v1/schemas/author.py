from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    biography: Optional[str] = Field(None, max_length=5000)
    birth_year: Optional[int] = Field(None, ge=1000, le=2100)
    nationality: Optional[str] = Field(None, max_length=100)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return v.strip()


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AuthorPagination(BaseModel):
    items: list[AuthorResponse]
    total: int
    page: int
    size: int
    pages: int