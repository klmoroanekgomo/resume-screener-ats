"""
FastAPI application for Resume Screening System
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List, Optional
import os
import shutil
import time
from datetime import datetime
import sys

# Add parent directory to path
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

# Global variables for models
document_parser = None
text_cleaner = None
skill_extractor = None
matcher = None

# Directories
UPLOAD_DIR = "data/raw/uploaded_resumes"
PROCESSED_DIR = "data/processed/uploaded_resumes"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load models on startup"""
    global document_parser, text_cleaner, skill_extractor, matcher
    
    print("="*70)
    print("STARTING RESUME SCREENING API")
    print("="*70)
    
    # Create directories
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Initialize models
    print("\n📦 Loading models...")
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
    
    # Cleanup (if needed)
    print("\n🔴 Shutting down API...")

# Initialize FastAPI app
app = FastAPI(
    title="Resume Screening System API",
    description="AI-powered Applicant Tracking System for resume screening and candidate matching",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
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

def generate_recommendations(match_result: dict) -> List[str]:
    """Generate recommendations based on match result"""
    recommendations = []
    
    # Skill gap recommendations
    missing_skills = match_result['skill_match']['missing_skills']
    if missing_skills:
        if len(missing_skills) <= 3:
            recommendations.append(f"Consider acquiring: {', '.join(missing_skills[:3])}")
        else:
            recommendations.append(f"Focus on developing {len(missing_skills)} missing skills")
    
    # Experience recommendations
    exp_match = match_result['experience_match']
    if not exp_match['meets_requirement']:
        recommendations.append("Gain more relevant work experience")
    
    # Education recommendations
    edu_match = match_result['education_match']
    if not edu_match['meets_requirement']:
        recommendations.append("Consider pursuing additional education/certifications")
    
    # Overall fit recommendations
    if match_result['overall_score'] >= 80:
        recommendations.append("Excellent fit - Highly recommended for interview")
    elif match_result['overall_score'] >= 60:
        recommendations.append("Good fit - Recommend for initial screening")
    elif match_result['overall_score'] >= 40:
        recommendations.append("Moderate fit - May be suitable for entry-level roles")
    else:
        recommendations.append("Consider other opportunities better aligned with skills")
    
    return recommendations

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Resume Screening System API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "upload_resume": "/resume/upload",
            "extract_profile": "/resume/profile/{filename}",
            "match_single": "/match/single",
            "match_batch": "/match/batch",
            "list_resumes": "/resumes/list"
        },
        "documentation": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        models_loaded=all([document_parser, text_cleaner, skill_extractor, matcher]),
        version="1.0.0"
    )

@app.post("/resume/upload", response_model=ResumeUploadResponse, tags=["Resume"])
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume file (PDF, DOCX, or TXT)
    
    - **file**: Resume file to upload
    """
    
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    save_upload_file(file, file_path)
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Extract text
    try:
        doc_data = document_parser.parse_file(file_path)
        text_length = len(doc_data['text'])
        status = "success"
        message = "Resume uploaded and processed successfully"
    except Exception as e:
        text_length = 0
        status = "error"
        message = f"Error processing file: {str(e)}"
    
    return ResumeUploadResponse(
        filename=file.filename,
        file_size=file_size,
        extracted_text_length=text_length,
        processing_status=status,
        message=message
    )

@app.get("/resume/profile/{filename}", response_model=ProfileResponse, tags=["Resume"])
async def extract_profile(filename: str):
    """
    Extract complete profile from an uploaded resume
    
    - **filename**: Name of the uploaded resume file
    """
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Resume file not found")
    
    try:
        # Parse document
        doc_data = document_parser.parse_file(file_path)
        text = doc_data['text']
        
        # Extract contact info
        contact = text_cleaner.extract_contact_info(text)
        name = text_cleaner.extract_name(text)
        years_exp = text_cleaner.extract_years_of_experience(text)
        sections = text_cleaner.extract_sections(text)
        
        # Extract complete profile
        profile = skill_extractor.extract_complete_profile(text, sections)
        
        return ProfileResponse(
            filename=filename,
            name=name,
            email=contact['email'],
            phone=contact['phone'],
            linkedin=contact['linkedin'],
            github=contact['github'],
            years_experience=years_exp,
            skills=SkillsResponse(**profile['skills']),
            education=EducationResponse(**profile['education']),
            experience_level=profile['experience_level'],
            certifications=profile['certifications']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting profile: {str(e)}")

@app.post("/match/single", response_model=MatchResultResponse, tags=["Matching"])
async def match_single_resume(
    filename: str,
    job_description: JobDescriptionRequest
):
    """
    Match a single resume to a job description
    
    - **filename**: Name of the uploaded resume file
    - **job_description**: Job description details
    """
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Resume file not found")
    
    try:
        # Parse resume
        doc_data = document_parser.parse_file(file_path)
        resume_text = doc_data['text']
        
        # Extract resume profile
        contact = text_cleaner.extract_contact_info(resume_text)
        name = text_cleaner.extract_name(resume_text)
        years_exp = text_cleaner.extract_years_of_experience(resume_text)
        sections = text_cleaner.extract_sections(resume_text)
        
        resume_profile = skill_extractor.extract_complete_profile(resume_text, sections)
        resume_profile['filename'] = filename
        resume_profile['name'] = name
        resume_profile['years_experience'] = years_exp
        resume_profile['raw_text'] = resume_text
        
        # Extract job profile
        job_profile = skill_extractor.extract_complete_profile(
            job_description.description,
            {}
        )
        job_profile['raw_text'] = job_description.description
        
        # Override with specified requirements
        if job_description.required_skills:
            job_profile['skills']['skills'] = job_description.required_skills
        
        # Calculate match
        match_result = matcher.calculate_overall_fit_score(resume_profile, job_profile)
        
        # Generate recommendations
        recommendations = generate_recommendations(match_result)
        
        return MatchResultResponse(
            candidate_name=name,
            filename=filename,
            overall_score=match_result['overall_score'],
            fit_level=match_result['fit_level'],
            skill_match=SkillMatchResponse(**match_result['skill_match']),
            experience_match=match_result['experience_match'],
            education_match=match_result['education_match'],
            text_similarity=match_result['text_similarity'],
            semantic_similarity=match_result['semantic_similarity'],
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching resume: {str(e)}")

@app.post("/match/batch", response_model=BatchMatchResponse, tags=["Matching"])
async def match_batch_resumes(request: BatchMatchRequest):
    """
    Match multiple resumes to a job description
    
    - **job_description**: Job description details
    - **resume_filenames**: List of resume filenames (optional, if not provided, matches all)
    """
    
    start_time = time.time()
    
    # Get list of resumes to process
    if request.resume_filenames:
        resume_files = request.resume_filenames
    else:
        # Get all resumes in upload directory
        resume_files = [f for f in os.listdir(UPLOAD_DIR) 
                       if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
    
    if not resume_files:
        raise HTTPException(status_code=404, detail="No resume files found")
    
    # Extract job profile
    job_profile = skill_extractor.extract_complete_profile(
        request.job_description.description,
        {}
    )
    job_profile['raw_text'] = request.job_description.description
    
    if request.job_description.required_skills:
        job_profile['skills']['skills'] = request.job_description.required_skills
    
    # Match each resume
    matches = []
    
    for filename in resume_files:
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            continue
        
        try:
            # Parse resume
            doc_data = document_parser.parse_file(file_path)
            resume_text = doc_data['text']
            
            # Extract profile
            contact = text_cleaner.extract_contact_info(resume_text)
            name = text_cleaner.extract_name(resume_text)
            years_exp = text_cleaner.extract_years_of_experience(resume_text)
            sections = text_cleaner.extract_sections(resume_text)
            
            resume_profile = skill_extractor.extract_complete_profile(resume_text, sections)
            resume_profile['filename'] = filename
            resume_profile['name'] = name
            resume_profile['years_experience'] = years_exp
            resume_profile['raw_text'] = resume_text
            
            # Calculate match
            match_result = matcher.calculate_overall_fit_score(resume_profile, job_profile)
            
            # Generate recommendations
            recommendations = generate_recommendations(match_result)
            
            matches.append(MatchResultResponse(
                candidate_name=name,
                filename=filename,
                overall_score=match_result['overall_score'],
                fit_level=match_result['fit_level'],
                skill_match=SkillMatchResponse(**match_result['skill_match']),
                experience_match=match_result['experience_match'],
                education_match=match_result['education_match'],
                text_similarity=match_result['text_similarity'],
                semantic_similarity=match_result['semantic_similarity'],
                recommendations=recommendations
            ))
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    # Sort by overall score
    matches.sort(key=lambda x: x.overall_score, reverse=True)
    
    processing_time = time.time() - start_time
    
    return BatchMatchResponse(
        job_title=request.job_description.title,
        total_candidates=len(matches),
        matches=matches,
        processing_time=round(processing_time, 2)
    )

@app.get("/resumes/list", tags=["Resume"])
async def list_resumes():
    """List all uploaded resumes"""
    
    if not os.path.exists(UPLOAD_DIR):
        return {"resumes": [], "total": 0}
    
    resumes = []
    
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if os.path.isfile(file_path):
            file_stats = os.stat(file_path)
            resumes.append({
                "filename": filename,
                "size_bytes": file_stats.st_size,
                "size_kb": round(file_stats.st_size / 1024, 2),
                "uploaded_at": datetime.fromtimestamp(file_stats.st_ctime).isoformat()
            })
    
    return {
        "resumes": resumes,
        "total": len(resumes)
    }

@app.delete("/resume/{filename}", tags=["Resume"])
async def delete_resume(filename: str):
    """Delete an uploaded resume"""
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Resume file not found")
    
    try:
        os.remove(file_path)
        return {"message": f"Resume {filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)