# Import Libraries
from flask import Flask, request, render_template, jsonify
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import os
import PyPDF2
import docx
import tempfile
import json
import logging
import tempfile

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Flask logging for troubleshooting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Google Cloud credentials
#GOOGLE_APPLICATION_CREDENTIALS = "/etc/secrets/google-credentials.json"
gcp_project = os.environ["GOOGLE_PROJECT"] 
gen_location = os.environ["GOOGLE_LOCATION"]
gen_model = os.environ["GOOGLE_GEN_MODEL"]

# Initialize Vertex AI
aiplatform.init(project=gcp_project, location=gen_location)

# Initialize model
model = GenerativeModel(gen_model)

def get_chat_response(prompt: str) -> str:
    # Create a new chat session for each request
    chat_session = model.start_chat()
    response = chat_session.send_message(prompt)
    return response.text

def read_file_content(file):
    """Extract text from various file formats"""
    filename = file.filename.lower()
    content = ""
    
    try:
        if filename.endswith('.txt'):
            content = file.read().decode('utf-8')
        
        elif filename.endswith('.pdf'):
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                file.save(temp_file.name)
                
            # Read PDF content
            with open(temp_file.name, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    content += page.extract_text()
            
            # Clean up temporary file
            os.unlink(temp_file.name)
        
        elif filename.endswith(('.doc', '.docx')):
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=filename[-5:]) as temp_file:
                file.save(temp_file.name)
            
            # Read DOC/DOCX content
            doc = docx.Document(temp_file.name)
            content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            # Clean up temporary file
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
            return {'status': 'error', 'response': 'No file selected'}
        
        # Extract text from file
        file_content = read_file_content(file)
        
        # Create prompt with file content
        full_prompt = f"""
        Analyze the following text and answer the question: {prompt}

        Text content:
        {file_content}
        """
        
        # Get response from Gemini
        response = get_chat_response(full_prompt)
        
        return {'status': 'success', 'response': response}
    
    except Exception as e:
        return {'status': 'error', 'response': str(e)}

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)