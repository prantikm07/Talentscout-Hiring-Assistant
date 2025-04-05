# gemini_integration.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")

def format_chat_history(chat_history):
    """
    Format chat history to match Gemini API requirements.
    
    Args:
        chat_history (list): List of dictionaries with 'role' and 'content' keys.
        
    Returns:
        list: Formatted list compatible with Gemini API.
    """
    formatted_history = []
    for message in chat_history:
        formatted_history.append({"parts": [{"text": message["content"]}]})
    return formatted_history

def generate_response(prompt, chat_history=None):
    """
    Generate a response from the Gemini model.
    
    Args:
        prompt (str): The prompt to send to the model.
        chat_history (list, optional): List of previous messages.
        
    Returns:
        str: The generated response text.
    """
    if chat_history:
        formatted_history = format_chat_history(chat_history)
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(prompt)
    else:
        response = model.generate_content(prompt)
    
    return response.text
