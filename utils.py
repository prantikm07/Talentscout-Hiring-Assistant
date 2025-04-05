# utils.py
import pandas as pd
import streamlit as st
import os
import json
from datetime import datetime

def save_candidate_data(candidate_info, conversation_history):
    """
    Save candidate data to a CSV file.
    
    Args:
        candidate_info (dict): Dictionary containing candidate information
        conversation_history (list): List of conversation messages
    """
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a directory for saving data if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Convert candidate info to DataFrame and save to CSV
    df = pd.DataFrame([candidate_info])
    df.to_csv(f"data/candidate_{timestamp}.csv", index=False)
    
    # Save conversation history to JSON
    with open(f"data/conversation_{timestamp}.json", "w") as f:
        json.dump(conversation_history, f)
        
    return f"data/candidate_{timestamp}.csv", f"data/conversation_{timestamp}.json"
