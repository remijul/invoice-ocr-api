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

# Set page configuration
st.set_page_config(
    page_title="Invoice OCR Demo",
    page_icon="📄",
    layout="wide"
)

# Constants
API_URL = "http://localhost:8000"

def main():
    """Main function for the Streamlit app."""
    st.title("Invoice OCR Demo")
    st.write("Upload an invoice image (PDF, PNG, or JPEG) to extract information.")
    
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
            st.image(image, caption=uploaded_file.name, use_container_width=True) #use_column_width=True)
        elif uploaded_file.type == 'application/pdf':
            st.write("PDF file uploaded (preview not available)")
        
        # Process button
        if st.button("Extract Information"):
            with st.spinner("Processing invoice..."):
                # Send to API
                result = process_invoice(uploaded_file)
                
                # Display results
                st.subheader("Extracted Information")
                
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

def process_invoice(file):
    """
    Send the file to the API for processing.
    
    Args:
        file: Uploaded file object
        
    Returns:
        dict: API response
    """
    # Create a files dictionary for the request
    files = {"file": (file.name, file.getvalue(), file.type)}
    
    try:
        # Make POST request to the API
        response = requests.post(f"{API_URL}/extract/", files=files)
        
        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return {}
    
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return {}

if __name__ == "__main__":
    main()