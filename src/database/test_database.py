"""
Test database operations
"""

from src.database.database import SessionLocal
from src.database import crud
from src.database.models import Resume, JobDescription, Match

def test_database():
    """Test all database operations"""
    
    print("="*70)
    print("TESTING DATABASE OPERATIONS")
    print("="*70)
    
    db = SessionLocal()
    
    try:
        # Test 1: Create Resume
        print("\n1. Creating test resume...")
        resume_data = {
            "filename": "test_resume.pdf",
            "original_filename": "John_Doe_Resume.pdf",
            "file_size": 2048,
            "file_type": "pdf",
            "candidate_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+27 123 456 789",
            "raw_text": "Test resume text...",
            "years_experience": 5,
            "experience_level": "senior",
            "education_level": "bachelors",
            "skills": ["Python", "Django", "AWS"],
            "certifications": ["AWS Certified"]
        }
        
        resume = crud.create_resume(db, resume_data)
        print(f"✓ Resume created: {resume.id}")
        
        # Test 2: Get Resume
        print("\n2. Retrieving resume...")
        retrieved = crud.get_resume(db, resume.id)
        print(f"✓ Resume retrieved: {retrieved.candidate_name}")
        
        # Test 3: Create Job
        print("\n3. Creating test job...")
        job_data = {
            "title": "Senior Python Developer",
            "company": "TechCorp",
            "description": "We are seeking...",
            "required_skills": ["Python", "Django"],
            "required_education": "bachelors",
            "required_years": 5,
            "extracted_skills": ["Python", "Django", "AWS"]
        }
        
        job = crud.create_job(db, job_data)
        print(f"✓ Job created: {job.id}")
        
        # Test 4: Create Match
        print("\n4. Creating match...")
        match_data = {
            "resume_id": resume.id,
            "job_id": job.id,
            "overall_score": 85.5,
            "skill_match_percentage": 80.0,
            "text_similarity": 75.0,
            "semantic_similarity": 82.0,
            "fit_level": "Excellent",
            "skill_match_details": {
                "matched": ["Python", "Django"],
                "missing": ["Kubernetes"]
            },
            "recommendations": ["Excellent fit"]
        }
        
        match = crud.create_match(db, match_data)
        print(f"✓ Match created: {match.id}")
        
        # Test 5: Get Statistics
        print("\n5. Getting statistics...")
        resume_count = crud.get_resume_count(db)
        job_count = crud.get_job_count(db)
        match_count = crud.get_match_count(db)
        
        print(f"✓ Total resumes: {resume_count}")
        print(f"✓ Total jobs: {job_count}")
        print(f"✓ Total matches: {match_count}")
        
        # Test 6: Get matches for job
        print("\n6. Getting matches for job...")
        matches = crud.get_matches_by_job(db, job.id)
        print(f"✓ Found {len(matches)} match(es)")
        
        for m in matches:
            print(f"   • Resume: {m.resume.candidate_name} - Score: {m.overall_score}%")
        
        print("\n" + "="*70)
        print("✓ ALL DATABASE TESTS PASSED!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_database()