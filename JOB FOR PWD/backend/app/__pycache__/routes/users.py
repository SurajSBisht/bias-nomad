"""
User-related API routes.

This module handles all HTTP endpoints related to user management,
including creating new users and retrieving user information.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.db_init import get_db
from app.database.models import User
from app.utils.schemas import UserCreate, UserResponse

# Create router for user endpoints
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[UserResponse]:
    """
    Retrieve a list of all users.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        db: Database session dependency
        
    Returns:
        List of user objects
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    """
    Retrieve a specific user by ID.
    
    Args:
        user_id: Unique identifier of the user
        db: Database session dependency
        
    Returns:
        User object
        
    Raises:
        HTTPException: If user with given ID is not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """
    Create a new user account.
    
    Args:
        user: User data from request body
        db: Database session dependency
        
    Returns:
        Created user object
        
    Raises:
        HTTPException: If user with given email already exists
    """
    # Check if user with email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists"
        )
    
    # Create new user instance
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        has_disability=user.has_disability,
        disability_type=user.disability_type,
        accessibility_needs=user.accessibility_needs
    )
    
    # Add to database and commit
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

