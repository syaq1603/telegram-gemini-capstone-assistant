import PyPDF2
import pandas as pd
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(file_bytes):
    """
    Extract text from a PDF file.
    Args:
        file_bytes (bytes): The byte content of the PDF file.
    Returns:
        str: The extracted text from the PDF file.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        return text.strip() if text else "No readable text found in PDF."
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

def extract_text_from_csv(file_bytes):
    """
    Extract text from a CSV file.
    Args:
        file_bytes (bytes): The byte content of the CSV file.
    Returns:
        str: The extracted text from the CSV file.
    """
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
        return df.to_string(index=False)
    except Exception as e:
        return f"Error extracting text from CSV: {e}"

def extract_text_from_image(file_bytes):
    """
    Extract text from an image using Optical Character Recognition (OCR).
    Args:
        file_bytes (bytes): The byte content of the image file.
    Returns:
        str: The extracted text from the image.
    """
    try:
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        return text.strip() if text else "No readable text found in image."
    except Exception as e:
        return f"Error extracting text from image: {e}"

def extract_text_from_file(file_bytes, filename):
    """
    Extract text from various file types (PDF, CSV, Image).
    Args:
        file_bytes (bytes): The byte content of the file.
        filename (str): The name of the uploaded file.
    Returns:
        str: The extracted text or an error message.
    """
    filename = filename.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.endswith(".csv"):
        return extract_text_from_csv(file_bytes)
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        return extract_text_from_image(file_bytes)
    else:
        return "Unsupported file format."
