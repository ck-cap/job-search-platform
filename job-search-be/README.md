# Job Search Backend (PoC)

This is the FastAPI backend for the Job Search Platform Proof of Concept.

## Features
- Resume upload endpoint (supports .pdf and .docx)
- CORS enabled for local frontend development
- Ready for resume parsing, analysis, and job recommendation endpoints

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the development server:**
   ```bash
   uvicorn main:app --reload
   ```

3. **API Docs:**
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

---

## Next Steps
- Implement resume parsing and analysis endpoints
- Add job recommendation logic 