from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.routes import router as contracts_router
from app.database import cosmos_db
from config.settings import get_settings

# Get application settings
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Disable verbose Azure logging
azure_logger = logging.getLogger('azure.core.pipeline.policies.http_logging_policy')
azure_logger.setLevel(logging.WARNING)

azure_cosmos_logger = logging.getLogger('azure.cosmos')
azure_cosmos_logger.setLevel(logging.WARNING)

# Keep uvicorn access logs to see API requests
uvicorn_access_logger = logging.getLogger('uvicorn.access')
uvicorn_access_logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager - handles startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting SaaSeer Contract Management API...")
    
    # Initialize database and container if they don't exist
    try:
        await cosmos_db.create_database_and_container_if_not_exists()
        logger.info("✅ Database and container initialization completed")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {str(e)}")
        # Don't fail startup, but log the error
    
    yield
    
    # Shutdown
    logger.info("⏹️ Shutting down SaaSeer Contract Management API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="""
    A FastAPI backend for managing contract information with Azure Cosmos DB storage.
    
    ## Features
    
    * **Create contracts** - Store new contract information
    * **Retrieve contracts** - Get contract details by ID
    * **Update contracts** - Modify existing contract information
    * **Delete contracts** - Remove contracts from the database
    * **List contracts** - Get all contracts for a specific user
    
    ## Usage
    
    All contract operations use the user email as a partition key for efficient querying in Cosmos DB.
    """,
    version=settings.app_version,
    terms_of_service="https://www.fpt.com/terms",
    contact={
        "name": "FPT Software",
        "url": "https://www.fpt.com",
        "email": "contact@fpt.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Include routers
app.include_router(contracts_router)


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint providing API information
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    General health check endpoint
    """
    try:
        # You could add more health checks here (database connectivity, etc.)
        return {
            "status": "healthy",
            "message": "API is running successfully",
            "version": settings.app_version
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions
    """
    logger.error(f"Global exception handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred",
            "detail": str(exc) if settings.debug else "Internal server error"
        }
    )


if __name__ == "__main__":
    # For development only
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
