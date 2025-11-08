"""
Database initialization and session management.

This module handles SQLite database connection, session creation,
and database lifecycle management using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

# SQLite database URL
# Using a relative path that will create the database file in the backend directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./bias_nomad.db"

# Create SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed for SQLite to work with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for SQL query logging during development
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency function to get database session.
    
    Yields a database session and ensures it's closed after use.
    This is used as a FastAPI dependency for route handlers.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database by creating all tables.
    
    This function should be called once at application startup
    to ensure all database tables are created.
    """
    # Import models here to ensure they're registered with Base
    from app.database import models
    
    # Create all tables defined in models
    Base.metadata.create_all(bind=engine)

