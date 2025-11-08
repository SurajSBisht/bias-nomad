"""
Job-related API routes.

This module handles all HTTP endpoints related to job postings,
including retrieving job listings with optional filtering.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.db_init import get_db
from app.database.models import Job
from app.utils.schemas import JobResponse

# Create router for job endpoints
router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[JobResponse])
def get_jobs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    is_remote: Optional[bool] = Query(None, description="Filter by remote work availability"),
    is_inclusive: Optional[bool] = Query(None, description="Filter by inclusive job flag"),
    location: Optional[str] = Query(None, description="Filter by location (partial match)"),
    db: Session = Depends(get_db)
) -> List[JobResponse]:
    """
    Retrieve a list of job postings with optional filtering.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        is_remote: Optional filter for remote jobs
        is_inclusive: Optional filter for inclusive jobs
        location: Optional location filter (case-insensitive partial match)
        db: Database session dependency
        
    Returns:
        List of job objects matching the criteria
    """
    # Start with base query
    query = db.query(Job)
    
    # Apply filters if provided
    if is_remote is not None:
        query = query.filter(Job.is_remote == is_remote)
    
    if is_inclusive is not None:
        query = query.filter(Job.is_inclusive == is_inclusive)
    
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    
    # Apply pagination and execute query
    jobs = query.offset(skip).limit(limit).all()
    
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)) -> JobResponse:
    """
    Retrieve a specific job by ID.
    
    Args:
        job_id: Unique identifier of the job
        db: Database session dependency
        
    Returns:
        Job object
        
    Raises:
        HTTPException: If job with given ID is not found
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID {job_id} not found"
        )
    return job

