"""Run script for local development"""
import uvicorn
from app.database import engine, Base
from app.models import User, EntrepreneurProfile, Requirement, Scheme, SavedScheme

def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    # Initialize database
    init_db()

    # Run the application
    print("\nStarting ArthSetu API server...")
    print("API will be available at: http://localhost:8000")
    print("API Documentation at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
