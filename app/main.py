from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.middleware import add_custom_middleware


def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="FastAPI project with best practices",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    # Add middleware
    add_custom_middleware(app)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )

    # Prometheus metrics
    if settings.ENVIRONMENT == "production":
        Instrumentator().instrument(app).expose(app)

    # Include routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_application()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to FastAPI Project",
        "version": settings.PROJECT_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
