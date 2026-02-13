# Resume Screening API Documentation

## Base URL
```
http://localhost:8000
```

## Interactive Documentation
Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Authentication
Currently, no authentication is required. In production, implement OAuth2/JWT.

---

## Endpoints

### 1. Health Check
**GET** `/health`

Check API health and model status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-12T10:30:00",
  "models_loaded": true,
  "version": "1.0.0"
}
```

---

### 2. Upload Resume
**POST** `/resume/upload`

Upload a resume file (PDF, DOCX, or TXT).

**Request:**
- Content-Type: `multipart/form-data`
- Body: File upload

**Response:**
```json
{
  "filename": "John_Doe_Resume.txt",
  "file_size": 2048,
  "extracted_text_length": 1500,
  "processing_status": "success",
  "message": "Resume uploaded and processed successfully"
}
```

---

### 3. Extract Profile
**GET** `/resume/profile/{filename}`

Extract complete candidate profile from uploaded resume.

**Parameters:**
- `filename` (path): Name of uploaded resume

**Response:**
```json
{
  "filename": "John_Doe_Resume.txt",
  "name": "John Doe",
  "email": "john.doe@email.com",
  "phone": "+27 123 456 789",
  "linkedin": "linkedin.com/in/johndoe",
  "github": "github.com/johndoe",
  "years_experience": 6,
  "skills": {
    "skills": ["Python", "Django", "AWS", "Docker"],
    "total_skills": 25,
    "categories": {
      "programming_languages": ["Python", "JavaScript"],
      "cloud_platforms": ["AWS"]
    },
    "skill_count": {"Python": 5, "Django": 3}
  },
  "education": {
    "highest_level": "bachelors",
    "has_degree": true,
    "found_degrees": [...]
  },
  "experience_level": "senior",
  "certifications": ["AWS Certified Solutions Architect"]
}
```

---

### 4. Match Single Resume
**POST** `/match/single`

Match a single resume to a job description.

**Parameters:**
- `filename` (query): Resume filename

**Request Body:**
```json
{
  "title": "Senior Python Developer",
  "company": "TechCorp",
  "description": "We are seeking...",
  "required_skills": ["Python", "Django", "AWS"],
  "required_education": "bachelors",
  "required_years": 5
}
```

**Response:**
```json
{
  "candidate_name": "John Doe",
  "filename": "John_Doe_Resume.txt",
  "overall_score": 85.5,
  "fit_level": "Excellent",
  "skill_match": {
    "match_percentage": 80.0,
    "matched_skills": ["Python", "Django", "AWS"],
    "missing_skills": ["Kubernetes"],
    "extra_skills": ["React", "MongoDB"],
    "total_required": 5,
    "total_matched": 4
  },
  "experience_match": {
    "score": 100,
    "meets_requirement": true,
    "difference": 1
  },
  "education_match": {
    "score": 100,
    "meets_requirement": true
  },
  "text_similarity": 75.5,
  "semantic_similarity": 82.3,
  "recommendations": [
    "Excellent fit - Highly recommended for interview"
  ]
}
```

---

### 5. Batch Match Resumes
**POST** `/match/batch`

Match multiple resumes to a job description.

**Request Body:**
```json
{
  "job_description": {
    "title": "Data Scientist",
    "company": "DataMinds AI",
    "description": "Looking for...",
    "required_skills": ["Python", "Machine Learning"],
    "required_education": "masters",
    "required_years": 3
  },
  "resume_filenames": ["resume1.txt", "resume2.txt"]
}
```

**Response:**
```json
{
  "job_title": "Data Scientist",
  "total_candidates": 3,
  "matches": [
    {
      "candidate_name": "Sarah Johnson",
      "overall_score": 92.5,
      "fit_level": "Excellent",
      ...
    },
    ...
  ],
  "processing_time": 2.5
}
```

---

### 6. List Resumes
**GET** `/resumes/list`

List all uploaded resumes.

**Response:**
```json
{
  "resumes": [
    {
      "filename": "John_Doe_Resume.txt",
      "size_bytes": 2048,
      "size_kb": 2.0,
      "uploaded_at": "2024-02-12T10:00:00"
    }
  ],
  "total": 3
}
```

---

### 7. Delete Resume
**DELETE** `/resume/{filename}`

Delete an uploaded resume.

**Parameters:**
- `filename` (path): Resume filename

**Response:**
```json
{
  "message": "Resume John_Doe_Resume.txt deleted successfully"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid file type. Allowed types: .pdf, .docx, .txt"
}
```

### 404 Not Found
```json
{
  "detail": "Resume file not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing file: ..."
}
```

---

## Usage Examples

### Python
```python
import requests

# Upload resume
files = {'file': open('resume.pdf', 'rb')}
response = requests.post('http://localhost:8000/resume/upload', files=files)
print(response.json())

# Match resume
job = {
    "title": "Software Engineer",
    "company": "Tech Inc",
    "description": "...",
    "required_skills": ["Python", "Django"]
}
response = requests.post(
    'http://localhost:8000/match/single?filename=resume.pdf',
    json=job
)
print(response.json())
```

### JavaScript
```javascript
// Upload resume
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/resume/upload', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Rate Limiting
Currently no rate limiting. In production, implement rate limiting using middleware.

## CORS
CORS is enabled for all origins in development. Restrict in production.

## Deployment
For production deployment:
1. Use environment variables for configuration
2. Implement authentication (OAuth2/JWT)
3. Add rate limiting
4. Use HTTPS
5. Configure proper CORS
6. Set up logging and monitoring
7. Use production ASGI server (Gunicorn + Uvicorn)