import os
import json
import re
import logging
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai
import httpx
import pandas as pd
import numpy as np
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()
app = FastAPI(
    title="AI Resume Analyzer API",
    description="An API to upload, parse, and analyze resumes using a hybrid approach.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure the Google AI Client with the API key
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found.")
    genai.configure(api_key=api_key)
    logger.info("Google Generative AI client configured successfully.")
except ValueError as e:
    logger.error(f"API Key Configuration Error: {e}")

# Model Service Configuration
MODEL_SERVICE_URL = os.environ.get("MODEL_SERVICE_URL", "http://model-service:8001")
logger.info(f"Model service URL configured: {MODEL_SERVICE_URL}")

# CSV Data Configuration
CSV_DATA_PATH = os.environ.get("CSV_DATA_PATH", "/app/mock-data")
logger.info(f"CSV data path configured: {CSV_DATA_PATH}")

# Pydantic Models
class Company(BaseModel):
    id: int
    name: str
    industry: str
    size: str
    match: float
    description: str
    location: Optional[str] = None
    tagline: Optional[str] = None
    website: Optional[str] = None
    founded: Optional[str] = None
    employee_count: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None

class JobOpening(BaseModel):
    job_id: str
    job_title: str
    company: str
    job_text: str
    location: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    role: Optional[str] = None
    type: Optional[str] = None
    salary: Optional[str] = None
    listing_date: Optional[str] = None

class CompanyReview(BaseModel):
    id: int
    company: str
    job_title: Optional[str] = None
    rating: Optional[float] = None
    work_life_balance: Optional[float] = None
    culture_values: Optional[float] = None
    career_opp: Optional[float] = None
    comp_benefits: Optional[float] = None
    headline: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    date_review: Optional[str] = None
    current: Optional[str] = None
    location: Optional[str] = None

# Global data cache
company_data_cache = None
job_data_cache = None
review_data_cache = None

def load_csv_data():
    """Load and cache CSV data"""
    global company_data_cache, job_data_cache, review_data_cache
    
    try:
        # Load company info
        company_info_path = Path(CSV_DATA_PATH) / "company_info.csv"
        if company_info_path.exists():
            company_data_cache = pd.read_csv(company_info_path)
            logger.info(f"Loaded {len(company_data_cache)} companies from CSV")
        else:
            logger.warning(f"Company info CSV not found at {company_info_path}")
            company_data_cache = pd.DataFrame()
        
        # Load job vacancy data
        job_vacancy_path = Path(CSV_DATA_PATH) / "job_vacancy.csv"
        if job_vacancy_path.exists():
            job_data_cache = pd.read_csv(job_vacancy_path)
            logger.info(f"Loaded {len(job_data_cache)} jobs from CSV")
        else:
            logger.warning(f"Job vacancy CSV not found at {job_vacancy_path}")
            job_data_cache = pd.DataFrame()
        
        # Load review data
        review_path = Path(CSV_DATA_PATH) / "company_review.csv"
        if review_path.exists():
            review_data_cache = pd.read_csv(review_path)
            logger.info(f"Loaded {len(review_data_cache)} reviews from CSV")
        else:
            logger.warning(f"Company review CSV not found at {review_path}")
            review_data_cache = pd.DataFrame()
            
    except Exception as e:
        logger.error(f"Error loading CSV data: {e}")
        # Initialize empty DataFrames as fallback
        company_data_cache = pd.DataFrame()
        job_data_cache = pd.DataFrame()
        review_data_cache = pd.DataFrame()

def extract_skills_from_text(job_text: str) -> List[str]:
    """Extract skills from job description text"""
    if not job_text or pd.isna(job_text):
        return []
    
    skill_keywords = [
        'JavaScript', 'Python', 'Java', 'React', 'Node.js', 'Angular', 'Vue.js',
        'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'AWS', 'Azure', 'Docker', 
        'Kubernetes', 'Git', 'HTML', 'CSS', 'TypeScript', 'PHP', 'C++', 'C#',
        'Machine Learning', 'Data Analysis', 'Tableau', 'Excel', 'Figma',
        'Photoshop', 'Project Management', 'Agile', 'Scrum', 'DevOps',
        'TensorFlow', 'PyTorch', 'Pandas', 'NumPy'
    ]
    
    found_skills = []
    text_lower = str(job_text).lower()
    
    for skill in skill_keywords:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills[:5]  # Limit to 5 skills

def calculate_match_percentage(company_name: str, user_skills: List[str] = None) -> float:
    """Calculate match percentage for a company based on various factors"""
    try:
        # Base match score
        base_score = 50.0
        
        # Industry-based scoring (placeholder logic)
        industry_keywords = {
            'Technology': ['javascript', 'python', 'react', 'node'],
            'Data Science': ['python', 'sql', 'machine learning', 'data'],
            'Cloud Computing': ['aws', 'azure', 'docker', 'kubernetes'],
            'FinTech': ['finance', 'security', 'compliance'],
            'Healthcare': ['medical', 'healthcare', 'regulatory']
        }
        
        # Add some variation based on company name hash for demo
        import hashlib
        if not company_name:
            return 75.0  # default value for empty names
        
        name_hash = int(hashlib.md5(company_name.encode()).hexdigest()[:8], 16)
        variation = (name_hash % 30) + 70  # Between 70-99
        
        result = min(variation, 99.0)
        
        # Ensure the result is a valid float
        if pd.isna(result) or result == float('inf') or result == float('-inf'):
            return 75.0
        
        return float(result)
    except Exception:
        return 75.0  # Safe fallback

# Global helper function for safe float conversion
def safe_float(value, default=4.0):
    """Safely convert a value to float, handling NaN, infinity, and invalid values"""
    try:
        if pd.notna(value):
            result = float(value)
            # Check if result is finite (not NaN, inf, or -inf)
            if pd.notna(result) and result != float('inf') and result != float('-inf'):
                return result
        return default
    except (ValueError, TypeError):
        return default

def make_json_safe(obj):
    """Recursively make an object safe for JSON serialization"""
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            safe_v = make_json_safe(v)
            # Special handling for location fields
            if k == 'location' and (safe_v == 0.0 or safe_v == '0.0' or safe_v == 0):
                safe_v = 'Malaysia'
            result[k] = safe_v
        return result
    elif isinstance(obj, list):
        return [make_json_safe(item) for item in obj]
    elif isinstance(obj, (int, str, bool)) or obj is None:
        return obj
    elif isinstance(obj, float):
        if pd.isna(obj) or obj == float('inf') or obj == float('-inf'):
            return 0.0
        return obj
    elif hasattr(obj, 'item'):  # numpy types
        try:
            return obj.item()
        except (ValueError, OverflowError):
            return 0
    else:
        # Try to convert to string as last resort
        try:
            return str(obj)
        except:
            return None

# Load CSV data on startup
load_csv_data()

# Prompts and Helper Functions
COMBINED_PROMPT = """
You are a highly advanced resume parsing system and expert career coach. Your task is to analyze the attached resume and convert its content into a single, structured JSON object.

The output MUST be a single, valid JSON object and nothing else.

Your tasks are:
1.  **Parse the Resume**: Convert the resume content into a structured JSON object under the `parsed_data` key. Group the content into standard categories: "contact_info", "summary", "experience", "education", "skills", "projects", "certificates". For each section, provide both `full_text` and a concise `summary`.
2.  **Provide Summary Recommendations**: Based on the parsed summary, provide 3-4 actionable recommendations for improvement under the `summary_recommendations` key. These recommendations should be concise, specific, and professional.

Required JSON Structure:
{
    "parsed_data": {
        "contact_info": { "name": "[Name]", "phone": "[Phone]", "email": "[Email]", "location": "[Location]" },
        "summary": { "summary": "[...]", "full_text": "[...]" },
        "experience": { "summary": "[...]", "full_text": "[...]" },
        "education": { "summary": "[...]", "full_text": "[...]" },
        "skills": { "summary": "[...]", "full_text": "[...]" }
    },
    "summary_recommendations": [
        "Recommendation 1...",
        "Recommendation 2..."
    ]
}
"""

def convert_docx_to_pdf_linux(docx_path: str, output_dir: str):
    """
    Converts a DOCX file to PDF using the LibreOffice command-line tool.
    This is designed for a Linux/Docker environment where LibreOffice is installed.
    """
    logger.info(f"Attempting to convert {docx_path} to PDF in {output_dir}")
    command = [
        "libreoffice",
        "--headless",          # Run without a GUI
        "--convert-to", "pdf", # Specify the output format
        "--outdir", output_dir, # Specify the output directory
        docx_path,             # The input file
    ]
    try:
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=True)
        logger.info(f"LibreOffice stdout: {process.stdout.decode('utf-8')}")
        pdf_filename = Path(docx_path).stem + ".pdf"
        if not (Path(output_dir) / pdf_filename).exists():
            raise FileNotFoundError("Conversion succeeded but output PDF not found.")
    except FileNotFoundError:
        logger.error("COMMAND NOT FOUND: 'libreoffice'. Is it installed in the container?")
        raise
    except subprocess.CalledProcessError as e:
        logger.error(f"LibreOffice conversion failed. Stderr: {e.stderr.decode('utf-8')}")
        raise
    except subprocess.TimeoutExpired:
        logger.error("LibreOffice conversion timed out after 30 seconds.")
        raise

async def robust_json_parser(response_text: str) -> dict:
    """A helper function to safely extract and parse JSON from an LLM's response."""
    logging.debug(f"LLM Raw Response Text: {response_text}")
    json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
    
    if not json_match:
        logging.error("No JSON object found in the LLM response. Response was: %s", response_text)
        raise ValueError("LLM response did not contain a valid JSON object.")
        
    json_string = json_match.group(0)
    
    try:
        parsed_data = json.loads(json_string)
        logging.info("Successfully parsed structured JSON from LLM response.")
        return parsed_data
    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {e}. Problematic string: {json_string}")
        raise ValueError("Failed to decode JSON from AI model response.")

async def parse_resume_from_pdf_file(pdf_path: str) -> dict:
    """Sends a PDF file to Gemini for multimodal parsing."""
    logger.info(f"Using multimodal parsing for PDF file: {pdf_path}")
    uploaded_file_gemini = None
    try:
        uploaded_file_gemini = await run_in_threadpool(genai.upload_file, path=pdf_path)
        logging.info(f"Successfully uploaded file. Gemini name: {uploaded_file_gemini.name}")

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await model.generate_content_async([COMBINED_PROMPT, uploaded_file_gemini])
        return await robust_json_parser(response.text)
    
    except Exception as e:
        logging.exception("An error occurred during the multimodal parsing process.")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    finally:
        if uploaded_file_gemini:
            await run_in_threadpool(genai.delete_file, name=uploaded_file_gemini.name)
            logging.info(f"Cleaned up uploaded file {uploaded_file_gemini.name}.")

# --- API Endpoints ---
@app.post("/parse_resume")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    """
    Processes a resume file. Converts DOCX to PDF if necessary, then uses a single
    AI call to get both the parsed data and summary recommendations.
    """
    logger.info(f"Received request for file: {file.filename} (MIME: {file.content_type})")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        original_file_path = temp_dir_path / file.filename
        
        with open(original_file_path, "wb") as f:
            f.write(await file.read())
        
        pdf_to_process_path = original_file_path

        # If it's a docx, convert it to PDF
        if file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file.filename.endswith(".docx"):
            logging.info("DOCX file detected. Attempting to convert to PDF via LibreOffice...")
            try:
                # Use our new subprocess function
                await run_in_threadpool(convert_docx_to_pdf_linux, str(original_file_path), str(temp_dir_path))
                pdf_to_process_path = original_file_path.with_suffix('.pdf')
                logging.info(f"Successfully converted to {pdf_to_process_path}")
            except Exception as e:
                logging.exception("Failed to convert DOCX to PDF.")
                raise HTTPException(status_code=500, detail=f"Error converting DOCX to PDF: {e}")

        if pdf_to_process_path.suffix.lower() != ".pdf":
             raise HTTPException(status_code=400, detail=f"File type not supported for multimodal analysis: {file.filename}")

        # The model now returns only the parsed data (contact_info, experience, etc.)
        parsed_content_data = await parse_resume_from_pdf_file(str(pdf_to_process_path))

    logging.info(f"Successfully processed. Returning parsed data for {file.filename}.")
    
    # Construct the final, correct JSON response here.
    final_response = {
        "filename": file.filename,
        "parsed_data": parsed_content_data
    }

    return final_response

@app.post("/analyze_resume")
async def analyze_resume_endpoint(data: dict):
    """
    Analyzes the parsed resume data by calling the model service to find matching jobs.
    """
    logger.info("Received request for custom job analysis.")
    try:
        parsed_data = data.get('parsed_data', {})
        summary_text = parsed_data.get('summary', {}).get('full_text', '')
        experience_text = parsed_data.get('experience', {}).get('full_text', '')
        skills_text = parsed_data.get('skills', {}).get('full_text', '')
        
        query_text = f"{summary_text}\n{experience_text}\n{skills_text}"
        
        # Call the model service
        async with httpx.AsyncClient() as client:
            model_response = await client.post(
                f"{MODEL_SERVICE_URL}/match_jobs",
                json={"resume_text": query_text, "top_k": 5},
                timeout=30.0
            )
            
            if model_response.status_code != 200:
                logger.error(f"Model service returned status {model_response.status_code}: {model_response.text}")
                raise HTTPException(status_code=500, detail="Model service unavailable")
            
            model_data = model_response.json()
            job_matches = model_data.get("job_matches", [])
            
        return {
            "analysis": {"job_matches": job_matches},
            "original_parsed_data": data
        }
    except httpx.RequestError as e:
        logger.exception(f"Error connecting to model service: {e}")
        raise HTTPException(status_code=500, detail="Unable to connect to model service")
    except Exception as e:
        logger.exception("An error occurred during custom analysis.")
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")


# --- CSV-based Company and Job Endpoints ---

@app.get("/companies")
async def get_companies(
    industry: Optional[List[str]] = Query(None, description="Filter by industry (can be multiple)"),
    size: Optional[str] = Query(None, description="Filter by company size"),
    search: Optional[str] = Query(None, description="Search companies by name or description"),
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    limit: int = Query(12, ge=1, le=100, description="Number of companies per page")
):
    """Get list of companies with optional filtering and pagination"""
    logger.info(f"GET /companies - page={page}, limit={limit}, industry={industry}, size={size}, search={search}")
    try:
        if company_data_cache.empty:
            # Return fallback data if CSV not loaded
            return {
                "companies": [],
                "pagination": {
                    "current_page": 1,
                    "total_pages": 0,
                    "total_companies": 0,
                    "per_page": limit,
                    "has_next": False,
                    "has_prev": False
                }
            }
        
        # Start with all companies
        filtered_companies = company_data_cache.copy()
        
        # Apply filters
        if industry and len(industry) > 0:
            if 'industry' in filtered_companies.columns:
                # Handle multiple industries with OR logic
                industry_mask = pd.Series([False] * len(filtered_companies))
                for ind in industry:
                    industry_mask |= filtered_companies['industry'].str.contains(ind, case=False, na=False)
                filtered_companies = filtered_companies[industry_mask]
        
        if search:
            if 'Company' in filtered_companies.columns:
                search_mask = filtered_companies['Company'].str.contains(search, case=False, na=False)
                if 'description' in filtered_companies.columns:
                    search_mask |= filtered_companies['description'].str.contains(search, case=False, na=False)
                filtered_companies = filtered_companies[search_mask]
        
        # Calculate pagination
        total_companies = len(filtered_companies)
        offset = (page - 1) * limit
        
        # Get paginated data
        paginated_companies = filtered_companies.iloc[offset:offset + limit]
        
        # Convert to list of dictionaries
        companies = []
        for idx, row in paginated_companies.iterrows():
            company = {
                "id": idx + 1,
                "name": row.get('Company', f'Company {idx + 1}'),
                "industry": row.get('industry', 'Technology'),
                "size": row.get('size', 'Mid-size (100-500)'),
                "description": row.get('description', row.get('Review Summary', 'No description available')),
                "match": calculate_match_percentage(row.get('Company', '')),
                "location": row.get('headquarters', 'Malaysia')
            }
            companies.append(company)
        
        # Sort by match percentage descending
        companies.sort(key=lambda x: x['match'], reverse=True)
        
        # Calculate pagination metadata
        total_pages = (total_companies + limit - 1) // limit
        
        return make_json_safe({
            "companies": companies,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_companies": total_companies,
                "per_page": limit,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching companies: {e}")
        return {
            "companies": [],
            "pagination": {
                "current_page": 1,
                "total_pages": 0,
                "total_companies": 0,
                "per_page": limit,
                "has_next": False,
                "has_prev": False
            }
        }

@app.get("/companies/{company_name}")
async def get_company_details(company_name: str):
    """Get detailed information about a specific company"""
    try:
        logger.info(f"Fetching company details for: {company_name}")
        # Convert URL slug back to potential company name
        # First, convert hyphens to spaces
        potential_name = company_name.replace('-', ' ')
        
        # Try to find exact match in company data first
        clean_company_name = None
        if not company_data_cache.empty and 'Company' in company_data_cache.columns:
            # Look for companies that match when both are stripped of punctuation and lowercased
            for company in company_data_cache['Company'].dropna():
                company_clean = ''.join(c.lower() for c in company if c.isalnum() or c.isspace())
                potential_clean = ''.join(c.lower() for c in potential_name if c.isalnum() or c.isspace())
                if company_clean == potential_clean:
                    clean_company_name = company
                    break
        
        # Fallback to title case if no exact match found
        if clean_company_name is None:
            clean_company_name = potential_name.title()
        
        # Find company in data using the exact name we found
        company_row = None
        if not company_data_cache.empty and 'Company' in company_data_cache.columns:
            exact_match = company_data_cache[
                company_data_cache['Company'] == clean_company_name
            ]
            if not exact_match.empty:
                company_row = exact_match.iloc[0]
        
        # Get company reviews using exact company name
        company_reviews = []
        if not review_data_cache.empty and 'Company' in review_data_cache.columns:
            reviews_for_company = review_data_cache[
                review_data_cache['Company'] == clean_company_name
            ].head(10)  # Limit to 10 reviews
            
            for idx, review in reviews_for_company.iterrows():
                company_reviews.append({
                    "id": int(idx) if pd.notna(idx) else 0,
                    "rating": safe_float(review.get('overall_rating'), 4.0),
                    "title": review.get('headline', 'Employee Review'),
                    "position": review.get('job_title', 'Employee'),
                    "location": review.get('location', 'Malaysia') if review.get('location') and str(review.get('location')).strip() and str(review.get('location')) != '0.0' else 'N/A',
                    "date": review.get('date_review', '2024'),
                    "employment": review.get('current', 'N/A'),
                    "pros": review.get('pros', 'N/A'),
                    "cons": review.get('cons', 'N/A'),
                })
        
        # Get job openings for this company using exact company name
        company_jobs = []
        if not job_data_cache.empty and 'company' in job_data_cache.columns:
            jobs_for_company = job_data_cache[
                job_data_cache['company'] == clean_company_name
            ].head(5)  # Limit to 5 jobs
            
            for idx, job in jobs_for_company.iterrows():
                company_jobs.append({
                    "job_id": str(job.get('job_id', int(idx) if pd.notna(idx) else 0)),
                    "job_title": job.get('job_title', 'N/A'),
                    "category": job.get('category', 'N/A'),
                    "subcategory": job.get('subcategory', 'N/A'),
                    "location": job.get('location', 'N/A'),
                    "type": job.get('type', 'N/A'),
                    "salary": job.get('salary', 'N/A'),
                    "job_text": job.get('job_text', 'N/A'),
                    "role": job.get('role', 'N/A')
                })
        
        # Calculate average ratings
        avg_rating = 0.0
        review_count = len(company_reviews)
        if company_reviews:
            # Filter out any NaN ratings and ensure we have valid numbers
            valid_ratings = [r['rating'] for r in company_reviews if isinstance(r['rating'], (int, float)) and not pd.isna(r['rating'])]
            if valid_ratings:
                avg_rating = sum(valid_ratings) / len(valid_ratings)
            else:
                avg_rating = 0.0  # fallback if no valid ratings
        
        # Ensure avg_rating is valid
        if not isinstance(avg_rating, (int, float)) or pd.isna(avg_rating):
            avg_rating = 0.0
        
        # Build company details using actual CSV data
        company_details = {
            "name": company_row.get('Company') if company_row is not None else clean_company_name,
            "tagline": company_row.get('tagline', 'N/A') if company_row is not None else 'N/A',
            "location": company_row.get('headquarters', 'N/A') if company_row is not None else 'N/A',
            "industry": company_row.get('industry', 'N/A') if company_row is not None else 'N/A',
            "size": company_row.get('size', 'N/A') if company_row is not None else 'N/A',
            "rating": round(avg_rating, 0),
            "reviewCount": review_count,
            "workLifeBalance": round(avg_rating * 0.95, 0),
            "culture": round(avg_rating * 1.05, 0),
            "careerOpportunities": round(avg_rating * 0.9, 0),
            "founded": company_row.get('founded', 'N/A') if company_row is not None else 'N/A',
            "employeeCount": company_row.get('employee_count', 'N/A') if company_row is not None else 'N/A',
            "headquarters": company_row.get('headquarters', 'N/A') if company_row is not None else 'N/A',
            "website": company_row.get('website', 'N/A') if company_row is not None else 'N/A',
            "description": company_row.get('description', 'N/A') if company_row is not None else 'N/A',
            "mission": company_row.get('mission', 'N/A') if company_row is not None else 'N/A',
            "reviewSummary": company_row.get('Review Summary', 'N/A') if company_row is not None else 'N/A',
            "benefits": company_row.get('benefits', 'N/A').split(', ') if company_row is not None and company_row.get('benefits') else [
                "N/A",
            ],
            "openJobs": company_jobs,
            "reviews": company_reviews
        }
        
        return make_json_safe(company_details)
        
    except Exception as e:
        logger.error(f"Error fetching company details for {company_name}: {e}")
        raise HTTPException(status_code=404, detail="Company not found")

@app.get("/jobs")
async def get_jobs(
    company: Optional[str] = Query(None, description="Filter by company"),
    category: Optional[str] = Query(None, description="Filter by job category"),
    location: Optional[str] = Query(None, description="Filter by location"),
    limit: int = Query(20, description="Maximum number of jobs to return")
):
    """Get list of job openings with optional filtering"""
    try:
        if job_data_cache.empty:
            return []
        
        # Start with all jobs
        filtered_jobs = job_data_cache.copy()
        
        # Apply filters
        if company:
            if 'company' in filtered_jobs.columns:
                filtered_jobs = filtered_jobs[
                    filtered_jobs['company'].str.contains(company, case=False, na=False)
                ]
        
        if category:
            if 'category' in filtered_jobs.columns:
                filtered_jobs = filtered_jobs[
                    filtered_jobs['category'].str.contains(category, case=False, na=False)
                ]
        
        if location:
            if 'location' in filtered_jobs.columns:
                filtered_jobs = filtered_jobs[
                    filtered_jobs['location'].str.contains(location, case=False, na=False)
                ]
        
        # Convert to list of dictionaries
        jobs = []
        for idx, row in filtered_jobs.head(limit).iterrows():
            job = {
                "job_id": str(row.get('job_id', int(idx) if pd.notna(idx) else 0)),
                "job_title": row.get('job_title', 'Software Engineer'),
                "company": row.get('company', 'Tech Company'),
                "job_text": row.get('job_text', 'Great opportunity'),
                "location": row.get('location', 'Malaysia'),
                "category": row.get('category', 'Technology'),
                "subcategory": row.get('subcategory', 'Software'),
                "role": row.get('role', 'Engineer'),
                "type": row.get('type', 'Full-time'),
                "salary": row.get('salary', 'Competitive'),
                "listing_date": row.get('listingDate', '2024-01-01'),
                "skills": extract_skills_from_text(row.get('job_text', ''))
            }
            jobs.append(job)
        
        return make_json_safe(jobs)
        
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        return []

@app.get("/reviews/{company_name}")
async def get_company_reviews(
    company_name: str,
    limit: int = Query(10, description="Maximum number of reviews to return")
):
    """Get reviews for a specific company"""
    try:
        if review_data_cache.empty:
            return []
        
        # Clean up company name
        clean_company_name = company_name.replace('-', ' ').title()
        
        # Find reviews for this company - remove periods for search but preserve original names in results
        company_reviews = review_data_cache[
            review_data_cache['Company'].str.contains(clean_company_name.replace('.', ''), case=False, na=False)
        ].head(limit)
        
        reviews = []
        for idx, review in company_reviews.iterrows():
            reviews.append({
                "id": int(idx) if pd.notna(idx) else 0,
                "company": review.get('Company'),
                "job_title": review.get('job_title', 'Employee'),
                "rating": safe_float(review.get('overall_rating'), 4.0),
                "work_life_balance": safe_float(review.get('work_life_balance'), 4.0),
                "culture_values": safe_float(review.get('culture_values'), 4.0),
                "career_opp": safe_float(review.get('career_opp'), 4.0),
                "comp_benefits": safe_float(review.get('comp_benefits'), 4.0),
                "headline": review.get('headline', 'Employee Review'),
                "pros": review.get('pros', 'Good workplace'),
                "cons": review.get('cons', 'Some areas for improvement'),
                "date_review": review.get('date_review', '2024'),
                "current": review.get('current', 'Current Employee'),
                "location": review.get('location', 'Malaysia') if review.get('location') and str(review.get('location')).strip() and str(review.get('location')) != '0.0' else 'Malaysia'
            })
        
        return make_json_safe(reviews)
        
    except Exception as e:
        logger.error(f"Error fetching reviews for {company_name}: {e}")
        return []

@app.get("/industries")
async def get_industries():
    """Get list of available industries"""
    try:
        if company_data_cache.empty or 'industry' not in company_data_cache.columns:
            # Return default industries if CSV not available
            return [
                "Technology", "Data Science", "Cloud Computing", "FinTech", 
                "Healthcare", "Manufacturing", "Retail", "Finance"
            ]
        
        industries = company_data_cache['industry'].dropna().unique().tolist()
        return sorted(industries)
        
    except Exception as e:
        logger.error(f"Error fetching industries: {e}")
        return ["Technology", "Data Science", "Cloud Computing"]

@app.post("/reload-data")
async def reload_csv_data():
    """Reload CSV data (useful for development)"""
    try:
        load_csv_data()
        return {
            "message": "CSV data reloaded successfully",
            "companies_count": len(company_data_cache) if not company_data_cache.empty else 0,
            "jobs_count": len(job_data_cache) if not job_data_cache.empty else 0,
            "reviews_count": len(review_data_cache) if not review_data_cache.empty else 0
        }
    except Exception as e:
        logger.error(f"Error reloading CSV data: {e}")
        raise HTTPException(status_code=500, detail="Failed to reload CSV data")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Resume Analyzer API."}