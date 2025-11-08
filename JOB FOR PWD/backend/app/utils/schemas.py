"""
Pydantic schemas for request/response validation.

This module defines Pydantic models for API request and response validation.
These schemas ensure type safety and automatic validation of incoming/outgoing data.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ==================== User Schemas ====================

class UserBase(BaseModel):
    """Base schema for User with common fields."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    has_disability: bool = False
    disability_type: Optional[str] = Field(None, max_length=255)
    accessibility_needs: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass


class UserResponse(UserBase):
    """Schema for user response with additional metadata."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


# ==================== Job Schemas ====================

class JobBase(BaseModel):
    """Base schema for Job with common fields."""
    title: str = Field(..., min_length=1, max_length=255)
    company: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    skills: Optional[str] = Field(None, description="Required skills for the job")
    location: str = Field(..., min_length=1, max_length=255)
    is_remote: bool = False
    is_inclusive: bool = False
    accessibility_features: Optional[str] = None
    salary_min: Optional[float] = Field(None, ge=0)
    salary_max: Optional[float] = Field(None, ge=0)
    application_url: Optional[str] = Field(None, max_length=500)


class JobCreate(JobBase):
    """Schema for creating a new job posting."""
    pass


class JobResponse(JobBase):
    """Schema for job response with additional metadata."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


# ==================== ML Recommendation Schemas ====================

class RecommendationRequest(BaseModel):
    """Schema for ML recommendation request."""
    user_id: int = Field(..., gt=0, description="ID of the user requesting recommendations")
    limit: int = Field(10, ge=1, le=50, description="Maximum number of recommendations to return")


class JobRecommendation(BaseModel):
    """Schema for a single job recommendation with score."""
    job: JobResponse
    match_score: float = Field(..., ge=0.0, le=1.0, description="ML-generated match score (0-1)")


class RecommendationResponse(BaseModel):
    """Schema for ML recommendation response."""
    user_id: int
    recommendations: list[JobRecommendation]
    total_found: int

