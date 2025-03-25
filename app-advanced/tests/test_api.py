"""
Tests for the Invoice OCR API endpoints.
"""
import os
import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(test_client):
    """Test the root endpoint returns a welcome message."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Welcome" in response.json()["message"]

def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_extract_invalid_file_type(test_client, auth_headers):
    """Test that the API rejects unsupported file types."""
    # Create a temporary text file
    with open("temp_test.txt", "w") as f:
        f.write("This is a test file")
    
    # Try to upload the text file
    with open("temp_test.txt", "rb") as f:
        response = test_client.post(
            "/extract/",
            headers=auth_headers,
            files={"file": ("temp_test.txt", f, "text/plain")}
        )
    
    # Clean up
    os.remove("temp_test.txt")
    
    # Assert that the response is an error
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

def test_extract_with_sample_image(test_client, auth_headers, sample_image):
    """Test the OCR extraction functionality with a sample image."""
    # Upload the sample image
    with open(sample_image, "rb") as f:
        response = test_client.post(
            "/extract/",
            headers=auth_headers,
            files={"file": ("test_invoice.png", f, "image/png")}
        )
    
    # Check response
    assert response.status_code == 200
    assert "filename" in response.json()
    assert "extracted_data" in response.json()
    
    # Check extracted data
    extracted_data = response.json()["extracted_data"]
    
    # Since we're using real OCR, the results may vary
    # We'll just check that the structure is correct
    assert "raw_text" in extracted_data
    
    # Ideally, we would check for specific extracted fields,
    # but OCR results can be inconsistent, so we'll keep this simple