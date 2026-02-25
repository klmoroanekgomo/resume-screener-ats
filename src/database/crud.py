"""
CRUD operations for database
"""

from sqlalchemy import func
from sqlalchemy.orm import Session
from src.database.models import Resume, JobDescription, Match, User
from typing import List, Optional
import json

# Resume CRUD

def create_resume(db: Session, resume_data: dict) -> Resume:
    """Create a new resume record"""
    resume = Resume(**resume_data)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume

def get_resume(db: Session, resume_id: str) -> Optional[Resume]:
    """Get resume by ID"""
    return db.query(Resume).filter(Resume.id == resume_id).first()

def get_resume_by_filename(db: Session, filename: str) -> Optional[Resume]:
    """Get resume by filename"""
    return db.query(Resume).filter(Resume.filename == filename).first()

def get_all_resumes(db: Session, skip: int = 0, limit: int = 100) -> List[Resume]:
    """Get all resumes with pagination"""
    return db.query(Resume).offset(skip).limit(limit).all()

def update_resume(db: Session, resume_id: str, resume_data: dict) -> Optional[Resume]:
    """Update resume"""
    resume = get_resume(db, resume_id)
    if resume:
        for key, value in resume_data.items():
            setattr(resume, key, value)
        db.commit()
        db.refresh(resume)
    return resume

def delete_resume(db: Session, resume_id: str) -> bool:
    """Delete resume"""
    resume = get_resume(db, resume_id)
    if resume:
        db.delete(resume)
        db.commit()
        return True
    return False

def search_resumes(db: Session, query: str) -> List[Resume]:
    """Search resumes by name, email, or skills"""
    return db.query(Resume).filter(
        (Resume.candidate_name.ilike(f"%{query}%")) |
        (Resume.email.ilike(f"%{query}%"))
    ).all()

# Job Description CRUD

def create_job(db: Session, job_data: dict) -> JobDescription:
    """Create a new job description"""
    job = JobDescription(**job_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_job(db: Session, job_id: str) -> Optional[JobDescription]:
    """Get job by ID"""
    return db.query(JobDescription).filter(JobDescription.id == job_id).first()

def get_all_jobs(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[JobDescription]:
    """Get all job descriptions"""
    query = db.query(JobDescription)
    if active_only:
        query = query.filter(JobDescription.is_active == True)
    return query.offset(skip).limit(limit).all()

def update_job(db: Session, job_id: str, job_data: dict) -> Optional[JobDescription]:
    """Update job description"""
    job = get_job(db, job_id)
    if job:
        for key, value in job_data.items():
            setattr(job, key, value)
        db.commit()
        db.refresh(job)
    return job

def delete_job(db: Session, job_id: str) -> bool:
    """Delete job description"""
    job = get_job(db, job_id)
    if job:
        db.delete(job)
        db.commit()
        return True
    return False

# Match CRUD

def create_match(db: Session, match_data: dict) -> Match:
    """Create a new match record"""
    match = Match(**match_data)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

def get_match(db: Session, match_id: str) -> Optional[Match]:
    """Get match by ID"""
    return db.query(Match).filter(Match.id == match_id).first()

def get_matches_by_resume(db: Session, resume_id: str) -> List[Match]:
    """Get all matches for a resume"""
    return db.query(Match).filter(Match.resume_id == resume_id).all()

def get_matches_by_job(db: Session, job_id: str) -> List[Match]:
    """Get all matches for a job"""
    return db.query(Match).filter(Match.job_id == job_id).order_by(Match.overall_score.desc()).all()

def get_top_matches(db: Session, job_id: str, limit: int = 10) -> List[Match]:
    """Get top N matches for a job"""
    return db.query(Match).filter(Match.job_id == job_id).order_by(Match.overall_score.desc()).limit(limit).all()

def delete_match(db: Session, match_id: str) -> bool:
    """Delete match"""
    match = get_match(db, match_id)
    if match:
        db.delete(match)
        db.commit()
        return True
    return False

# Statistics

def get_resume_count(db: Session) -> int:
    """Get total number of resumes"""
    return db.query(Resume).count()

def get_job_count(db: Session) -> int:
    """Get total number of jobs"""
    return db.query(JobDescription).filter(JobDescription.is_active == True).count()

def get_match_count(db: Session) -> int:
    """Get total number of matches"""
    return db.query(Match).count()

def get_average_match_score(db: Session) -> float:
    """Get average match score across all matches"""
    result = db.query(func.avg(Match.overall_score)).scalar()
    return float(result) if result else 0.0