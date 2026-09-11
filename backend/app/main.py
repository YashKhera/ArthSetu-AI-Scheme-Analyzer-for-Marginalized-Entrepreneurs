"""FastAPI main application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, profile, schemes, recommendations, saved, oauth
from app.api import recommendations_v2

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Government Scheme Analyzer API for ArthSetu - SIH 2026",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://localhost:5173",  # vite dev server (if frontend team uses it)
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(oauth.router, prefix="/api", tags=["Google OAuth"])
app.include_router(profile.router, prefix="/api", tags=["Profile"])
app.include_router(schemes.router, prefix="/api", tags=["Schemes"])
app.include_router(recommendations.router, prefix="/api", tags=["Recommendations"])
app.include_router(saved.router, prefix="/api", tags=["Saved Schemes"])
app.include_router(recommendations_v2.router, prefix="/api/v2", tags=["Recommendations V2"])


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": settings.VERSION,
        "service": settings.APP_NAME,
    }


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ArthSetu API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'SQLite'}")
    print("API Documentation: http://localhost:8000/docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print(f"Shutting down {settings.APP_NAME}")