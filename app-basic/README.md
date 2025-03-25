# Invoice OCR API

A simple API for extracting information from invoice images and PDFs using Optical Character Recognition (OCR).

## Features

- Upload invoice files (PDF, PNG, JPEG) and receive extracted data as JSON
- Simple OCR processing using PyTesseract
- Interactive demo interface using Streamlit
- Comprehensive documentation for beginners

## Project Structure

```
invoice-ocr-api/
├── app/                   # API application
├── streamlit_app/         # Streamlit demo interface
├── tests/                 # Tests
├── docs/                  # Documentation
└── requirements.txt       # Project dependencies
```

## Quick Start

1. **Setup Environment**

```bash
# Clone the repository
git clone https://github.com/yourusername/invoice-ocr-api.git
cd invoice-ocr-api

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR on your system if not already installed
# Ubuntu: sudo apt install tesseract-ocr
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# MacOS: brew install tesseract
```

2. **Run the API**

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to see the API documentation.

3. **Run the Streamlit Demo**

```bash
cd streamlit_app
streamlit run app.py
```

Visit `http://localhost:8501` to see the interactive demo.

## Documentation

See the `docs/` directory for detailed documentation:

- [Setup Guide](docs/setup.md) - Detailed setup instructions
- [API Usage Guide](docs/api_usage.md) - How to use the API

## Technologies

- [FastAPI](https://fastapi.tiangolo.com/) - API framework
- [PyTesseract](https://github.com/madmaze/pytesseract) - OCR engine wrapper
- [Streamlit](https://streamlit.io/) - Demo interface

## License

MIT