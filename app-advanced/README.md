# Invoice OCR API

A simple API for extracting information from invoice images and PDFs using Optical Character Recognition (OCR).

## Features

- Upload invoice files (PDF, PNG, JPEG) and receive extracted data as JSON
- Simple OCR processing using PyTesseract
- HTTP Basic Authentication for API security
- Comprehensive logging system
- Interactive demo interface using Streamlit
- Docker support for easy deployment
- CI/CD with GitHub Actions
- Comprehensive documentation for beginners

## Project Structure

```
invoice-ocr-api/
├── app/                   # API application
│   ├── auth.py            # Authentication logic
│   ├── logger.py          # Logging configuration
│   ├── main.py            # FastAPI application
│   ├── models.py          # Data models
│   └── ocr_processor.py   # OCR processing logic
├── streamlit_app/         # Streamlit demo interface
├── tests/                 # Tests
├── docs/                  # Documentation
├── .github/workflows/     # CI/CD configuration
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker configuration
└── requirements.txt       # Project dependencies
```

## Quick Start

### Option 1: Running Locally

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

# Create a .env file with your Tesseract path
echo "TESSERACT_CMD_PATH=/usr/bin/tesseract" > .env  # Adjust the path for your system

# Add authentication credentials to .env
echo "API_USERNAME=admin" >> .env
echo "API_PASSWORD=password" >> .env

# Run the API
uvicorn app.main:app --reload

# Run the Streamlit demo (in another terminal)
cd streamlit_app
streamlit run app.py
```

### Option 2: Using Docker Compose

```bash
# Clone the repository
git clone https://github.com/yourusername/invoice-ocr-api.git
cd invoice-ocr-api

# Start the services with Docker Compose
docker-compose up -d

# Access the API at http://localhost:8000
# Access the Streamlit demo at http://localhost:8501
```

## Using the API

The API endpoint `/extract/` requires authentication:

```bash
# Using curl
curl -X POST "http://localhost:8000/extract/" \
  -H "accept: application/json" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQ=" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/invoice.pdf"
```

See the documentation for more detailed examples and explanation.

## Documentation

See the `docs/` directory for detailed documentation:

- [Setup Guide](docs/setup.md) - Detailed setup instructions
- [API Usage Guide](docs/api_usage.md) - How to use the API
- [Environment Variables](docs/environment_variables.md) - Configure the application
- [Authentication Guide](docs/authentication.md) - How authentication works
- [Docker Guide](docs/docker.md) - Running with Docker
- [CI/CD Guide](docs/ci_cd.md) - Continuous Integration and Deployment
- [Tutorial](docs/tutorial.md) - Step-by-step tutorial

## Technologies

- [FastAPI](https://fastapi.tiangolo.com/) - API framework
- [PyTesseract](https://github.com/madmaze/pytesseract) - OCR engine wrapper
- [Streamlit](https://streamlit.io/) - Demo interface
- [Docker](https://www.docker.com/) - Containerization
- [GitHub Actions](https://github.com/features/actions) - CI/CD

## License

MIT