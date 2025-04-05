# app.py
import streamlit as st
import pandas as pd
import time
from gemini_integration import generate_response
from prompts import (
    GREETING_PROMPT, 
    INFORMATION_GATHERING_PROMPT, 
    TECHNICAL_QUESTIONS_PROMPT,
    FALLBACK_PROMPT,
    CONVERSATION_END_PROMPT
)

# Set page configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="👔",
    layout="wide"
)

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {
        "full_name": None,
        "email": None,
        "phone": None,
        "experience": None,
        "position": None,
        "location": None,
        "tech_stack": None
    }
if "current_stage" not in st.session_state:
    st.session_state.current_stage = "greeting"
if "questions_generated" not in st.session_state:
    st.session_state.questions_generated = False
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Helper functions for candidate information processing
def update_candidate_info(message):
    """
    Update candidate information based on user input and advance to the next stage.
    """
    if st.session_state.current_stage == "name":
        st.session_state.candidate_info["full_name"] = message
        st.session_state.current_stage = "email"
    elif st.session_state.current_stage == "email":
        st.session_state.candidate_info["email"] = message
        st.session_state.current_stage = "phone"
    elif st.session_state.current_stage == "phone":
        st.session_state.candidate_info["phone"] = message
        st.session_state.current_stage = "experience"
    elif st.session_state.current_stage == "experience":
        st.session_state.candidate_info["experience"] = message
        st.session_state.current_stage = "position"
    elif st.session_state.current_stage == "position":
        st.session_state.candidate_info["position"] = message
        st.session_state.current_stage = "location"
    elif st.session_state.current_stage == "location":
        st.session_state.candidate_info["location"] = message
        st.session_state.current_stage = "tech_stack"
    elif st.session_state.current_stage == "tech_stack":
        st.session_state.candidate_info["tech_stack"] = message
        st.session_state.current_stage = "technical_questions"


def get_next_prompt():
    """
    Determine the next prompt based on the current stage of the conversation.
    """
    if st.session_state.current_stage == "greeting":
        st.session_state.current_stage = "name"
        return GREETING_PROMPT
    elif st.session_state.current_stage == "name":
        return "What is your full name?"
    elif st.session_state.current_stage == "email":
        return "What is your email address?"
    elif st.session_state.current_stage == "phone":
        return "What is your phone number?"
    elif st.session_state.current_stage == "experience":
        return "How many years of experience do you have?"
    elif st.session_state.current_stage == "position":
        return "What position are you applying for?"
    elif st.session_state.current_stage == "location":
        return "Where are you currently located?"
    elif st.session_state.current_stage == "tech_stack":
        return (
            "Please list your tech stack, including programming languages, frameworks, databases, "
            "and tools you are proficient in."
        )
    elif st.session_state.current_stage == "technical_questions" and not st.session_state.questions_generated:
        st.session_state.questions_generated = True
        prompt = TECHNICAL_QUESTIONS_PROMPT.format(
            tech_stack=st.session_state.candidate_info["tech_stack"],
            years_experience=st.session_state.candidate_info["experience"]
        )
        return prompt
    elif st.session_state.current_stage == "end":
        return CONVERSATION_END_PROMPT


def reset_chat():
    st.session_state.chat_history = []
    st.session_state.candidate_info = {
        "full_name": None,
        "email": None,
        "phone": None,
        "experience": None,
        "position": None,
        "location": None,
        "tech_stack": None
    }
    st.session_state.current_stage = "greeting"
    st.session_state.questions_generated = False
    st.session_state.conversation_history = []

# UI Components
# Simulating initial interaction
st.title("TalentScout Hiring Assistant")
st.subheader("AI-powered candidate screening")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.conversation_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Initialize the chat if it's empty
    if not st.session_state.conversation_history:
        initial_prompt = get_next_prompt()
        initial_response = generate_response(initial_prompt)
        
        # Add assistant's greeting to conversation history
        st.session_state.conversation_history.append({"role": "assistant", "content": initial_response})
        
        with st.chat_message("assistant"):
            st.write(initial_response)

# Sidebar with candidate information (as it's collected)
with st.sidebar:
    st.header("Candidate Information")
    if st.session_state.candidate_info["full_name"]:
        st.write(f"**Name:** {st.session_state.candidate_info['full_name']}")
    if st.session_state.candidate_info["email"]:
        st.write(f"**Email:** {st.session_state.candidate_info['email']}")
    if st.session_state.candidate_info["phone"]:
        st.write(f"**Phone:** {st.session_state.candidate_info['phone']}")
    if st.session_state.candidate_info["experience"]:
        st.write(f"**Experience:** {st.session_state.candidate_info['experience']}")
    if st.session_state.candidate_info["position"]:
        st.write(f"**Desired Position:** {st.session_state.candidate_info['position']}")
    if st.session_state.candidate_info["location"]:
        st.write(f"**Location:** {st.session_state.candidate_info['location']}")
    if st.session_state.candidate_info["tech_stack"]:
        st.write(f"**Tech Stack:** {st.session_state.candidate_info['tech_stack']}")
    
    if st.button("Reset Chat"):
        reset_chat()

# Chat input - using a unique key to avoid the duplicate error
user_input = st.chat_input("Type your message here...", key="unique_chat_input")
if user_input:
    # Display user message
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Check for exit keywords
    exit_keywords = ["exit", "quit", "bye", "goodbye", "end"]
    if any(keyword in user_input.lower() for keyword in exit_keywords):
        st.session_state.current_stage = "end"
    else:
        # Update candidate information based on the current stage
        update_candidate_info(user_input)
    
    # Get appropriate prompt and generate response
    next_prompt = get_next_prompt()
    
    # Add the user's message to the context
    context = f"Previous message from user: {user_input}\n\n{next_prompt}"
    
    # Show a spinner while generating the response
    with st.spinner("Thinking..."):
        ai_response = generate_response(context, st.session_state.chat_history)
    
    # Display assistant response
    st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.write(ai_response)
    
    # Update chat history for context in future responses
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

# Footer
# st.markdown("---")
# st.markdown("TalentScout Hiring Assistant | Powered by Gemini 2.0 Flash-Lite")