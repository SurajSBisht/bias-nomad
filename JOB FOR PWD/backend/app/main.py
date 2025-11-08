"""
Bias Nomad Backend - FastAPI Application Entry Point

This is the main application file that initializes the FastAPI app,
configures middleware, includes routers, and handles startup events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db_init import init_db
from app.routes import users, jobs, ml_routes

# Create FastAPI application instance
app = FastAPI(
    title="Bias Nomad API",
    description="Backend API for Bias Nomad - A platform for finding inclusive and accessible job opportunities",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc",  # ReDoc documentation
)

# Configure CORS (Cross-Origin Resource Sharing)
# In production, replace "*" with specific allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    
    This function runs once when the application starts.
    It initializes the database by creating all tables.
    """
    init_db()
    print("[OK] Database initialized")


@app.get("/", tags=["root"])
def root():
    """
    Root endpoint providing API information.
    
    Returns:
        Dictionary with API name and documentation links
    """
    return {
        "message": "Welcome to Bias Nomad API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint for monitoring and deployment verification.
    
    Returns:
        Dictionary with health status
    """
    return {"status": "healthy", "service": "bias-nomad-backend"}


# Include routers for different API endpoints
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(ml_routes.router)


if __name__ == "__main__":
    import uvicorn
    
    # Run the application using uvicorn
    # This is useful for development; in production, use a proper ASGI server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes (development only)
    )

