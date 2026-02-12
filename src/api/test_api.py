"""
Test script for the Resume Screening API
"""

import requests
import json
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*70)
    print("1️⃣  TESTING HEALTH CHECK")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    
    assert response.status_code == 200
    print("✓ Health check passed")

def test_upload_resume():
    """Test uploading a resume"""
    print("\n" + "="*70)
    print("2️⃣  TESTING RESUME UPLOAD")
    print("="*70)
    
    # Use sample resume
    resume_path = "data/sample/resumes/John_Doe_Resume.txt"
    
    if not os.path.exists(resume_path):
        print(f"❌ Resume file not found: {resume_path}")
        return None
    
    with open(resume_path, 'rb') as f:
        files = {'file': ('John_Doe_Resume.txt', f, 'text/plain')}
        response = requests.post(f"{BASE_URL}/resume/upload", files=files)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    
    assert response.status_code == 200
    print("✓ Resume upload successful")
    
    return response.json()['filename']

def test_extract_profile(filename):
    """Test extracting profile from uploaded resume"""
    print("\n" + "="*70)
    print("3️⃣  TESTING PROFILE EXTRACTION")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/resume/profile/{filename}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nCandidate: {data['name']}")
        print(f"Email: {data['email']}")
        print(f"Years Experience: {data['years_experience']}")
        print(f"Total Skills: {data['skills']['total_skills']}")
        print(f"Education Level: {data['education']['highest_level']}")
        print(f"Experience Level: {data['experience_level']}")
        
        print(f"\nTop 10 Skills:")
        for skill in data['skills']['skills'][:10]:
            print(f"  • {skill}")
        
        print("✓ Profile extraction successful")
    else:
        print(f"❌ Error: {response.json()}")

def test_single_match(filename):
    """Test matching a single resume to a job"""
    print("\n" + "="*70)
    print("4️⃣  TESTING SINGLE RESUME MATCHING")
    print("="*70)
    
    job_data = {
        "title": "Senior Python Developer",
        "company": "TechCorp",
        "description": """
        We are seeking a Senior Python Developer with 5+ years of experience.
        
        Required Skills:
        - Python, Django, FastAPI
        - PostgreSQL, MongoDB
        - AWS, Docker, Kubernetes
        - RESTful APIs, Microservices
        - Git, CI/CD
        
        Education: Bachelor's degree in Computer Science
        Experience: 5+ years
        """,
        "required_skills": ["Python", "Django", "FastAPI", "AWS", "Docker", "PostgreSQL"],
        "required_education": "bachelors",
        "required_years": 5
    }
    
    params = {"filename": filename}
    response = requests.post(
        f"{BASE_URL}/match/single",
        params=params,
        json=job_data
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n🎯 MATCH RESULTS")
        print(f"Candidate: {data['candidate_name']}")
        print(f"Overall Score: {data['overall_score']:.1f}% - {data['fit_level']}")
        print(f"\nSkill Match: {data['skill_match']['match_percentage']:.1f}%")
        print(f"  Matched: {data['skill_match']['total_matched']}/{data['skill_match']['total_required']}")
        print(f"  Matched Skills: {', '.join(data['skill_match']['matched_skills'][:5])}")
        
        if data['skill_match']['missing_skills']:
            print(f"\n  Missing Skills:")
            for skill in data['skill_match']['missing_skills'][:5]:
                print(f"    ❌ {skill}")
        
        print(f"\nText Similarity: {data['text_similarity']:.1f}%")
        print(f"Semantic Similarity: {data['semantic_similarity']:.1f}%")
        
        print(f"\n📝 Recommendations:")
        for rec in data['recommendations']:
            print(f"  • {rec}")
        
        print("\n✓ Single match successful")
    else:
        print(f"❌ Error: {response.json()}")

def test_batch_match():
    """Test batch matching multiple resumes"""
    print("\n" + "="*70)
    print("5️⃣  TESTING BATCH RESUME MATCHING")
    print("="*70)
    
    # First upload all sample resumes
    sample_resumes_dir = "data/sample/resumes"
    uploaded_files = []
    
    if os.path.exists(sample_resumes_dir):
        for filename in os.listdir(sample_resumes_dir):
            file_path = os.path.join(sample_resumes_dir, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    files = {'file': (filename, f, 'text/plain')}
                    resp = requests.post(f"{BASE_URL}/resume/upload", files=files)
                    if resp.status_code == 200:
                        uploaded_files.append(filename)
                        print(f"  ✓ Uploaded: {filename}")
    
    # Now do batch matching
    job_data = {
        "job_description": {
            "title": "Data Scientist",
            "company": "DataMinds AI",
            "description": """
            Looking for a Data Scientist with ML expertise.
            
            Required Skills:
            - Python, R
            - Machine Learning, TensorFlow, PyTorch
            - SQL, NoSQL
            - Data visualization
            - NLP, Computer Vision
            
            Education: Master's degree preferred
            Experience: 3+ years
            """,
            "required_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "NLP"],
            "required_education": "masters",
            "required_years": 3
        }
    }
    
    response = requests.post(f"{BASE_URL}/match/batch", json=job_data)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 BATCH MATCH RESULTS")
        print(f"Job: {data['job_title']}")
        print(f"Total Candidates: {data['total_candidates']}")
        print(f"Processing Time: {data['processing_time']}s")
        
        print(f"\n🏆 TOP CANDIDATES (Ranked by Score):")
        for i, match in enumerate(data['matches'], 1):
            print(f"\n  {i}. {match['candidate_name']} ({match['filename']})")
            print(f"     Score: {match['overall_score']:.1f}% - {match['fit_level']}")
            print(f"     Skills: {match['skill_match']['match_percentage']:.1f}% " +
                  f"({match['skill_match']['total_matched']}/{match['skill_match']['total_required']})")
            
            if i <= 3:  # Show details for top 3
                print(f"     Missing: {', '.join(match['skill_match']['missing_skills'][:3])}")
        
        print("\n✓ Batch match successful")
    else:
        print(f"❌ Error: {response.json()}")

def test_list_resumes():
    """Test listing all uploaded resumes"""
    print("\n" + "="*70)
    print("6️⃣  TESTING LIST RESUMES")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/resumes/list")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal Resumes: {data['total']}")
        print(f"\nResumes:")
        for resume in data['resumes']:
            print(f"  • {resume['filename']} ({resume['size_kb']} KB)")
        
        print("\n✓ List resumes successful")
    else:
        print(f"❌ Error: {response.json()}")

def main():
    """Run all API tests"""
    
    print("="*70)
    print("RESUME SCREENING API - TEST SUITE")
    print("="*70)
    print(f"\nTesting API at: {BASE_URL}")
    print("Make sure the API is running before executing tests!")
    print("Run: python src/api/main.py")
    print("="*70)
    
    try:
        # Test 1: Health check
        test_health_check()
        
        # Test 2: Upload resume
        filename = test_upload_resume()
        
        if filename:
            # Test 3: Extract profile
            test_extract_profile(filename)
            
            # Test 4: Single match
            test_single_match(filename)
        
        # Test 5: Batch match
        test_batch_match()
        
        # Test 6: List resumes
        test_list_resumes()
        
        print("\n" + "="*70)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("Make sure the API is running:")
        print("  python src/api/main.py")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()