import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from loguru import logger


async def log_requests_middleware(request: Request, call_next: Callable) -> Response:
    """Log all requests with timing information."""
    start_time = time.time()
    
    # Log request
    logger.info(
        f"Request: {request.method} {request.url.path} - "
        f"Client: {request.client.host if request.client else 'unknown'}"
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    process_time = time.time() - start_time
    
    # Log response
    logger.info(
        f"Response: {response.status_code} - "
        f"Duration: {process_time:.4f}s"
    )
    
    # Add timing header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


def add_custom_middleware(app: FastAPI) -> None:
    """Add custom middleware to the FastAPI application."""
    app.middleware("http")(log_requests_middleware)