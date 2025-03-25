# Invoice OCR API Tutorial

This step-by-step tutorial explains how the Invoice OCR API works and how to use it. It's designed for beginners who want to learn about building APIs with FastAPI and implementing OCR functionality.

## What You'll Learn

- Setting up a FastAPI application
- Implementing OCR with PyTesseract
- Processing different file types (PDF, PNG, JPEG)
- Extracting structured data from raw text
- Creating a simple web interface with Streamlit

## Project Overview

This project creates an API that can extract information from invoice images or PDFs using Optical Character Recognition (OCR). The API accepts file uploads, processes them using PyTesseract, and returns structured data in JSON format.

## Understanding the Components

### 1. FastAPI Application (`app/main.py`)

The main application file sets up the FastAPI application and defines the API endpoints:

```python
# Initialize FastAPI application
app = FastAPI(
    title="Invoice OCR API",
    description="API for extracting data from invoice images and PDFs using OCR",
    version="0.1.0"
)

@app.post("/extract/", response_model=OCRResponse)
async def extract_invoice_data(file: UploadFile = File(...)):
    # Code to process the uploaded file
```

Key points to understand:

- `FastAPI()` creates a new web application
- `@app.post("/extract/")` defines a POST endpoint at the `/extract/` URL
- `response_model=OCRResponse` specifies the structure of the response
- `file: UploadFile = File(...)` indicates that this endpoint accepts file uploads

### 2. Data Models (`app/models.py`)

This file defines the structure of the data using Pydantic models:

```python
class OCRResponse(BaseModel):
    filename: str
    extracted_data: Dict[str, Any]

class InvoiceData(BaseModel):
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    # Other fields...
```

These models:
- Define the expected structure of the API's input and output
- Provide automatic validation
- Generate API documentation

### 3. OCR Processor (`app/ocr_processor.py`)

This file contains the logic for processing files and extracting information:

```python
def process_invoice(file_path: str) -> Dict[str, Any]:
    # Get file extension
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Convert file to image(s) based on file type
    if file_ext == '.pdf':
        images = pdf2image.convert_from_path(file_path)
        image = images[0]
    else:
        image = Image.open(file_path)
    
    # Perform OCR on the image
    text = pytesseract.image_to_string(image)
    
    # Extract structured data from the OCR text
    extracted_data = extract_invoice_data(text)
    
    return extracted_data
```

The key steps are:
1. Determine the file type
2. Convert the file to an image (if it's a PDF)
3. Use PyTesseract to extract text from the image
4. Process the text to extract structured information

### 4. Streamlit Demo (`streamlit_app/app.py`)

The Streamlit app provides a user-friendly interface to test the API:

```python
def main():
    st.title("Invoice OCR Demo")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an invoice file",
        type=["pdf", "png", "jpg", "jpeg"]
    )
    
    if uploaded_file is not None:
        # Display the uploaded file
        # ...
        
        # Process button
        if st.button("Extract Information"):
            # Send to API and display results
            # ...
```

This app:
1. Provides a file upload widget
2. Displays a preview of the uploaded file
3. Sends the file to the API for processing
4. Displays the results in a user-friendly format

## Step-by-Step Implementation Guide

### Step 1: Setting Up the Project

First, create the project structure and install the required dependencies:

```bash
# Create project directory
mkdir invoice-ocr-api
cd invoice-ocr-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-multipart pytesseract Pillow pdf2image streamlit
```

### Step 2: Creating the FastAPI Application

Create the main application file:

```python
# app/main.py
from fastapi import FastAPI, File, UploadFile

app = FastAPI(
    title="Invoice OCR API",
    description="API for extracting data from invoice images and PDFs using OCR",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Invoice OCR API"}

@app.post("/extract/")
async def extract_invoice_data(file: UploadFile = File(...)):
    # We'll implement this later
    return {"filename": file.filename}
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000/docs to see the API documentation.

### Step 3: Implementing OCR Processing

Now, let's implement the OCR processing logic:

```python
# app/ocr_processor.py
import pytesseract
from PIL import Image
import pdf2image

def process_invoice(file_path):
    # Determine file type
    if file_path.endswith('.pdf'):
        # Convert PDF to image
        images = pdf2image.convert_from_path(file_path)
        image = images[0]
    else:
        # Load image directly
        image = Image.open(file_path)
    
    # Perform OCR
    text = pytesseract.image_to_string(image)
    
    # Return basic result
    return {"raw_text": text}
```

Update the API endpoint to use this function:

```python
# app/main.py
from .ocr_processor import process_invoice

@app.post("/extract/")
async def extract_invoice_data(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = f"uploaded_files/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process the file
    result = process_invoice(file_path)
    
    # Clean up
    os.remove(file_path)
    
    return {"filename": file.filename, "extracted_data": result}
```

### Step 4: Extracting Structured Data

Now, let's add functions to extract structured data from the raw text:

```python
# app/ocr_processor.py
import re

def extract_invoice_data(text):
    return {
        "invoice_number": extract_invoice_number(text),
        "date": extract_date(text),
        "total_amount": extract_total_amount(text),
        "raw_text": text
    }

def extract_invoice_number(text):
    # Use regular expressions to find the invoice number
    pattern = r'(?i)invoice\s*(?:#|number|num|no)?[:\s]*([A-Z0-9\-]+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return None

def extract_date(text):
    # Use regular expressions to find the date
    pattern = r'(?i)date\s*(?::|of|is)?[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return None

def extract_total_amount(text):
    # Use regular expressions to find the total amount
    pattern = r'(?i)total\s*(?:amount|payment|due)?[:\s]*[\$£€]?([0-9,]+\.[0-9]{2})'
    match = re.search(pattern, text)
    if match:
        amount_str = match.group(1).replace(',', '')
        try:
            return float(amount_str)
        except ValueError:
            pass
    return None
```

### Step 5: Creating a Streamlit Demo

Let's create a simple Streamlit app to test our API:

```python
# streamlit_app/app.py
import streamlit as st
import requests
from PIL import Image

st.title("Invoice OCR Demo")

uploaded_file = st.file_uploader("Choose an invoice file", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded file
    if uploaded_file.type.startswith('image'):
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name)
    
    # Process button
    if st.button("Extract Information"):
        # Send to API
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post("http://localhost:8000/extract/", files=files)
        
        if response.status_code == 200:
            result = response.json()
            
            # Display extracted information
            st.subheader("Extracted Information")
            st.write("**Invoice Number:**", result["extracted_data"].get("invoice_number", "Not found"))
            st.write("**Date:**", result["extracted_data"].get("date", "Not found"))
            st.write("**Total Amount:**", result["extracted_data"].get("total_amount", "Not found"))
            
            # Display raw text
            st.subheader("Raw Extracted Text")
            st.text(result["extracted_data"].get("raw_text", "No text extracted"))
```

Run the Streamlit app:

```bash
cd streamlit_app
streamlit run app.py
```

Visit http://localhost:8501 to use the demo app.

## Enhancing the API

Here are some ways you can enhance the API:

1. **Improve text extraction**:
   - Add more regular expressions to extract additional information
   - Implement more sophisticated text parsing
   - Use machine learning for entity extraction

2. **Add validation and error handling**:
   - Validate the extracted data
   - Implement more robust error handling
   - Add logging

3. **Add authentication and authorization**:
   - Implement API keys
   - Add user authentication
   - Set up role-based access control

4. **Improve performance**:
   - Implement caching
   - Optimize the OCR process
   - Add background processing for large files

## Testing

You can test the API using various methods:

1. **Using the Swagger UI**:
   - Go to http://127.0.0.1:8000/docs
   - Click on the `/extract/` endpoint
   - Click "Try it out"
   - Upload a file and execute the request

2. **Using cURL**:
   ```bash
   curl -X POST "http://localhost:8000/extract/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@/path/to/your/invoice.pdf"
   ```

3. **Using the Streamlit demo app**:
   - Go to http://localhost:8501
   - Upload a file
   - Click "Extract Information"

## Conclusion

You've now built a simple Invoice OCR API that can extract information from invoice images and PDFs. This project demonstrates how to use FastAPI, PyTesseract, and Streamlit to create a full-stack application.

Remember that OCR is not perfect, and the accuracy of the extracted information depends on the quality of the input images. You may need to adjust the regular expressions and text processing logic to handle different invoice formats.