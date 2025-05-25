from flask import Flask, request, render_template
import os
import requests

app = Flask(__name__)

# Define the function to generate a response based on user input
def generate_telegram_reply(message):
    print(f"Generating response for message: {message}")
    
    # Handle basic queries
    if "hello" in message.lower():
        return "Hello! How can I assist you today?"
    
    elif "inflation" in message.lower():
        return "Inflation is the rate at which the general level of prices for goods and services rises, and subsequently, the purchasing power of currency falls."
    
    # AI-based response for more complex queries
    else:
        try:
            # Prepare prompt for the AI model (Gemini or other)
            system_prompt = "You are a financial assistant. Answer finance-related questions."
            prompt = f"{system_prompt}\n\nUser Question: {message}"

            # Call the function to get the AI response (this needs to be defined)
            ai_response = generate_from_gemini(prompt)
            
            # Log the AI response for debugging purposes
            print(f"AI Response: {ai_response}")

            return ai_response
        
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "Sorry, I couldn't process that request. Please try again."

# Function to interact with Gemini or another AI API
def generate_from_gemini(prompt):
    """
    This function interacts with the AI model (e.g., Google Gemini or OpenAI).
    Replace this with actual code to call the AI model API.
    """
    try:
        # Example for OpenAI integration (if you are using OpenAI)
        response = openai.Completion.create(
            engine="text-davinci-003",  # Update with your model name
            prompt=prompt,
            max_tokens=100
        )
        
        # Return the AI-generated text
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating content from Gemini: {e}")
        return "Sorry, there was an error connecting to the AI service."

# Define the route to handle incoming messages from Telegram
@app.route("/telegram", methods=["POST"])
def telegram():
    update = request.get_json()
    print(f"Received update: {update}")  # Log the incoming update
    handle_telegram_webhook(update)
    return "ok", 200

# Example function for handling the webhook
def handle_telegram_webhook(update):
    """Handles incoming Telegram messages and sends responses."""
    try:
        chat_id = update['message']['chat']['id']
        user_message = update['message']['text']
        print(f"Received message: {user_message} from chat_id: {chat_id}")

        # Generate a response for the received message
        response = generate_telegram_reply(user_message)  # Call the reply generation
        send_telegram_message(chat_id, response)
    except Exception as e:
        print(f"Error processing update: {e}")

def send_telegram_message(chat_id, text):
    telegram_url = f"https://api.telegram.org/bot{os.getenv('GEMINI_TELEGRAM_TOKEN')}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    
    # Send the message to Telegram
    response = requests.post(telegram_url, data=payload)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")
    else:
        print(f"Successfully sent message: {text} to chat_id: {chat_id}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
