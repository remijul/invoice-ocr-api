"""
Pydantic models for request and response data.
These models define the expected structure of the API's input and output.
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

class OCRResponse(BaseModel):
    """
    Response model for the OCR extraction endpoint.
    
    Attributes:
        filename (str): Name of the processed file
        extracted_data (Dict[str, Any]): Extracted data from the invoice
    """
    filename: str
    extracted_data: Dict[str, Any]

class InvoiceData(BaseModel):
    """
    Model representing structured invoice data.
    This is what we aim to extract from the raw OCR text.
    
    Attributes:
        invoice_number (Optional[str]): Invoice identification number
        date (Optional[str]): Invoice date
        due_date (Optional[str]): Payment due date
        vendor (Optional[str]): Vendor/supplier name
        total_amount (Optional[float]): Total invoice amount
        items (List[Dict[str, Any]]): List of invoice line items
        additional_info (Dict[str, Any]): Any additional information extracted
    """
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    due_date: Optional[str] = None
    vendor: Optional[str] = None
    total_amount: Optional[float] = None
    items: List[Dict[str, Any]] = []
    additional_info: Dict[str, Any] = {}