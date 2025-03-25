# Docker Guide

This guide explains how to use Docker with the Invoice OCR API.

## Overview

Docker allows you to package the application and all its dependencies into a standardized unit called a container. This makes it easy to deploy the API in different environments without worrying about dependencies or configuration.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine

## Project Docker Files

The project includes two Docker-related files:

1. **Dockerfile**: This defines how to build the Docker image for the API.
2. **docker-compose.yml**: This defines how to run multiple services (API and Streamlit) together.

## Building and Running with Docker

### Option 1: Using Docker Directly

To build and run the API using Docker:

```bash
# Build the Docker image
docker build -t invoice-ocr-api .

# Run the container
docker run -p 8000:8000 \
  -e API_USERNAME=admin \
  -e API_PASSWORD=password \
  invoice-ocr-api
```

### Option 2: Using Docker Compose (Recommended)

Docker Compose makes it easy to run both the API and Streamlit demo together:

```bash
# Start all services
docker-compose up

# Run in background
docker-compose up -d

# Stop all services
docker-compose down
```

## Accessing the Services

- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Streamlit Demo: http://localhost:8501

## Understanding the Dockerfile

Let's break down the key components of the Dockerfile:

```dockerfile
# Use Python 3.9 as the base image
FROM python:3.9-slim

# Install Tesseract OCR and other dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV TESSERACT_CMD_PATH=/usr/bin/tesseract
ENV UPLOAD_DIR=uploaded_files

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

This Dockerfile:
1. Starts with a Python 3.9 base image
2. Installs Tesseract OCR and Poppler (for PDF processing)
3. Installs Python dependencies
4. Copies the application code
5. Sets environment variables
6. Exposes port 8000
7. Defines the command to start the API

## Understanding docker-compose.yml

The docker-compose.yml file defines two services:

1. **api**: The FastAPI application
2. **streamlit**: The Streamlit demo application

It also sets up volumes for logs and uploaded files, and configures environment variables.

## Customizing the Configuration

You can customize the Docker setup by modifying:

1. **Environment Variables**: Edit the `environment` section in docker-compose.yml
2. **Ports**: Change the port mappings in the `ports` section
3. **Volumes**: Adjust the paths in the `volumes` section

## Common Docker Commands

```bash
# View running containers
docker ps

# View logs
docker logs container_id

# Stop a container
docker stop container_id

# Remove all stopped containers
docker container prune

# View Docker images
docker images

# Remove an image
docker rmi image_name
```

## CI/CD Integration

The Dockerfile and docker-compose.yml files are designed to work with the CI/CD pipeline. The GitHub Actions workflow:

1. Builds the Docker image
2. Pushes it to GitHub Container Registry
3. Makes it available for deployment

This enables continuous delivery of the application.