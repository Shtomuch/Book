from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    email: str
    username: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None