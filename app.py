# Import Libraries
from flask import Flask, request, render_template
from dotenv import load_dotenv
import openai
import os
import PyPDF2
import docx
import tempfile
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Flask logging for troubleshooting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get API Key from .env
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

def get_chat_response(prompt: str) -> str:
    """Generate a response using OpenAI ChatCompletion"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise

def read_file_content(file):
    """Extract text from various file formats"""
    filename = file.filename.lower()
    content = ""

    try:
        if filename.endswith('.txt'):
            content = file.read().decode('utf-8')

        elif filename.endswith('.pdf'):
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                file.save(temp_file.name)

            with open(temp_file.name, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    content += page.extract_text()

            os.unlink(temp_file.name)

        elif filename.endswith(('.doc', '.docx')):
            with tempfile.NamedTemporaryFile(delete=False, suffix=filename[-5:]) as temp_file:
                file.save(temp_file.name)

            doc = docx.Document(temp_file.name)
            content = "\n".join([p.text for p in doc.paragraphs])

            os.unlink(temp_file.name)

        else:
            raise ValueError("Unsupported file format")

        return content.strip()

    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        if prompt:
            try:
                response = get_chat_response(prompt)
                return {'status': 'success', 'response': response}
            except Exception as e:
                return {'status': 'error', 'response': str(e)}
    return render_template('index.html')

@app.route('/analyze_file', methods=['POST'])
def analyze_file():
    try:
        if 'file' not in request.files:
            return {'status': 'error', 'response': 'No file uploaded'}

        file = request.files['file']
        prompt = request.form.get('prompt', '')

        if file.filename == '':
