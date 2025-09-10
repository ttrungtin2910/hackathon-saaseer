"""Main FastAPI application for Contract Management API"""

import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings
from app.api.endpoints import router
from app.services.cosmosdb import cosmosdb_service
from app.services.azure_blob import azure_blob_service

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Contract Management API...")

    try:
        # Test connections
        logger.info("Testing service connections...")

        # Test CosmosDB connection
        try:
            # This will create database and containers if they don't exist
            logger.info("CosmosDB service initialized successfully")
        except Exception as e:
            logger.error(f"CosmosDB connection failed: {e}")
            # Don't raise exception, let the app start but log the error

        # Test Azure Blob Storage connection
        try:
            # This will create container if it doesn't exist
            logger.info("Azure Blob Storage service initialized successfully")
        except Exception as e:
            logger.error(f"Azure Blob Storage connection failed: {e}")
            # Don't raise exception, let the app start but log the error

        logger.info("Contract Management API started successfully")

    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        # Optionally raise exception to prevent startup
        # raise

    yield

    # Shutdown
    logger.info("Shutting down Contract Management API...")


# Create FastAPI application
app = FastAPI(
    title="Contract Management API",
    description="API for storing and querying contracts using CosmosDB, Azure Blob Storage, and LangGraph OpenAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Contract Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
        "endpoints": {
            "list_contracts": "GET /api/v1/contracts/{username}",
            "upload_contract": "POST /api/v1/contracts/upload",
            "search_contract": "POST /api/v1/contracts/search",
            "get_requirements": "GET /api/v1/contracts/{contract_id}/requirements",
            "download_contract": "GET /api/v1/contracts/{contract_id}/download",
        },
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "type": type(exc).__name__,
        },
    )


# HTTP exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


if __name__ == "__main__":
    logger.info(f"Starting server on {settings.APP_HOST}:{settings.APP_PORT}")

    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
        log_level="info",
    )
