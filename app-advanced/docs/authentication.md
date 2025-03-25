# Authentication Guide

This guide explains how the authentication system works in the Invoice OCR API.

## Overview

The API uses HTTP Basic Authentication, a simple authentication mechanism where the client sends a username and password with each request. This is a simple and beginner-friendly approach that doesn't require a database.

## How It Works

1. When a client makes a request to a protected endpoint (like `/extract/`), they must include an `Authorization` header with their credentials.
2. The credentials are encoded in the format `username:password` and prefixed with `Basic `.
3. The API validates these credentials against the configured username and password.
4. If authentication succeeds, the request proceeds; otherwise, a 401 Unauthorized response is returned.

## Configuration

Authentication credentials are stored in the `.env` file:

```
API_USERNAME=admin
API_PASSWORD=password
```

In a production environment, you would use much stronger credentials!

## Making Authenticated Requests

### Using cURL

```bash
curl -X POST "http://localhost:8000/extract/" \
  -H "accept: application/json" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQ=" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/invoice.pdf"
```

The `Authorization` header contains the Base64-encoded string `admin:password` prefixed with `Basic `.

### Using Python requests

```python
import requests
import base64

# Set up authentication
username = "admin"
password = "password"
credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {"Authorization": f"Basic {encoded_credentials}"}

# Make the request
url = "http://localhost:8000/extract/"
file_path = "/path/to/your/invoice.pdf"

with open(file_path, "rb") as file:
    response = requests.post(
        url,
        headers=headers,
        files={"file": file}
    )

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

## Security Considerations

This authentication method has some limitations to be aware of:

1. **HTTP Basic Auth transmits credentials in an encoded (not encrypted) format.** Always use HTTPS in production to encrypt the data.
2. **Static credentials** are simpler for learning but not ideal for production. In a real-world application, you would use a database to store users and hashed passwords.
3. **No session management or token expiration.** This implementation requires credentials to be sent with every request.

These limitations are acceptable for educational purposes, but for a production application, you might want to consider more robust authentication methods like OAuth2 or JWT.

## Using the Streamlit Demo with Authentication

The Streamlit demo application has been updated to use authentication:

1. By default, it uses the credentials from the environment variables.
2. You can toggle "Use custom credentials" in the sidebar to enter different credentials.
3. If authentication fails, an error message will be displayed.

This allows you to test the authentication system easily without manually constructing HTTP headers.