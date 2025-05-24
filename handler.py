import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

def extract_text_from_pdf(file_bytes):
    """Extract text from a PDF byte stream."""
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def extract_text_from_image(file_bytes):
    """Extract text from an image byte stream."""
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    text = pytesseract.image_to_string(image)
    return text.strip()

def extract_text_from_file(file_bytes, file_path):
    """
    Determines file type from path and routes to the appropriate extractor.
    :param file_bytes: BytesIO content from downloaded file
    :param file_path: Full file path from Telegram's getFile API
    :return: Extracted text as string
    """
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_bytes)
    else:
        return "Unsupported file type for extraction."
