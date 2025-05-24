import re
import os
from datetime import datetime

def sanitize_input(text: str) -> str:
    """
    Clean and sanitize user input to prevent malicious content or errors.
    Args:
        text (str): The user input.
    Returns:
        str: The sanitized text.
    """
    # Remove unwanted characters like special characters, multiple spaces, etc.
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Allow only alphanumeric and spaces
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = text.strip()  # Remove leading and trailing spaces
    return text


def validate_file(file_bytes: bytes, file_type: str) -> bool:
    """
    Validate the uploaded file to check if it's supported.
    Args:
        file_bytes (bytes): The file content in bytes.
        file_type (str): The type of the file (pdf, csv, image).
    Returns:
        bool: True if the file is valid, otherwise False.
    """
    # Check file type based on extension
    if file_type == 'pdf':
        return validate_pdf(file_bytes)
    elif file_type == 'csv':
        return validate_csv(file_bytes)
    elif file_type in ['jpg', 'jpeg', 'png']:
        return validate_image(file_bytes)
    else:
        return False


def validate_pdf(file_bytes: bytes) -> bool:
    """
    Validate the uploaded PDF file.
    Args:
        file_bytes (bytes): The byte content of the PDF file.
    Returns:
        bool: True if valid, else False.
    """
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_bytes)
        # Check if the PDF has pages (this is a simple validation)
        return len(reader.pages) > 0
    except Exception as e:
        print(f"Error validating PDF: {e}")
        return False


def validate_csv(file_bytes: bytes) -> bool:
    """
    Validate the uploaded CSV file.
    Args:
        file_bytes (bytes): The byte content of the CSV file.
    Returns:
        bool: True if valid, else False.
    """
    try:
        import pandas as pd
        df = pd.read_csv(file_bytes)
        # Check if the CSV contains rows and columns
        return not df.empty
    except Exception as e:
        print(f"Error validating CSV: {e}")
        return False


def validate_image(file_bytes: bytes) -> bool:
    """
    Validate the uploaded image file (JPG, PNG, JPEG).
    Args:
        file_bytes (bytes): The byte content of the image file.
    Returns:
        bool: True if valid, else False.
    """
    try:
        from PIL import Image
        image = Image.open(file_bytes)
        # Check if the image can be opened
        image.verify()
        return True
    except Exception as e:
        print(f"Error validating image: {e}")
        return False


def process_financial_data(data: str) -> str:
    """
    Process and extract meaningful financial data or analysis from the input text.
    Args:
        data (str): The financial data or user input.
    Returns:
        str: The processed data or analysis.
    """
    # Example: Extracting numbers and performing simple analysis
    try:
        numbers = re.findall(r"\d+(\.\d{1,2})?", data)  # Find all numbers
        if numbers:
            total = sum(map(float, numbers))
            return f"Total sum of numbers found: ${total:.2f}"
        else:
            return "No numbers found in the input."
    except Exception as e:
        return f"Error processing financial data: {e}"


def log_user_activity(name: str, action: str):
    """
    Log user activities like asking a question or uploading a document.
    Args:
        name (str): The user's name.
        action (str): The action the user performed (e.g., 'Asked a question').
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("user_activity.log", "a") as log_file:
        log_file.write(f"{timestamp} - {name}: {action}\n")
    print(f"Logged action: {action} for user: {name}")
