# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install Tesseract OCR and other dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create upload directory
RUN mkdir -p uploaded_files

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TESSERACT_CMD_PATH=/usr/bin/tesseract
ENV UPLOAD_DIR=uploaded_files
ENV ALLOWED_EXTENSIONS=png,jpg,jpeg
ENV LOG_LEVEL=INFO
ENV LOG_FILE=/app/logs/app.log

# Create logs directory
RUN mkdir -p /app/logs

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]