from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Author:
    id: Optional[int]
    name: str
    biography: Optional[str]
    birth_year: Optional[int]
    nationality: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]