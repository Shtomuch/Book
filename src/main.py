from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.middleware import (
    domain_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.api.v1.endpoints import api_router
from src.core.config import settings
from src.core.exceptions import DomainException
from src.infrastructure.database import DatabasePool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabasePool.initialize()
    yield
    await DatabasePool.close()


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return {
        "message": "Book Management System API",
        "version": settings.version,
        "docs": f"{settings.api_v1_prefix}/docs",
        "redoc": f"{settings.api_v1_prefix}/redoc",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}