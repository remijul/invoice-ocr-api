"""
Main entry point for the Invoice OCR API.
This module defines the FastAPI application and its endpoints.
"""
import os
import shutil
import time
import json
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Request, Form, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER
from typing import Optional
import base64
from dotenv import load_dotenv

from .models import OCRResponse
from .ocr_processor import process_invoice
from .auth import authenticate_user, API_USERNAME, verify_password, API_PASSWORD_HASH
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

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

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
async def root(request: Request):
    """
    Root endpoint - returns a welcome message.
    """
    app_logger.info("Root endpoint accessed")
    
    # Check if the request is from a browser
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        # If it's a browser request, redirect to the web interface
        return templates.TemplateResponse("index.html", {"request": request, "user": None})
    
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


# From here, implementation of Jinja templates -------------------------------------------------------------------------
# Web Interface Routes

@app.get("/web/upload", response_class=HTMLResponse)
async def web_upload_form(request: Request, auth: Optional[str] = Cookie(None)):
    """
    Show the upload form.
    """
    app_logger.info("Web upload form accessed")
    
    # Verify user authentication
    user = verify_web_auth(auth)
    if not user:
        return RedirectResponse(url="/web/login", status_code=HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse("upload.html", {"request": request, "user": user})

@app.post("/web/process", response_class=HTMLResponse)
async def web_process_invoice(request: Request, file: UploadFile = File(...), auth: Optional[str] = Cookie(None)):
    """
    Process the uploaded invoice and show results.
    """
    app_logger.info(f"Web process request for file: {file.filename}")
    
    # Verify user authentication
    user = verify_web_auth(auth)
    if not user:
        return RedirectResponse(url="/web/login", status_code=HTTP_303_SEE_OTHER)
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Get allowed extensions from environment variable or use defaults
        allowed_extensions = os.getenv("ALLOWED_EXTENSIONS", "pdf,png,jpg,jpeg")
        valid_extensions = ["." + ext.strip() for ext in allowed_extensions.split(",")]
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in valid_extensions:
            error_msg = f"Invalid file type. Supported types: {', '.join(valid_extensions)}"
            app_logger.warning(f"Invalid file type attempt: {file_ext} for file {file.filename}")
            return templates.TemplateResponse(
                "error.html", 
                {"request": request, "error": error_msg, "user": user}
            )
        
        # Process the invoice with OCR
        result = process_invoice(file_path)
        
        # Create the response model
        response_data = OCRResponse(
            filename=file.filename,
            extracted_data=result
        )
        
        # Convert to JSON for display
        result_json = json.dumps(response_data.dict(), indent=4)
        
        # Return the results page
        return templates.TemplateResponse(
            "results.html", 
            {
                "request": request, 
                "result": response_data, 
                "result_json": result_json,
                "user": user
            }
        )
    except Exception as e:
        app_logger.error(f"Error processing file {file.filename}: {str(e)}")
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "error": str(e), "user": user}
        )
    finally:
        # Clean up - remove the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/web/login", response_class=HTMLResponse)
async def web_login_form(request: Request, auth: Optional[str] = Cookie(None)):
    """
    Show the login form.
    """
    app_logger.info("Web login form accessed")
    
    # Check if already logged in
    user = verify_web_auth(auth)
    if user:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse("login.html", {"request": request, "user": None})

@app.post("/web/login", response_class=HTMLResponse)
async def web_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    Process login form.
    """
    app_logger.info(f"Login attempt for user: {username}")
    
    # Check credentials
    is_username_correct = username == API_USERNAME
    is_password_correct = False
    if is_username_correct:
        is_password_correct = verify_password(password, API_PASSWORD_HASH)
    
    if not (is_username_correct and is_password_correct):
        app_logger.warning(f"Failed login attempt for user: {username}")
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Invalid credentials", "user": None}
        )
    
    # Create authentication cookie
    auth_value = base64.b64encode(f"{username}:{password}".encode()).decode()
    
    # Redirect to home page with authentication cookie
    response = RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="auth", value=auth_value)
    
    app_logger.info(f"Successful login for user: {username}")
    return response

@app.get("/web/logout")
async def web_logout():
    """
    Logout the user.
    """
    app_logger.info("User logged out")
    
    # Redirect to home page and clear authentication cookie
    response = RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    response.delete_cookie(key="auth")
    
    return response

def verify_web_auth(auth_cookie: Optional[str]) -> Optional[str]:
    """
    Verify the web authentication cookie.
    
    Args:
        auth_cookie: The authentication cookie value
        
    Returns:
        str: The username if authentication is successful, None otherwise
    """
    if not auth_cookie:
        return None
    
    try:
        # Decode the cookie
        decoded_auth = base64.b64decode(auth_cookie.encode()).decode()
        username, password = decoded_auth.split(":", 1)
        
        # Check if the username matches
        is_username_correct = username == API_USERNAME
        
        # Check if the password matches
        is_password_correct = False
        if is_username_correct:
            is_password_correct = verify_password(password, API_PASSWORD_HASH)
        
        # If both checks pass, return the username
        if is_username_correct and is_password_correct:
            return username
    except Exception:
        pass
    
    return None