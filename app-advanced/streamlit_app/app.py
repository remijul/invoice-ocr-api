"""
Streamlit demo application for the Invoice OCR API.
This app provides a user interface to test the API functionality.
"""
import streamlit as st
import requests
import os
import json
from PIL import Image
import io
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Invoice OCR Demo",
    page_icon="📄",
    layout="wide"
)

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_USERNAME = os.getenv("API_USERNAME", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "password")

def get_auth_header():
    """
    Create the Basic Authentication header.
    
    Returns:
        dict: Authentication header
    """
    credentials = f"{API_USERNAME}:{API_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

def main():
    """Main function for the Streamlit app."""
    st.title("Invoice OCR Demo")
    st.write("Upload an invoice image (PDF, PNG, or JPEG) to extract information.")
    
    # Authentication status
    st.sidebar.title("API Authentication")
    if st.sidebar.checkbox("Use custom credentials"):
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if username and password:
            credentials = f"{username}:{password}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            auth_header = {"Authorization": f"Basic {encoded_credentials}"}
        else:
            auth_header = get_auth_header()
    else:
        auth_header = get_auth_header()
        st.sidebar.info(f"Using default credentials: {API_USERNAME}")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an invoice file",
        type=["pdf", "png", "jpg", "jpeg"]
    )
    
    if uploaded_file is not None:
        # Display the uploaded file
        st.subheader("Uploaded Invoice")
        
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        
        st.json(file_details)
        
        # Check if it's an image file
        if uploaded_file.type.startswith('image'):
            image = Image.open(uploaded_file)
            st.image(image, caption=uploaded_file.name, use_container_width=True)
        elif uploaded_file.type == 'application/pdf':
            st.write("PDF file uploaded (preview not available)")
        
        # Process button
        if st.button("Extract Information"):
            with st.spinner("Processing invoice..."):
                # Send to API
                result = process_invoice(uploaded_file, auth_header)
                
                # Display results
                st.subheader("Extracted Information")
                
                # Check for error
                if "error" in result:
                    st.error(result["error"])
                else:
                    # Create two columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Invoice Number:**", result.get("extracted_data", {}).get("invoice_number", "Not found"))
                        st.write("**Date:**", result.get("extracted_data", {}).get("date", "Not found"))
                        st.write("**Due Date:**", result.get("extracted_data", {}).get("due_date", "Not found"))
                        st.write("**Vendor:**", result.get("extracted_data", {}).get("vendor", "Not found"))
                        st.write("**Total Amount:**", result.get("extracted_data", {}).get("total_amount", "Not found"))
                    
                    with col2:
                        # Display raw JSON
                        st.write("**Raw JSON Response:**")
                        st.json(result)
                    
                    # Display raw text
                    st.subheader("Raw Extracted Text")
                    st.text(result.get("extracted_data", {}).get("raw_text", "No text extracted"))

def process_invoice(file, auth_header):
    """
    Send the file to the API for processing.
    
    Args:
        file: Uploaded file object
        auth_header: Authentication header
        
    Returns:
        dict: API response or error
    """
    # Create a files dictionary for the request
    files = {"file": (file.name, file.getvalue(), file.type)}
    
    try:
        # Make POST request to the API
        response = requests.post(
            f"{API_URL}/extract/",
            files=files,
            headers=auth_header
        )
        
        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Authentication failed. Please check your credentials."}
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    
    except Exception as e:
        return {"error": f"Error connecting to API: {str(e)}"}

if __name__ == "__main__":
    main()