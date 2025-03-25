# Setup Guide

This guide will walk you through setting up the Invoice OCR API on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed:

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **Tesseract OCR**
   - This is the OCR engine that PyTesseract uses.
   
   **Installation by operating system:**
   
   - **Windows:**
     - Download installer from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
     - Add the installation directory to your PATH environment variable
   
   - **macOS:**
     - Using Homebrew: `brew install tesseract`
   
   - **Linux (Ubuntu/Debian):**
     - `sudo apt update`
     - `sudo apt install tesseract-ocr`

   - Verify installation: `tesseract --version`

3. **Poppler** (for PDF processing)
   - Required by pdf2image to convert PDFs to images
   
   **Installation by operating system:**
   
   - **Windows:**
     - Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases/)
     - Add the bin folder to your PATH
   
   - **macOS:**
     - Using Homebrew: `brew install poppler`
   
   - **Linux (Ubuntu/Debian):**
     - `sudo apt install poppler-utils`

## Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/invoice-ocr-api.git
   cd invoice-ocr-api
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify setup**

   Run the following test to make sure Tesseract is properly set up:

   ```python
   import pytesseract
   print(pytesseract.get_tesseract_version())
   ```

   If this returns a version number, your setup is correct.

## Running the API

1. **Start the API server**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

2. **Access the API documentation**

   Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Running the Streamlit Demo

1. **Start the Streamlit app**

   ```bash
   cd streamlit_app
   streamlit run app.py
   ```

   The app will be available at [http://localhost:8501](http://localhost:8501)

## Troubleshooting

### Common Issues

1. **Tesseract not found error**

   If you see an error like `tesseract is not installed or it's not in your PATH`, you need to:
   
   - Make sure Tesseract is installed
   - Add Tesseract to your PATH environment variable
   - For Windows, you can also set the path explicitly in code:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```

2. **PDF processing issues**

   If you encounter issues processing PDFs:
   
   - Make sure you have the poppler-utils installed correctly
   - On Windows, you may need to set the path to poppler:
     ```python
     from pdf2image import convert_from_path
     images = convert_from_path(pdf_path, poppler_path=r'C:\path\to\poppler\bin')
     ```