"""
Configuration and fixtures for pytest.
"""
import os
import pytest
import base64
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def test_client():
    """
    Create a test client for the FastAPI application.
    
    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(app)

@pytest.fixture
def auth_headers():
    """
    Create authentication headers for testing protected endpoints.
    
    Returns:
        dict: Headers with Basic Authentication
    """
    # Get credentials from environment variables or use defaults for testing
    username = os.getenv("API_USERNAME", "admin")
    password = os.getenv("API_PASSWORD", "password")
    
    # Create Basic Auth header
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    return {"Authorization": f"Basic {encoded_credentials}"}

@pytest.fixture
def sample_image():
    """
    Create a simple test image for OCR testing.
    
    Returns:
        str: Path to the test image
    """
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a directory for test files if it doesn't exist
    os.makedirs("tests/test_files", exist_ok=True)
    
    # Path for the test image
    image_path = "tests/test_files/test_invoice.png"
    
    # Create a simple image with text for testing OCR
    img = Image.new('RGB', (500, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, or use default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw invoice-like text
    draw.text((50, 50), "INVOICE #12345", fill=(0, 0, 0), font=font)
    draw.text((50, 80), "Date: 01/01/2023", fill=(0, 0, 0), font=font)
    draw.text((50, 110), "Due Date: 01/31/2023", fill=(0, 0, 0), font=font)
    draw.text((50, 140), "Amount: $500.00", fill=(0, 0, 0), font=font)
    draw.text((50, 170), "From: Test Company Inc.", fill=(0, 0, 0), font=font)
    
    # Save the image
    img.save(image_path)
    
    yield image_path
    
    # Clean up
    if os.path.exists(image_path):
        os.remove(image_path)