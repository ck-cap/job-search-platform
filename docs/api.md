# API Reference

## Backend API (Port 8000)

### Resume Parsing

**POST** `/parse_resume`

Upload and parse resume files (PDF/DOCX).

**Request:**
- `file`: Resume file (PDF or DOCX)

**Response:**
```json
{
  "filename": "resume.pdf",
  "parsed_data": {
    "contact_info": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-0123",
      "location": "New York, NY"
    },
    "summary": {
      "summary": "Brief overview",
      "full_text": "Complete summary text"
    },
    "experience": {
      "summary": "Experience overview",
      "full_text": "Complete experience details"
    },
    "education": {
      "summary": "Education overview", 
      "full_text": "Complete education details"
    },
    "skills": {
      "summary": "Skills overview",
      "full_text": "Complete skills list"
    }
  },
  "summary_recommendations": [
    "Recommendation 1",
    "Recommendation 2"
  ]
}
```

### Resume Analysis

**POST** `/analyze_resume`

Analyze parsed resume data and find matching jobs.

**Request:**
```json
{
  "parsed_data": {
    // Parsed resume data from parse_resume endpoint
  }
}
```

**Response:**
```json
{
  "job_matches": [
    {
      "title": "Software Engineer",
      "company": "Tech Corp",
      "similarity_score": 0.85,
      "description": "Job description..."
    }
  ]
}
```

## Model Service (Port 8001)

### Job Matching

**POST** `/match_jobs`

Find job matches for resume text.

**Request:**
```json
{
  "resume_text": "Resume content as text",
  "top_k": 5
}
```

**Response:**
```json
{
  "job_matches": [
    // Array of matching job objects
  ]
}
```

### Health Check

**GET** `/health`

Check model service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "job-matcher-model"
}
```

## Error Responses

All APIs return error responses in this format:

```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:
- `400`: Bad Request (invalid input)
- `500`: Internal Server Error
- `503`: Service Unavailable (model not loaded) 