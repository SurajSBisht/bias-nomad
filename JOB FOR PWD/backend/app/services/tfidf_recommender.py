"""
TF-IDF-based job recommendation service.

This module implements a TF-IDF (Term Frequency-Inverse Document Frequency)
based recommendation system for matching users with job postings.
The system combines job text fields (title, skills, description) and
user profile information to compute similarity scores using cosine similarity.
"""

from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from app.database.models import User, Job


def combine_job_text(job: Job) -> str:
    """
    Combine job text fields into a single string for TF-IDF processing.
    
    Combines title, skills, and description fields into a single text document.
    Handles None values gracefully by replacing them with empty strings.
    
    Args:
        job: Job database model instance
        
    Returns:
        Combined text string for the job
    """
    # Combine title, skills, and description
    title = job.title or ""
    skills = job.skills or ""
    description = job.description or ""
    
    # Combine all text fields with spaces
    combined_text = f"{title} {skills} {description}".strip()
    
    return combined_text


def combine_user_profile_text(user: User) -> str:
    """
    Combine user profile text fields into a single string for TF-IDF processing.
    
    Combines user's full name, disability type, and accessibility needs
    into a single text document to represent their profile and preferences.
    
    Args:
        user: User database model instance
        
    Returns:
        Combined text string representing the user profile
    """
    # Combine user profile fields
    full_name = user.full_name or ""
    disability_type = user.disability_type or ""
    accessibility_needs = user.accessibility_needs or ""
    
    # Combine all text fields with spaces
    combined_text = f"{full_name} {disability_type} {accessibility_needs}".strip()
    
    return combined_text


def compute_tfidf_recommendations(
    user: User,
    jobs: List[Job],
    limit: int = 10
) -> List[Tuple[Job, float]]:
    """
    Compute TF-IDF-based job recommendations for a user.
    
    This function:
    1. Combines text fields from user profile and all jobs
    2. Computes TF-IDF vectors for user profile and job descriptions
    3. Calculates cosine similarity between user and each job
    4. Returns top matching jobs sorted by similarity score
    
    Args:
        user: User database model instance
        jobs: List of Job database model instances
        limit: Maximum number of recommendations to return
        
    Returns:
        List of tuples containing (Job, similarity_score) sorted by score (descending)
        
    Raises:
        ValueError: If jobs list is empty
    """
    # Handle empty jobs list gracefully
    if not jobs:
        return []
    
    # Combine user profile text
    user_text = combine_user_profile_text(user)
    
    # Combine job texts
    job_texts = [combine_job_text(job) for job in jobs]
    
    # Create TF-IDF vectorizer
    # max_features limits vocabulary size for efficiency
    # ngram_range=(1, 2) considers both single words and bigrams
    # min_df=1 means include terms that appear in at least 1 document
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=1,
        stop_words='english',  # Remove common English stop words
        lowercase=True,
        strip_accents='unicode'
    )
    
    # Fit and transform all documents (user + jobs)
    # Include user text first, then all job texts
    all_texts = [user_text] + job_texts
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Extract user vector (first row) and job vectors (remaining rows)
    user_vector = tfidf_matrix[0:1]  # Keep as 2D array for cosine_similarity
    job_vectors = tfidf_matrix[1:]
    
    # Compute cosine similarity between user and all jobs
    # Returns a 2D array where [0][i] is similarity between user and job i
    similarity_scores = cosine_similarity(user_vector, job_vectors)[0]
    
    # Create list of (job, score) tuples
    job_scores = list(zip(jobs, similarity_scores))
    
    # Sort by similarity score (descending) and return top 'limit' results
    job_scores.sort(key=lambda x: x[1], reverse=True)
    
    return job_scores[:limit]


# TODO: ML Model Training Placeholder
# In the future, this module will be extended to:
# 1. Load pre-trained TF-IDF vectorizers from saved_models/
# 2. Use more sophisticated models (e.g., BERT embeddings, neural networks)
# 3. Incorporate user interaction history (clicks, applications, favorites)
# 4. Add collaborative filtering components
# 5. Implement model retraining pipeline in ml/train_recommender.py
# 6. Cache TF-IDF vectors for better performance
# 7. Add feature engineering for accessibility-specific matching

