"""
Tests for the Invoice OCR API endpoints.
"""
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Initialize test client
client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Welcome" in response.json()["message"]

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_extract_invalid_file_type():
    """Test that the API rejects unsupported file types."""
    # Create a temporary text file
    with open("temp_test.txt", "w") as f:
        f.write("This is a test file")
    
    # Try to upload the text file
    with open("temp_test.txt", "rb") as f:
        response = client.post(
            "/extract/",
            files={"file": ("temp_test.txt", f, "text/plain")}
        )
    
    # Clean up
    os.remove("temp_test.txt")
    
    # Assert that the response is an error
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]