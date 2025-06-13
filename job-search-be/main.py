import os
import json
import re
import logging
import tempfile
import subprocess
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load .env file and configure the API
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

# This prompt now only asks the AI to parse the content, not provide the filename.
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

Required JSON Structure (You should ONLY output this JSON structure):
{
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
    Processes a resume file. If it's a DOCX, it's converted to PDF first using LibreOffice.
    Then, the PDF is parsed using the multimodal LLM.
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
    logging.info("Received request for custom analysis.")
    return {"analysis": {"status": "Analysis logic pending implementation."}, "original_parsed_data": data}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Resume Analyzer API."}