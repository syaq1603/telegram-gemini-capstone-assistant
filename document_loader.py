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
        # Read the PDF content from the byte data
        pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(file_bytes))
        text = ""
        
        # Extract text from each page of the PDF
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
        
        if not text:
            return "No readable text found in PDF."
        
        return text
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
        # Read the CSV content using pandas
        df = pd.read_csv(io.BytesIO(file_bytes))
        
        # Convert the dataframe to text format (could be adjusted based on the required format)
        text = df.to_string(index=False)
        
        return text
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
        # Open the image using PIL and apply OCR using pytesseract
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        
        if not text:
            return "No readable text found in image."
        
        return text
    except Exception as e:
        return f"Error extracting text from image: {e}"


def extract_text_from_file(file_bytes, filename):
    """
    Extract text from various file types (PDF, CSV, Image, etc.).
    Args:
        file_bytes (bytes): The byte content of the file.
        filename (str): The name of the uploaded file.
    Returns:
        str: The extracted text from the file.
    """
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.endswith(".csv"):
        return extract_text_from_csv(file_bytes)
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        return extract_text_from_image(file_bytes)
    else:
        return "Unsupported file format."
