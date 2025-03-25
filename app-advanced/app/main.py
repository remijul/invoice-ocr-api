"""
Main entry point for the Invoice OCR API.
This module defines the FastAPI application and its endpoints.
"""
import os
import shutil
import time
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .models import OCRResponse
from .ocr_processor import process_invoice
from .auth import authenticate_user
from .logger import app_logger

# Load environment variables from .env file
load_dotenv()

# Get upload directory from environment variable or use default
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_files")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize FastAPI application
app = FastAPI(
    title="Invoice OCR API",
    description="API for extracting data from invoice images using OCR",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
except:
    # Create the directory if it doesn't exist
    os.makedirs("app/static", exist_ok=True)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    """
    Root endpoint - returns a welcome message.
    """
    app_logger.info("Root endpoint accessed")
    return {"message": "Welcome to Invoice OCR API"}

@app.post("/extract/", response_model=OCRResponse)
async def extract_invoice_data(
    file: UploadFile = File(...),
    username: str = Depends(authenticate_user)
):
    """
    Extract data from an uploaded invoice file.
    
    Parameters:
    - file: The invoice file (PDF, PNG, or JPEG)
    
    Returns:
    - OCRResponse: Extracted invoice data
    """
    app_logger.info(f"User {username} requested data extraction for file: {file.filename}")
    
    # Get allowed extensions from environment variable or use defaults
    allowed_extensions = os.getenv("ALLOWED_EXTENSIONS", "pdf,png,jpg,jpeg")
    valid_extensions = ["." + ext.strip() for ext in allowed_extensions.split(",")]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in valid_extensions:
        error_msg = f"Invalid file type. Supported types: {', '.join(valid_extensions)}"
        app_logger.warning(f"Invalid file type attempt: {file_ext} for file {file.filename}")
        raise HTTPException(
            status_code=400,
            detail=error_msg
        )
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Record start time for performance logging
        start_time = time.time()
        
        # Process the invoice with OCR
        result = process_invoice(file_path)
        
        # Log processing time
        processing_time = time.time() - start_time
        app_logger.info(f"Processed {file.filename} in {processing_time:.2f} seconds")
        
        # Return the extracted data
        return OCRResponse(
            filename=file.filename,
            extracted_data=result
        )
    except Exception as e:
        app_logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing invoice: {str(e)}")
    finally:
        # Clean up - remove the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the API is running.
    """
    app_logger.debug("Health check endpoint accessed")
    return {"status": "healthy"}