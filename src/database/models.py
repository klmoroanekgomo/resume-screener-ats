"""
SQLAlchemy models for database tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.database import Base
import uuid

def generate_uuid():
    """Generate UUID for primary keys"""
    return str(uuid.uuid4())

class Resume(Base):
    """Resume table"""
    __tablename__ = "resumes"
    __table_args__ = {'extend_existing': True}
    
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
    
    # Relationships - using string references
    matches = relationship("Match", back_populates="resume", cascade="all, delete-orphan", foreign_keys="[Match.resume_id]")

class JobDescription(Base):
    """Job description table"""
    __tablename__ = "job_descriptions"
    __table_args__ = {'extend_existing': True}
    
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
    
    # Relationships - using string references
    matches = relationship("Match", back_populates="job", cascade="all, delete-orphan", foreign_keys="[Match.job_id]")

class Match(Base):
    """Resume-Job match results table"""
    __tablename__ = "matches"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(String, ForeignKey("job_descriptions.id"), nullable=False)
    
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
    
    # Relationships - using string references
    resume = relationship("Resume", back_populates="matches", foreign_keys=[resume_id])
    job = relationship("JobDescription", back_populates="matches", foreign_keys=[job_id])

class User(Base):
    """User table (optional - for multi-user support)"""
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    
    # Role-based access
    role = Column(String, default="recruiter")  # recruiter, admin, viewer
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))