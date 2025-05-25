import re
from datetime import datetime
from PyPDF2 import PdfReader
import pandas as pd
from PIL import Image
import io

def sanitize_input(text: str) -> str:
    """
    Clean and sanitize user input to prevent malicious content or errors.
    """
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def log_user_activity(user: str, action: str):
    """
    Log user activities like asking a question or uploading a document.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("user_activity.log", "a") as log_file:
        log_file.write(f"{timestamp} - {user}: {action}\n")
    print(f"Logged: {user} - {action}")

# Optional: keep if you're doing file validation
def validate_file(file_bytes: bytes, file_type: str) -> bool:
    if file_type == 'pdf':
        return validate_pdf(file_bytes)
    elif file_type == 'csv':
        return validate_csv(file_bytes)
    elif file_type in ['jpg', 'jpeg', 'png']:
        return validate_image(file_bytes)
    return False

def validate_pdf(file_bytes: bytes) -> bool:
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        return len(reader.pages) > 0
    except Exception as e:
        print(f"Error validating PDF: {e}")
        return False

def validate_csv(file_bytes: bytes) -> bool:
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
        return not df.empty
    except Exception as e:
        print(f"Error validating CSV: {e}")
        return False

def validate_image(file_bytes: bytes) -> bool:
    try:
        image = Image.open(io.BytesIO(file_bytes))
        image.verify()
        return True
    except Exception as e:
        print(f"Error validating image: {e}")
        return False
