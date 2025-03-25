"""
Utility functions for the Invoice OCR API.
This module contains helper functions used across the application.
"""
import os
import re
from typing import List, Dict, Any

def ensure_dir_exists(directory: str) -> None:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory (str): Path to the directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def clean_text(text: str) -> str:
    """
    Clean OCR text by removing extra spaces, normalizing line breaks, etc.
    
    Args:
        text (str): Raw OCR text
        
    Returns:
        str: Cleaned text
    """
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Replace multiple line breaks with a single line break
    text = re.sub(r'\n+', '\n', text)
    
    # Strip whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    
    # Join the lines back together
    return '\n'.join(lines)

def validate_invoice_data(data: Dict[str, Any]) -> List[str]:
    """
    Validate extracted invoice data to ensure it has minimum required fields.
    
    Args:
        data (Dict[str, Any]): Extracted invoice data
        
    Returns:
        List[str]: List of validation errors, empty if validation passes
    """
    errors = []
    
    # Check for minimum required fields
    if not data.get('invoice_number'):
        errors.append("Invoice number not found")
    
    if not data.get('date'):
        errors.append("Invoice date not found")
    
    if not data.get('total_amount'):
        errors.append("Total amount not found")
    
    return errors