text
# TalentScout Hiring Assistant

An intelligent chatbot that assists in the initial screening of candidates for technology positions.

## Overview

The TalentScout Hiring Assistant is an AI-powered chatbot designed to streamline the initial candidate screening process. It collects essential candidate information and generates relevant technical questions based on the candidate's declared tech stack.

## Features

- Interactive and user-friendly interface
- Automated collection of candidate information
- AI-generated technical questions tailored to the candidate's tech stack
- Seamless conversation handling
- Secure data storage

## Installation

1. Clone this repository:
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant

text

2. Install the required packages:
pip install -r requirements.txt

text

3. Create a `.env` file in the project root with your Gemini API key:
GEMINI_API_KEY=your_gemini_api_key_here

text

4. Run the application:
streamlit run app.py

text

## Usage

1. Start the application using the command above
2. The chatbot will greet the candidate and begin collecting information
3. Once all information is collected, the chatbot will generate technical questions based on the candidate's tech stack
4. The conversation will continue until all questions are answered or the candidate ends the chat
5. Candidate information and the conversation history can be viewed and exported from the sidebar

## Technologies Used

- Python
- Streamlit
- Google Gemini 2.0 Flash-Lite API
- Pandas

## License

MIT

## Author

Your Name