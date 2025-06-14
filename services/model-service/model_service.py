import os
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from model import JobMatcher
import asyncio
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Global variable to hold the matcher
matcher = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the application lifecycle"""
    global matcher
    
    # Startup
    logger.info("Starting model service...")
    try:
        MODEL_PATH = os.environ.get("MODEL_PATH", "/app/model/fine_tuned_mpnet_with_eval")
        DATASET_PATH = os.environ.get("DATASET_PATH", "/app/dataset/mpnet_finetune_dataset_test.csv")
        
        # Check if files exist before loading
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model path does not exist: {MODEL_PATH}")
        if not os.path.exists(DATASET_PATH):
            raise FileNotFoundError(f"Dataset path does not exist: {DATASET_PATH}")

        matcher = JobMatcher(
            model_path=str(MODEL_PATH),
            dataset_path=str(DATASET_PATH)
        )
        logger.info("JobMatcher model loaded successfully in model service.")
    except FileNotFoundError as e:
        logger.error(f"ERROR: A required file was not found: {e}")
        raise SystemExit(f"Model loading failed: {e}")
    except Exception as e:
        logger.error(f"ERROR: An unexpected error occurred while loading the model: {e}")
        raise SystemExit(f"An unexpected model loading error occurred: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down model service...")

app = FastAPI(
    title="Job Matcher Model Service",
    description="A dedicated service for job matching using fine-tuned models",
    version="1.0.0",
    lifespan=lifespan
)

# Request/Response models
class JobMatchRequest(BaseModel):
    resume_text: str
    top_k: int = 5

class JobMatchResponse(BaseModel):
    job_matches: list

@app.post("/match_jobs", response_model=JobMatchResponse)
async def match_jobs(request: JobMatchRequest):
    """
    Find matching jobs for the given resume text.
    """
    global matcher
    
    if matcher is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet. Please try again later.")
    
    try:
        if not request.resume_text.strip():
            raise HTTPException(status_code=400, detail="Resume text cannot be empty")
        
        job_matches = matcher.find_top_matches(request.resume_text, top_k=request.top_k)
        
        return JobMatchResponse(job_matches=job_matches)
    
    except Exception as e:
        logger.exception("Error during job matching")
        raise HTTPException(status_code=500, detail=f"Error during job matching: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global matcher
    
    if matcher is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {"status": "healthy", "service": "job-matcher-model"}

@app.get("/")
async def read_root():
    return {"message": "Job Matcher Model Service is running"} 