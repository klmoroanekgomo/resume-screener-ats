"""
FastAPI application with Database Integration
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from typing import List, Optional
import os
import shutil
import time
from datetime import datetime
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.schemas import (
    ResumeUploadResponse, JobDescriptionRequest, ProfileResponse,
    MatchResultResponse, BatchMatchRequest, BatchMatchResponse,
    HealthResponse, SkillsResponse, EducationResponse, SkillMatchResponse
)
from data_processing.pdf_parser import DocumentParser
from data_processing.text_cleaner import TextCleaner
from models.skill_extractor import SkillExtractor
from models.matcher import ResumeJobMatcher
from database.database import get_db, engine
from database.models import Base, Resume as ResumeModel, JobDescription as JobModel, Match as MatchModel
from database import crud

# Global variables for models
document_parser = None
text_cleaner = None
skill_extractor = None
matcher = None

# Directories
UPLOAD_DIR = "data/raw/uploaded_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load models and initialize database on startup"""
    global document_parser, text_cleaner, skill_extractor, matcher
    
    print("="*70)
    print("STARTING RESUME SCREENING API (WITH DATABASE)")
    print("="*70)
    
    # Create database tables
    print("\n📦 Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("  ✓ Database tables ready")
    
    # Initialize models
    print("\n📦 Loading ML models...")
    try:
        document_parser = DocumentParser()
        print("  ✓ Document parser loaded")
        
        text_cleaner = TextCleaner()
        print("  ✓ Text cleaner loaded")
        
        skill_extractor = SkillExtractor(use_large_model=False)
        print("  ✓ Skill extractor loaded")
        
        matcher = ResumeJobMatcher(use_transformers=True)
        print("  ✓ Resume matcher loaded")
        
        print("\n✓ All models loaded successfully!")
        print("="*70)
    except Exception as e:
        print(f"\n❌ Error loading models: {e}")
        raise
    
    yield
    
    print("\n🔴 Shutting down API...")

# Initialize FastAPI app
app = FastAPI(
    title="Resume Screening System API (Database)",
    description="AI-powered ATS with PostgreSQL database",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions

def save_upload_file(upload_file: UploadFile, destination: str):
    """Save uploaded file to destination"""
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Resume Screening System API with Database",
        "version": "2.0.0",
        "status": "active",
        "database": "PostgreSQL",
        "endpoints": {
            "health": "/health",
            "upload_resume": "/resume/upload",
            "get_resume": "/resume/{resume_id}",
            "list_resumes": "/resumes",
            "create_job": "/job/create",
            "list_jobs": "/jobs",
            "match_single": "/match/{resume_id}/{job_id}",
            "match_batch": "/match/batch/{job_id}"
        },
        "documentation": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    
    # Check database connection
    try:
        resume_count = crud.get_resume_count(db)
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        timestamp=datetime.now().isoformat(),
        models_loaded=all([document_parser, text_cleaner, skill_extractor, matcher]),
        version="2.0.0"
    )

@app.post("/resume/upload", response_model=ResumeUploadResponse, tags=["Resume"])
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process a resume"""
    
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Check if resume already exists
    existing = crud.get_resume_by_filename(db, file.filename)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Resume with filename '{file.filename}' already exists"
        )
    
    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    save_upload_file(file, file_path)
    file_size = os.path.getsize(file_path)
    
    try:
        # Parse document
        doc_data = document_parser.parse_file(file_path)
        text = doc_data['text']
        
        # Extract profile
        contact = text_cleaner.extract_contact_info(text)
        name = text_cleaner.extract_name(text)
        years_exp = text_cleaner.extract_years_of_experience(text)
        sections = text_cleaner.extract_sections(text)
        
        profile = skill_extractor.extract_complete_profile(text, sections)
        
        # Save to database
        resume_data = {
            "filename": file.filename,
            "original_filename": file.filename,
            "file_size": file_size,
            "file_type": file_ext[1:],
            "candidate_name": name,
            "email": contact.get('email'),
            "phone": contact.get('phone'),
            "linkedin": contact.get('linkedin'),
            "github": contact.get('github'),
            "raw_text": text,
            "years_experience": years_exp,
            "experience_level": profile['experience_level'],
            "education_level": profile['education']['highest_level'],
            "skills": profile['skills']['skills'],
            "certifications": profile['certifications']
        }
        
        resume = crud.create_resume(db, resume_data)
        
        return ResumeUploadResponse(
            filename=file.filename,
            file_size=file_size,
            extracted_text_length=len(text),
            processing_status="success",
            message=f"Resume uploaded and saved to database (ID: {resume.id})"
        )
        
    except Exception as e:
        # Clean up file if database save fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@app.get("/resume/{resume_id}", response_model=ProfileResponse, tags=["Resume"])
async def get_resume_profile(resume_id: str, db: Session = Depends(get_db)):
    """Get resume profile from database"""
    
    resume = crud.get_resume(db, resume_id)
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Extract profile from stored data
    profile = skill_extractor.extract_complete_profile(resume.raw_text, {})
    
    return ProfileResponse(
        filename=resume.filename,
        name=resume.candidate_name,
        email=resume.email,
        phone=resume.phone,
        linkedin=resume.linkedin,
        github=resume.github,
        years_experience=resume.years_experience,
        skills=SkillsResponse(**profile['skills']),
        education=EducationResponse(**profile['education']),
        experience_level=resume.experience_level,
        certifications=resume.certifications or []
    )

@app.get("/resumes", tags=["Resume"])
async def list_all_resumes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all resumes from database"""
    
    resumes = crud.get_all_resumes(db, skip=skip, limit=limit)
    total = crud.get_resume_count(db)
    
    return {
        "resumes": [
            {
                "id": r.id,
                "filename": r.filename,
                "candidate_name": r.candidate_name,
                "email": r.email,
                "years_experience": r.years_experience,
                "experience_level": r.experience_level,
                "total_skills": len(r.skills) if r.skills else 0,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in resumes
        ],
        "total": total,
        "skip": skip,
        "limit": limit
    }

@app.post("/job/create", tags=["Job"])
async def create_job_description(
    job: JobDescriptionRequest,
    db: Session = Depends(get_db)
):
    """Create a new job description"""
    
    # Extract skills from job description
    profile = skill_extractor.extract_complete_profile(job.description, {})
    
    job_data = {
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "required_skills": job.required_skills,
        "required_education": job.required_education,
        "required_years": job.required_years,
        "extracted_skills": profile['skills']['skills']
    }
    
    job_record = crud.create_job(db, job_data)
    
    return {
        "id": job_record.id,
        "title": job_record.title,
        "company": job_record.company,
        "message": "Job description created successfully"
    }

@app.get("/jobs", tags=["Job"])
async def list_all_jobs(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List all job descriptions"""
    
    jobs = crud.get_all_jobs(db, skip=skip, limit=limit, active_only=active_only)
    total = crud.get_job_count(db)
    
    return {
        "jobs": [
            {
                "id": j.id,
                "title": j.title,
                "company": j.company,
                "required_years": j.required_years,
                "required_education": j.required_education,
                "total_skills": len(j.required_skills) if j.required_skills else 0,
                "created_at": j.created_at.isoformat() if j.created_at else None
            }
            for j in jobs
        ],
        "total": total
    }

@app.post("/match/{resume_id}/{job_id}", response_model=MatchResultResponse, tags=["Matching"])
async def match_resume_to_job(
    resume_id: str,
    job_id: str,
    db: Session = Depends(get_db)
):
    """Match a resume to a job and save result"""
    
    # Get resume and job from database
    resume = crud.get_resume(db, resume_id)
    job = crud.get_job(db, job_id)
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Prepare profiles
    resume_profile = skill_extractor.extract_complete_profile(resume.raw_text, {})
    resume_profile['filename'] = resume.filename
    resume_profile['name'] = resume.candidate_name
    resume_profile['years_experience'] = resume.years_experience
    resume_profile['raw_text'] = resume.raw_text
    
    job_profile = skill_extractor.extract_complete_profile(job.description, {})
    job_profile['raw_text'] = job.description
    if job.required_skills:
        job_profile['skills']['skills'] = job.required_skills
    
    # Calculate match
    match_result = matcher.calculate_overall_fit_score(resume_profile, job_profile)
    
    # Generate recommendations
    recommendations = []
    if match_result['overall_score'] >= 80:
        recommendations.append("Excellent fit - Highly recommended for interview")
    elif match_result['overall_score'] >= 60:
        recommendations.append("Good fit - Recommend for initial screening")
    
    missing_skills = match_result['skill_match']['missing_skills']
    if missing_skills and len(missing_skills) <= 3:
        recommendations.append(f"Consider acquiring: {', '.join(missing_skills[:3])}")
    
    # Helper function to convert numpy types to Python types
    def convert_to_python_type(obj):
        """Convert numpy types to Python native types"""
        import numpy as np
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_to_python_type(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_python_type(item) for item in obj]
        else:
            return obj
    
    # Save match to database - convert numpy types
    match_data = {
        "resume_id": resume_id,
        "job_id": job_id,
        "overall_score": float(match_result['overall_score']),
        "skill_match_percentage": float(match_result['skill_match']['match_percentage']),
        "text_similarity": float(match_result['text_similarity']),
        "semantic_similarity": float(match_result['semantic_similarity']),
        "fit_level": match_result['fit_level'],
        "skill_match_details": convert_to_python_type(match_result['skill_match']),
        "experience_match": convert_to_python_type(match_result['experience_match']),
        "education_match": convert_to_python_type(match_result['education_match']),
        "recommendations": recommendations
    }
    
    try:
        match_record = crud.create_match(db, match_data)
        print(f"✓ Match saved to database: {match_record.id}")
    except Exception as e:
        print(f"⚠ Warning: Could not save match to database: {e}")
        import traceback
        traceback.print_exc()
        # Continue anyway - return the match result even if saving fails
    
    return MatchResultResponse(
        candidate_name=resume.candidate_name,
        filename=resume.filename,
        overall_score=match_result['overall_score'],
        fit_level=match_result['fit_level'],
        skill_match=SkillMatchResponse(**match_result['skill_match']),
        experience_match=match_result['experience_match'],
        education_match=match_result['education_match'],
        text_similarity=match_result['text_similarity'],
        semantic_similarity=match_result['semantic_similarity'],
        recommendations=recommendations
    )
    
    match_record = crud.create_match(db, match_data)
    
    return MatchResultResponse(
        candidate_name=resume.candidate_name,
        filename=resume.filename,
        overall_score=match_result['overall_score'],
        fit_level=match_result['fit_level'],
        skill_match=SkillMatchResponse(**match_result['skill_match']),
        experience_match=match_result['experience_match'],
        education_match=match_result['education_match'],
        text_similarity=match_result['text_similarity'],
        semantic_similarity=match_result['semantic_similarity'],
        recommendations=recommendations
    )

@app.get("/stats", tags=["Statistics"])
async def get_statistics(db: Session = Depends(get_db)):
    """Get system statistics"""
    
    return {
        "total_resumes": crud.get_resume_count(db),
        "total_jobs": crud.get_job_count(db),
        "total_matches": crud.get_match_count(db),
        "average_match_score": crud.get_average_match_score(db)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)