import os
import google.generativeai as genai  # Correct import for gemini
from dotenv import load_dotenv
from flask import Flask, request, render_template

# Load environment variables from .env file
load_dotenv()

# Set up the Gemini API key using the SDK
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

def generate_from_gemini(prompt):
    """
    Function to call Google Gemini API and generate a response based on the prompt.
    """
    try:
        # Create a generative model instance
        model = genai.GenerativeModel("gemini-1.5")  # Use the appropriate model, adjust if necessary
        response = model.generate_content(prompt)  # Generate content using the model
        print(f"Generated response: {response.text}")  # Debug: print the response
        return response.text
    except Exception as e:
        # Handle any errors that occur during the API call
        print(f"Error generating content from Gemini: {e}")
        return f"Error generating content: {str(e)}"

# Define route to handle incoming Telegram messages
@app.route("/telegram", methods=["POST"])
def telegram():
    update = request.get_json()
    handle_telegram_webhook(update)
    return "ok", 200

def handle_telegram_webhook(update):
    """Handles incoming Telegram messages and sends responses."""
    try:
        chat_id = update['message']['chat']['id']
        user_message = update['message']['text']
        print(f"Received message: {user_message} from chat_id: {chat_id}")

        # Generate a response for the received message using Gemini
        response = generate_telegram_reply(user_message)  # Calls the reply generation
        send_telegram_message(chat_id, response)
    except Exception as e:
        print(f"Error processing update: {e}")

# Function to send messages back to Telegram
def send_telegram_message(chat_id, text):
    telegram_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    
    # Send the message to Telegram
    response = requests.post(telegram_url, data=payload)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")
    else:
        print(f"Successfully sent message: {text} to chat_id: {chat_id}")

# Function to generate a reply from Gemini for Telegram messages
def generate_telegram_reply(message):
    print(f"Generating response for message: {message}")
    
    if "hello" in message.lower():
        return "Hello! How can I assist you today?"
    
    elif "inflation" in message.lower():
        return "Inflation is the rate at which the general level of prices for goods and services rises, and subsequently, the purchasing power of currency falls."
    
    # Generate AI response for other finance-related queries
    else:
        try:
            # Prepare prompt for the AI model (Gemini or other)
            system_prompt = "You are a financial assistant. Answer finance-related questions."
            prompt = f"{system_prompt}\n\nUser Question: {message}"

            # Call the function to get the AI response from Gemini
            ai_response = generate_from_gemini(prompt)
            print(f"AI Response: {ai_response}")
            return ai_response
        
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "Sorry, I couldn't process that request. Please try again."

# Run the Flask app locally
if __name__ == "__main__":
    app.run(debug=True, port=5000)
