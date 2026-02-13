"""
Pydantic schemas for API request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any  # Added Any here
from datetime import datetime

# Request Schemas

class ResumeUploadResponse(BaseModel):
    """Response after uploading a resume"""
    filename: str
    file_size: int
    extracted_text_length: int
    processing_status: str
    message: str

class JobDescriptionRequest(BaseModel):
    """Request schema for job description"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "Senior Python Developer",
            "company": "TechCorp",
            "description": "We are seeking a Senior Python Developer with 5+ years of experience...",
            "required_skills": ["Python", "Django", "AWS", "Docker"],
            "required_education": "bachelors",
            "required_years": 5
        }
    })
    
    title: str
    company: str
    description: str
    required_skills: Optional[List[str]] = []
    required_education: Optional[str] = None
    required_years: Optional[int] = 0

# Response Schemas

class SkillsResponse(BaseModel):
    """Response schema for extracted skills"""
    skills: List[str]
    total_skills: int
    categories: Dict[str, List[str]]
    skill_count: Dict[str, int]

class EducationResponse(BaseModel):
    """Response schema for education information"""
    highest_level: Optional[str]
    has_degree: bool
    found_degrees: List[Dict[str, str]]

class ProfileResponse(BaseModel):
    """Response schema for complete profile"""
    filename: str
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    years_experience: int
    skills: SkillsResponse
    education: EducationResponse
    experience_level: str
    certifications: List[str]

class SkillMatchResponse(BaseModel):
    """Response schema for skill matching"""
    match_percentage: float
    matched_skills: List[str]
    missing_skills: List[str]
    extra_skills: List[str]
    total_required: int
    total_matched: int

class MatchResultResponse(BaseModel):
    """Response schema for resume-job match result"""
    candidate_name: Optional[str]
    filename: str
    overall_score: float
    fit_level: str
    skill_match: SkillMatchResponse
    experience_match: Dict[str, Any]  # Changed from Dict[str, any] to Dict[str, Any]
    education_match: Dict[str, Any]   # Changed from Dict[str, any] to Dict[str, Any]
    text_similarity: float
    semantic_similarity: float
    recommendations: List[str]

class BatchMatchRequest(BaseModel):
    """Request schema for batch matching"""
    job_description: JobDescriptionRequest
    resume_filenames: Optional[List[str]] = None  # If None, match all resumes

class BatchMatchResponse(BaseModel):
    """Response schema for batch matching"""
    job_title: str
    total_candidates: int
    matches: List[MatchResultResponse]
    processing_time: float

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    models_loaded: bool
    version: str

class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: str
    timestamp: str