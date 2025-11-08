"""
Machine Learning recommendation API routes.

This module handles ML-powered job recommendation endpoints.
Implements TF-IDF-based recommendation system for matching users with jobs.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db_init import get_db
from app.database.models import User, Job
from app.services.tfidf_recommender import compute_tfidf_recommendations
from app.utils.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    JobRecommendation,
    JobResponse
)

# Create router for ML endpoints
router = APIRouter(
    prefix="/ml",
    tags=["machine-learning"],
    responses={404: {"description": "Not found"}},
)


@router.post("/recommend", response_model=RecommendationResponse)
def recommend_jobs(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
) -> RecommendationResponse:
    """
    Generate job recommendations for a user using TF-IDF-based ML algorithms.
    
    This endpoint:
    1. Retrieves the user by user_id from the database
    2. Gets all job records from the database
    3. Combines job text fields (title, skills, description)
    4. Computes TF-IDF vectors for user profile and job descriptions
    5. Uses cosine similarity to find top-matching jobs
    6. Returns top limit job recommendations with similarity scores
    
    Args:
        request: Recommendation request containing user_id and limit
        db: Database session dependency
        
    Returns:
        RecommendationResponse with ranked job recommendations (job id, title, similarity score)
        
    Raises:
        HTTPException: 
            - 404 if user with given ID is not found
            - 200 with empty list if no jobs are available (handled gracefully)
    """
    # Retrieve the user by user_id
    user = db.query(User).filter(User.id == request.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get all job records from the database
    all_jobs = db.query(Job).all()
    
    # Handle empty job tables gracefully
    if not all_jobs:
        return RecommendationResponse(
            user_id=request.user_id,
            recommendations=[],
            total_found=0
        )
    
    # Compute TF-IDF-based recommendations
    # This combines job text fields, computes TF-IDF vectors, and uses cosine similarity
    job_scores = compute_tfidf_recommendations(
        user=user,
        jobs=all_jobs,
        limit=request.limit
    )
    
    # Convert to response format
    recommendations = [
        JobRecommendation(
            job=JobResponse.model_validate(job),
            match_score=float(score)  # Ensure score is a Python float (not numpy float)
        )
        for job, score in job_scores
    ]
    
    return RecommendationResponse(
        user_id=request.user_id,
        recommendations=recommendations,
        total_found=len(recommendations)
    )

