"""
Configuration module for medical records summarization app.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def get_gemini_api_key():
    """Get Gemini API key from session state or environment variable."""
    try:
        import streamlit as st
        if hasattr(st, 'session_state') and 'gemini_api_key' in st.session_state and st.session_state.gemini_api_key:
            return st.session_state.gemini_api_key
    except:
        pass
    return os.getenv("GEMINI_API_KEY", "")

# App Configuration
APP_TITLE = "Medical Records Summarization"
APP_SUBTITLE = "AI-Powered Medical Document Analysis"

# File Upload Configuration
ALLOWED_EXTENSIONS = [".pdf", ".txt", ".docx"]
MAX_FILE_SIZE_MB = 10

# Summarization Configuration
MAX_TOKENS = 2000
TEMPERATURE = 0.3
