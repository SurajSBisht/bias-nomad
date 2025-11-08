"""
Database models for Bias Nomad.

This module defines SQLAlchemy ORM models for User and Job entities.
These models represent the database schema and provide an object-oriented
interface to interact with the database.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.database.db_init import Base


class User(Base):
    """
    User model representing job seekers on the platform.
    
    Attributes:
        id: Primary key, unique identifier for the user
        email: User's email address (unique)
        full_name: User's full name
        has_disability: Boolean flag indicating if user has a disability
        disability_type: Optional description of disability type
        accessibility_needs: Text field for accessibility requirements
        created_at: Timestamp when user account was created
        updated_at: Timestamp when user account was last updated
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    has_disability = Column(Boolean, default=False, nullable=False)
    disability_type = Column(String(255), nullable=True)
    accessibility_needs = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Job(Base):
    """
    Job model representing job postings on the platform.
    
    Attributes:
        id: Primary key, unique identifier for the job
        title: Job title
        company: Company name
        description: Full job description
        skills: Required skills for the job (optional)
        location: Job location (city, state, country)
        is_remote: Boolean flag indicating if job is remote
        is_inclusive: Boolean flag indicating if job is marked as inclusive
        accessibility_features: Text field describing accessibility features
        salary_min: Minimum salary (optional)
        salary_max: Maximum salary (optional)
        application_url: URL to apply for the job
        created_at: Timestamp when job was posted
        updated_at: Timestamp when job was last updated
    """
    
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    skills = Column(Text, nullable=True)  # Required skills for the job
    location = Column(String(255), nullable=False)
    is_remote = Column(Boolean, default=False, nullable=False)
    is_inclusive = Column(Boolean, default=False, nullable=False)
    accessibility_features = Column(Text, nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    application_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

