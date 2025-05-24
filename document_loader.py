import fitz  # PyMuPDF
import docx2txt
import os

def extract_text_from_pdf(file_path):
    """Extract text from each page of a PDF using PyMuPDF"""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file using docx2txt"""
    return docx2txt.process(file_path)

def extract_text(file_path):
    """Auto-detect file type and extract text"""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")
