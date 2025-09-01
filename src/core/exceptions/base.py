from typing import Any, Optional


class DomainException(Exception):
    def __init__(self, message: str, code: Optional[str] = None) -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundException(DomainException):
    def __init__(self, entity: str, entity_id: Any) -> None:
        super().__init__(f"{entity} with id {entity_id} not found", "NOT_FOUND")
        self.entity = entity
        self.entity_id = entity_id


class ValidationException(DomainException):
    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field


class ConflictException(DomainException):
    def __init__(self, message: str) -> None:
        super().__init__(message, "CONFLICT")


class UnauthorizedException(DomainException):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message, "UNAUTHORIZED")


class ForbiddenException(DomainException):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message, "FORBIDDEN")