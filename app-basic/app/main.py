"""
Main entry point for the Invoice OCR API.
This module defines the FastAPI application and its endpoints.
"""
import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from .models import OCRResponse
from .ocr_processor import process_invoice

# Create upload directory if it doesn't exist
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize FastAPI application
app = FastAPI(
    title="Invoice OCR API",
    description="API for extracting data from invoice images and PDFs using OCR",
    version="0.1.0"
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
    return {"message": "Welcome to Invoice OCR API"}

@app.post("/extract/", response_model=OCRResponse)
async def extract_invoice_data(file: UploadFile = File(...)):
    """
    Extract data from an uploaded invoice file.
    
    Parameters:
    - file: The invoice file (PDF, PNG, or JPEG)
    
    Returns:
    - OCRResponse: Extracted invoice data
    """
    # Validate file type
    valid_extensions = [".png", ".jpg", ".jpeg"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in valid_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Supported types: {', '.join(valid_extensions)}"
        )
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Process the invoice with OCR
        result = process_invoice(file_path)
        
        # Return the extracted data
        return OCRResponse(
            filename=file.filename,
            extracted_data=result
        )
    except Exception as e:
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
    return {"status": "healthy"}