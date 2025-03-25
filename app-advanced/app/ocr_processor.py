"""
OCR processor module for extracting data from invoices.
This module contains the logic for processing different file types and extracting information.
"""
import os
import re
import pytesseract
from PIL import Image
from typing import Dict, Any, List
#import pdf2image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set Tesseract executable path from environment variable
tesseract_cmd_path = os.getenv("TESSERACT_CMD_PATH")
if tesseract_cmd_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
    
# Configure path for Tesseract
#pytesseract.pytesseract.tesseract_cmd = dotenv_values(".env")['PATH_TESSERACT']
#PATH_TESSERACT = r'C:\Program Files\Tesseract-OCR\tesseract'

def process_invoice(file_path: str) -> Dict[str, Any]:
    """
    Process an invoice file and extract data using OCR.
    
    Args:
        file_path (str): Path to the invoice file
        
    Returns:
        Dict[str, Any]: Extracted data from the invoice
    """
    # Get file extension
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Convert file to image(s) based on file type
    if file_ext == '.pdf':
        None
        # Convert PDF to image
        #images = pdf2image.convert_from_path(file_path)
        # For simplicity, we'll just process the first page
        #image = images[0]
    else:
        # For image files (PNG, JPEG)
        image = Image.open(file_path)
    
    # Perform OCR on the image
    text = pytesseract.image_to_string(image, config='--psm 4')
    
    # Extract structured data from the OCR text
    extracted_data = extract_invoice_data(text)
    
    return extracted_data

def extract_invoice_data(text: str) -> Dict[str, Any]:
    """
    Extract structured data from OCR text.
    
    Args:
        text (str): OCR text extracted from the invoice
        
    Returns:
        Dict[str, Any]: Structured invoice data
    """
    # Initialize result dictionary
    result = {
        "invoice_number": extract_invoice_number(text),
        "date": extract_date(text),
        "due_date": extract_due_date(text),
        "vendor": extract_vendor(text),
        "total_amount": extract_total_amount(text),
        "items": extract_items(text),
        "raw_text": text,  # Include raw text for reference
    }
    
    return result

def extract_invoice_number(text: str) -> str:
    """
    Extract invoice number from OCR text.
    
    Args:
        text (str): OCR text
        
    Returns:
        str: Extracted invoice number or None if not found
    """
    # Common patterns for invoice numbers
    patterns = [
        r'(?i)invoice\s*(?:#|number|num|no)?[:\s]*([A-Z0-9\-]+)',
        r'(?i)inv\s*(?:#|number|num|no)?[:\s]*([A-Z0-9\-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return None

def extract_date(text: str) -> str:
    """
    Extract invoice date from OCR text.
    
    Args:
        text (str): OCR text
        
    Returns:
        str: Extracted date or None if not found
    """
    # Common date patterns (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD)
    patterns = [
        r'(?i)(?:invoice|bill|statement)\s*date\s*(?::|is|of)?[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?i)date\s*(?::|of|is)?[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?i)date\s*(?::|of|is)?[:\s]*(\d{2,4}[/-]\d{1,2}[/-]\d{1,2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return None

def extract_due_date(text: str) -> str:
    """
    Extract due date from OCR text.
    
    Args:
        text (str): OCR text
        
    Returns:
        str: Extracted due date or None if not found
    """
    # Common due date patterns
    patterns = [
        r'(?i)(?:due|payment)\s*date\s*(?::|is)?[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?i)due\s*(?::|by|on)?[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?i)(?:payment|pay\s+by)\s*(?::|due|on)?[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return None

def extract_vendor(text: str) -> str:
    """
    Extract vendor name from OCR text.
    
    Args:
        text (str): OCR text
        
    Returns:
        str: Extracted vendor name or None if not found
    """
    # Look for "From:" or company labels
    patterns = [
        r'(?i)from\s*:?\s*([A-Za-z0-9\s,\.]+(?:Inc|LLC|Ltd|Corp|Corporation|Company|Co)?)',
        r'(?i)(?:vendor|supplier|biller)\s*:?\s*([A-Za-z0-9\s,\.]+(?:Inc|LLC|Ltd|Corp|Corporation|Company|Co)?)',
        r'(?i)([A-Za-z0-9\s,\.]+(?:Inc|LLC|Ltd|Corp|Corporation|Company|Co))',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            # Clean up the result
            vendor = match.group(1).strip()
            # Limit to a reasonable length
            if len(vendor) > 50:
                vendor = vendor[:50]
            return vendor
    
    # If nothing found, return first line (often contains company name)
    lines = text.split('\n')
    if lines and lines[0].strip():
        return lines[0].strip()[:50]
    
    return None

def extract_total_amount(text: str) -> float:
    """
    Extract total amount from OCR text.
    
    Args:
        text (str): OCR text
        
    Returns:
        float: Extracted total amount or None if not found
    """
    # Common patterns for total amount
    patterns = [
        r'(?i)total\s*(?:amount|payment|due)?[:\s]*[\$£€]?([0-9,]+\.[0-9]{2})',
        r'(?i)amount\s*(?:due|total)?[:\s]*[\$£€]?([0-9,]+\.[0-9]{2})',
        r'(?i)(?:sub)?total\s*(?:due)?[:\s]*[\$£€]?([0-9,]+\.[0-9]{2})',
        r'(?i)balance\s*(?:due)?[:\s]*[\$£€]?([0-9,]+\.[0-9]{2})',
        r'(?i)(?:please\s+)?pay\s*(?:this\s+amount)?[:\s]*[\$£€]?([0-9,]+\.[0-9]{2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            # Remove commas and convert to float
            amount_str = match.group(1).replace(',', '')
            try:
                return float(amount_str)
            except ValueError:
                continue
    
    return None

def extract_items(text: str) -> List[Dict[str, Any]]:
    """
    Extract line items from OCR text.
    
    Args:
        text (str): OCR text
        
    Returns:
        List[Dict[str, Any]]: List of extracted items
    """
    # This is a very simplified approach to item extraction
    # In a real application, you would need a more sophisticated method
    # that considers table structure, line breaks, etc.
    
    # For this beginner example, we'll return an empty list
    return []