"""
Tests for the authentication functionality.
"""
import base64
import pytest
from fastapi.testclient import TestClient

def test_extract_endpoint_without_auth(test_client):
    """Test that authentication is required for the extract endpoint."""
    response = test_client.post("/extract/")
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers
    assert response.headers["WWW-Authenticate"] == "Basic"

def test_extract_endpoint_with_invalid_auth(test_client):
    """Test that invalid credentials are rejected."""
    # Create invalid credentials
    credentials = "wrong:credentials"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_credentials}"}
    
    # Make request with invalid credentials
    response = test_client.post("/extract/", headers=headers)
    
    # Check response
    assert response.status_code == 401
    assert "detail" in response.json()
    assert "Invalid credentials" in response.json()["detail"]

def test_extract_endpoint_with_valid_auth(test_client, auth_headers):
    """Test that valid credentials are accepted."""
    # No file attached, so we should get a 422 error (not a 401)
    # This confirms that authentication succeeded but the request is invalid for other reasons
    response = test_client.post("/extract/", headers=auth_headers)
    
    # Should fail with 422 (missing file) but not 401 (auth error)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_public_endpoint_without_auth(test_client):
    """Test that public endpoints work without authentication."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_endpoint_without_auth(test_client):
    """Test that health endpoint works without authentication."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"