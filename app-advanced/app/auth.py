"""
Authentication module for the Invoice OCR API.
This module handles user authentication using FastAPI's security features.
"""
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

# Load environment variables
load_dotenv()

# Create security scheme
security = HTTPBasic()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get credentials from environment variables or use defaults
# In a real application, these would come from a database
API_USERNAME = os.getenv("API_USERNAME", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "password")

# Hash the password (in a real app, you'd store the hashed password)
API_PASSWORD_HASH = pwd_context.hash(API_PASSWORD)

def verify_password(plain_password, hashed_password):
    """
    Verify a password against a hash.
    
    Args:
        plain_password (str): Plain text password
        hashed_password (str): Hashed password
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authenticate a user using HTTP Basic Authentication.
    
    Args:
        credentials (HTTPBasicCredentials): The credentials provided in the request
        
    Returns:
        str: The username if authentication is successful
        
    Raises:
        HTTPException: If authentication fails
    """
    # Check if the username matches
    is_username_correct = credentials.username == API_USERNAME
    
    # Check if the password matches
    is_password_correct = False
    if is_username_correct:
        is_password_correct = verify_password(credentials.password, API_PASSWORD_HASH)
    
    # If either check fails, raise an exception
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username