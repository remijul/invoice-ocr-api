# API Usage Guide

This guide explains how to use the Invoice OCR API.

## API Endpoints

The API has the following endpoints:

1. `GET /` - Root endpoint with a welcome message
2. `POST /extract/` - Extract data from an invoice file
3. `GET /health` - Health check endpoint

## Extract Data from an Invoice

### Endpoint: POST /extract/

This is the main endpoint for extracting data from invoice files.

#### Request

- Method: POST
- Content-Type: multipart/form-data
- Body parameter: `file` (The invoice file to process, must be PDF, PNG, or JPEG)

#### Response

- Content-Type: application/json
- Body: JSON object with extracted invoice data

#### Example using cURL

```bash
curl -X POST "http://localhost:8000/extract/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/invoice.pdf"
```

#### Example using Python requests

```python
import requests

url = "http://localhost:8000/extract/"
file_path = "/path/to/your/invoice.pdf"

with open(file_path, "rb") as file:
    response = requests.post(
        url,
        files={"file": file}
    )

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### Response Format

The API returns a JSON object with the following structure:

```json
{
  "filename": "invoice.pdf",
  "extracted_data": {
    "invoice_number": "INV-12345",
    "date": "01/15/2023",
    "due_date": "02/15/2023",
    "vendor": "Example Company Inc",
    "total_amount": 123.45,
    "items": [],
    "raw_text": "The full OCR text extracted from the document..."
  }
}
```

### Response Fields

- `filename`: The name of the processed file
- `extracted_data`: An object containing the extracted information:
  - `invoice_number`: The invoice identification number
  - `date`: The invoice date
  - `due_date`: The payment due date
  - `vendor`: The vendor/supplier name
  - `total_amount`: The total invoice amount
  - `items`: List of line items (empty in the current implementation)
  - `raw_text`: The raw text extracted by OCR

### Error Responses

The API may return the following error responses:

- `400 Bad Request`: If the uploaded file is not a supported type (PDF, PNG, JPEG)
- `500 Internal Server Error`: If there's an error processing the invoice

## API Documentation (Swagger UI)

For interactive API documentation, visit:

```
http://localhost:8000/docs
```

This provides a web interface to:
- View all available endpoints
- Test the API directly from your browser
- See the request and response schemas