"""
SQLAlchemy models for database tables - Simplified version
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import uuid
import os
import sys

# Get the database Base from a fresh declarative_base
Base = declarative_base()

def generate_uuid():
    """Generate UUID for primary keys"""
    return str(uuid.uuid4())

class Resume(Base):
    """Resume table"""
    __tablename__ = "resumes"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    filename = Column(String, unique=True, nullable=False, index=True)
    original_filename = Column(String, nullable=False)
    file_size = Column(Integer)
    file_type = Column(String)
    
    # Candidate information
    candidate_name = Column(String)
    email = Column(String, index=True)
    phone = Column(String)
    linkedin = Column(String)
    github = Column(String)
    
    # Extracted data
    raw_text = Column(Text)
    years_experience = Column(Integer)
    experience_level = Column(String)
    education_level = Column(String)
    
    # Skills (stored as JSON)
    skills = Column(JSON)
    certifications = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class JobDescription(Base):
    """Job description table"""
    __tablename__ = "job_descriptions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # Requirements
    required_skills = Column(JSON)
    required_education = Column(String)
    required_years = Column(Integer)
    
    # Extracted data
    extracted_skills = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class Match(Base):
    """Resume-Job match results table"""
    __tablename__ = "matches"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    resume_id = Column(String, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(String, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Match scores
    overall_score = Column(Float, nullable=False)
    skill_match_percentage = Column(Float)
    text_similarity = Column(Float)
    semantic_similarity = Column(Float)
    fit_level = Column(String)
    
    # Detailed results (stored as JSON)
    skill_match_details = Column(JSON)
    experience_match = Column(JSON)
    education_match = Column(JSON)
    recommendations = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    """User table (optional - for multi-user support)"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    
    # Role-based access
    role = Column(String, default="recruiter")
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))