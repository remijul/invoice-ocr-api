"""
Logging module for the Invoice OCR API.
This module sets up logging for the application using Python's built-in logging module.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get logging configuration from environment variables
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")# "INFO")
LOG_FILE = os.getenv("LOG_FILE", "app.log")

# Convert string log level to logging constant
numeric_level = getattr(logging, LOG_LEVEL.upper(), None)
if not isinstance(numeric_level, int):
    numeric_level = logging.INFO

def setup_logger(name):
    """
    Set up a logger with both console and file handlers.
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    
    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10485760,  # 10 MB
        backupCount=5
    )
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set formatter for handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Create the main application logger
app_logger = setup_logger("invoice_ocr_api")