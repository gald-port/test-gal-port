"""
main.py
-------
Main entry point for the FastAPI server.

Install:
    pip install fastapi uvicorn

Run:
    python main.py

Or:
    uvicorn main:app --reload
"""

from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


# ============================================================
# Configuration
# ============================================================

HOST = "0.0.0.0"
PORT = 8000
DEBUG = True


# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("server")


# ============================================================
# Application Lifecycle
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs when the application starts and stops.

    This is a good place to initialize:
    - Database connections
    - Redis
    - External services
    - ML models
    - Background resources
    """

    logger.info("Starting server...")

    # Startup
    app.state.started_at = time.time()

    yield

    # Shutdown
    logger.info("Shutting down server...")


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="My Server",
    description="FastAPI server",
    version="1.0.0",
    debug=DEBUG,
    lifespan=lifespan,
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request Logging Middleware
# ============================================================

@app.middleware("http")
async def request_logger(request: Request, call_next):
    """
    Logs every incoming HTTP request.
    """

    start = time.perf_counter()

    try:
        response = await call_next(request)

        duration = (time.perf_counter() - start) * 1000

        logger.info(
            "%s %s -> %s (%.2fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = (time.perf_counter() - start) * 1000

        logger.exception(
            "Unhandled error: %s %s (%.2fms)",
            request.method,
            request.url.path,
            duration,
        )

        raise


# ============================================================
# Global Exception Handler
# ============================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handles unexpected server errors.
    """

    logger.exception(
        "Unhandled exception on %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
        },
    )


# ============================================================
# Root Endpoint
# ============================================================

@app.get("/")
async def root() -> dict[str, Any]:
    """
    Basic server information.
    """

    return {
        "success": True,
        "message": "Server is running",
        "version": app.version,
    }


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
async def health() -> dict[str, Any]:
    """
    Returns the current server health status.
    """

    started_at = getattr(
        app.state,
        "started_at",
        time.time(),
    )

    return {
        "status": "ok",
        "uptime": round(time.time() - started_at, 2),
    }


# ============================================================
# API Root
# ============================================================

@app.get("/api")
async def api_root() -> dict[str, Any]:
    """
    API status endpoint.
    """

    return {
        "success": True,
        "message": "API is working",
    }


# ============================================================
# API Status
# ============================================================

@app.get("/api/status")
async def api_status() -> dict[str, Any]:
    """
    Returns detailed API status information.
    """

    return {
        "success": True,
        "server": "online",
        "version": app.version,
    }


# ============================================================
# Hello Endpoint
# ============================================================

@app.get("/api/hello")
async def hello(name: str = "World") -> dict[str, Any]:
    """
    Simple example GET endpoint.

    Example:
        GET /api/hello?name=John
    """

    return {
        "success": True,
        "message": f"Hello, {name}!",
    }


# ============================================================
# Example POST Endpoint
# ============================================================

@app.post("/api/data")
async def receive_data(
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Receives arbitrary JSON data and returns it.

    Example request:

    {
        "username": "john",
        "age": 25
    }
    """

    logger.info("Received data: %s", data)

    return {
        "success": True,
        "data": data,
    }


# ============================================================
# 404 Handler
# ============================================================

@app.exception_handler(404)
async def not_found_handler(
    request: Request,
    exc: Exception,
):
    """
    Handles requests to non-existent endpoints.
    """

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "path": request.url.path,
        },
    )


# ============================================================
# Server Entry Point
# ============================================================

def main() -> None:
    """
    Starts the FastAPI server.
    """

    import uvicorn

    logger.info(
        "Starting server on http://%s:%s",
        HOST,
        PORT,
    )

    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info",
    )


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":
    main()
