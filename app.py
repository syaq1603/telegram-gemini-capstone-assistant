# Import new libraries and fix app.py
from flask import Flask, request, render_template
from dotenv import load_dotenv
import openai
import os
import PyPDF2
import docx
import tempfile
import logging

from bot import handle_telegram_webhook, set_telegram_webhook, remove_telegram_webhook
from handler import log_user_activity, sanitize_input

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
        return f"OpenAI error: {e}"

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
        return f"Error reading file: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        if prompt:
            try:
                cleaned_prompt = sanitize_input(prompt)
                log_user_activity("guest", "Asked a question")
                response = get_chat_response(cleaned_prompt)
                return render_template("openai_reply.html", r=response)
            except Exception as e:
                return render_template("openai_reply.html", r=f"Error: {str(e)}")
    return render_template("ai_assistant.html")

@app.route('/analyze_file', methods=['POST'])
def analyze_file():
    try:
        if 'file' not in request.files:
            return {'status': 'error', 'response': 'No file uploaded'}

        file = request.files['file']
        prompt = request.form.get('prompt', '')

        if file.filename == '':
            return {'status': 'error', 'response': 'No file selected'}

        file_content = read_file_content(file)
        full_prompt = f"{prompt}\n\nDocument Content:\n{file_content}"

        response = get_chat_response(full_prompt)
        return render_template("openai_reply.html", r=response, file_text=file_content)

    except Exception as e:
        return render_template("openai_reply.html", r=f"Error: {str(e)}")

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    update = request.get_json(force=True)
    handle_telegram_webhook(update)
    return "OK", 200

@app.route('/start_telegram', methods=['POST'])
def start_telegram():
    response = set_telegram_webhook()
    return render_template("telegram_reply.html", user_message="Bot Started", bot_response=response.text)

@app.route('/stop_telegram', methods=['POST'])
def stop_telegram():
    response = remove_telegram_webhook()
    return render_template("telegram_reply.html", user_message="Bot Stopped", bot_response=response.text)

@app.route('/telegram_page')
def telegram_page():
    return render_template("telegram.html", status="Active")

@app.route('/del_logs')
def del_logs():
    try:
        if os.path.exists("user_activity.log"):
            os.remove("user_activity.log")
        return render_template("del_logs.html")
    except Exception as e:
        return f"Error deleting logs: {e}"

@app.route('/logs')
def logs():
    try:
        with open("user_activity.log", "r") as log_file:
            return f"<pre>{log_file.read()}</pre>"
    except FileNotFoundError:
        return "No logs found."

# ---------- Run the App ----------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
