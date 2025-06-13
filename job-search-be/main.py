import os
import json
import re
import logging
import tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from docx2pdf import convert
import google.generativeai as genai

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load .env file and configure the API
load_dotenv()

app = FastAPI(
    title="AI Resume Analyzer API",
    description="An API to upload, parse, and analyze resumes using a hybrid approach.",
    version="6.0.0"
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
    logging.info("Google Generative AI client configured successfully.")
except ValueError as e:
    logging.error(f"API Key Configuration Error: {e}")

ADVANCED_PROMPT = """
You are a highly advanced and precise resume parsing system. Your task is to analyze the attached resume file and convert its content into a structured JSON object.

The output MUST be a single, valid JSON object and nothing else. Do not include any explanatory text or markdown formatting.

First, use your semantic understanding to identify logical sections of the resume, even if the titles are unconventional. Group the content into the following standard categories:
- "contact_info"
- "summary" (this could be titled "Objective", "Profile", or "Summary")
- "experience" (this could be titled "Work History", "Employment", etc.)
- "education"
- "skills"
- "projects"
- "certificates"

Then, format the output into a JSON object with the keys listed above.

For each key (except "contact_info"), the value should be an object with two sub-keys: "full_text" and "summary".

- **full_text**: Place the raw, verbatim text for that semantically-grouped section here.
- **summary**: Create a concise summary of the `full_text`. For "experience" and "projects", summarize the key achievements. For "skills" and "certificates", create a clean, comma-separated list of the items.

If a section cannot be found, the value for two sub-keys should be `null`.

Required JSON Structure:
{
    "filename": "[Filename]",
    "parsed_data": {
        "contact_info": {
            "name": "[Name]",
            "phone": "[Phone Number]",
            "email": "[Email Address]",
            "location": "[Location]"
        },
        "summary": {
            "summary": "[Summary of Professional Background]",
            "full_text": "[Detailed Professional Summary]"
        },
        "experience": {
            "summary": "[Summary of Work Experience]",
            "full_text": "[Detailed Description of Work Experience]"
        },
        "education": {
            "summary": "[Summary of Educational Background]",
            "full_text": "[Detailed Description of Education]"
        },
        "skills": {
            "summary": "[Summary of Skills]",
            "full_text": "[Detailed List of Skills]"
        },
        "projects": {
            "summary": "[Summary of Projects]",
            "full_text": "[Detailed Description of Projects]"
        },
        "certificates": {
            "summary": "[Summary of Certificates]",
            "full_text": "[Detailed List of Certificates]"
        }
    }
}
"""

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

async def parse_resume_from_pdf_file(pdf_path: str, original_filename: str) -> dict:
    """Saves a supported file (like PDF) temporarily and sends it to Gemini."""
    logging.info(f"Using multimodal parsing for PDF file: {pdf_path}")
    uploaded_file_gemini = None
    try:
        uploaded_file_gemini = await run_in_threadpool(genai.upload_file, path=pdf_path)
        logging.info(f"Successfully uploaded file. Gemini name: {uploaded_file_gemini.name}")

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await model.generate_content_async([ADVANCED_PROMPT, uploaded_file_gemini])
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
    Processes a resume file. If it's a DOCX, it's converted to PDF first.
    Then, the PDF is parsed using the multimodal LLM.
    """
    logging.info(f"Received request for file: {file.filename} (MIME: {file.content_type})")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        original_file_path = temp_dir_path / file.filename
        
        # Save the uploaded file to the temporary directory
        with open(original_file_path, "wb") as f:
            f.write(await file.read())
        
        pdf_to_process_path = original_file_path

        # If it's a docx, convert it to PDF
        if file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file.filename.endswith(".docx"):
            logging.info("DOCX file detected. Attempting to convert to PDF...")
            pdf_path = original_file_path.with_suffix('.pdf')
            try:
                # NOTE: For Docker, this requires LibreOffice to be installed in the container.
                # Example Dockerfile command: RUN apt-get update && apt-get install -y libreoffice
                await run_in_threadpool(convert, str(original_file_path), str(pdf_path))
                pdf_to_process_path = pdf_path
                logging.info(f"Successfully converted to {pdf_to_process_path}")
            except Exception as e:
                logging.exception("Failed to convert DOCX to PDF. Make sure LibreOffice (on Linux) or MS Word (on Windows) is installed.")
                raise HTTPException(status_code=500, detail="Error converting DOCX to PDF.")

        # Ensure we are working with a PDF before proceeding
        if pdf_to_process_path.suffix.lower() != ".pdf":
             raise HTTPException(status_code=400, detail=f"File type not supported for multimodal analysis: {file.filename}")

        parsed_sections = await parse_resume_from_pdf_file(str(pdf_to_process_path), file.filename)

    logging.info(f"Successfully processed. Returning parsed data for {file.filename}.")
    return {"filename": file.filename, "parsed_data": parsed_sections}

@app.post("/analyze_resume")
async def analyze_resume_endpoint(data: dict):
    logging.info("Received request for custom analysis.")
    return {"analysis": {"status": "Analysis logic pending implementation."}, "original_parsed_data": data}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Resume Analyzer API."}