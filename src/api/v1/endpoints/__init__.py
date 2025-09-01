from fastapi import APIRouter

from .auth import router as auth_router
from .authors import router as authors_router
from .books import router as books_router
from .import_export import router as import_export_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(books_router)
api_router.include_router(authors_router)
api_router.include_router(import_export_router)