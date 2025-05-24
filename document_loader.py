# document_loader.py

import fitz  # PyMuPDF
import docx2txt
import os
import pandas as pd

def extract_text_from_pdf(file_path):
    """Extract text from each page of a PDF using PyMuPDF"""
    with fitz.open(file_path) as doc:
        return "\n".join(page.get_text() for page in doc)

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file using docx2txt"""
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    """Extract plain text from a .txt file"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_csv(file_path):
    """Extract readable text from a CSV file"""
    df = pd.read_csv(file_path)
    return df.to_string(index=False)

def extract_text(file_path):
    """Auto-detect file type and extract text"""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext == ".csv":
        return extract_text_from_csv(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, TXT, or CSV.")
