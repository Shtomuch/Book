from typing import Optional

from src.core.exceptions import ConflictException, UnauthorizedException, ValidationException
from src.core.security import create_access_token, get_password_hash, verify_password
from src.domain.entities import User
from src.domain.repositories import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, email: str, username: str, password: str) -> User:
        self._validate_password(password)
        
        existing_email = await self.user_repository.get_by_email(email)
        if existing_email:
            raise ConflictException(f"User with email '{email}' already exists")
        
        existing_username = await self.user_repository.get_by_username(username)
        if existing_username:
            raise ConflictException(f"User with username '{username}' already exists")
        
        hashed_password = get_password_hash(password)
        user = User(
            id=None,
            email=email,
            username=username,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
        )
        
        return await self.user_repository.create(user)

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repository.get_by_username(username)
        if not user:
            user = await self.user_repository.get_by_email(username)
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            raise UnauthorizedException("User account is deactivated")
        
        return user

    async def create_token(self, user: User) -> str:
        return create_access_token(subject=str(user.id))

    async def get_current_user(self, user_id: int) -> Optional[User]:
        user = await self.user_repository.get_by_id(user_id)
        if not user or not user.is_active:
            return None
        return user

    def _validate_password(self, password: str) -> None:
        if len(password) < 8:
            raise ValidationException("Password must be at least 8 characters long")
        if not any(c.isupper() for c in password):
            raise ValidationException("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in password):
            raise ValidationException("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in password):
            raise ValidationException("Password must contain at least one digit")