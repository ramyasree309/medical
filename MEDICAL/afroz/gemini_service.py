"""
Gemini API service for medical records summarization.
"""
import google.generativeai as genai
from config import GEMINI_API_KEY, MAX_TOKENS, TEMPERATURE
import streamlit as st


def initialize_gemini(api_key=None):
    """Initialize Gemini API with API key."""
    # Use provided API key, or get from config
    from config import get_gemini_api_key
    api_key = api_key or get_gemini_api_key()
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in the sidebar or .env file.")
    genai.configure(api_key=api_key)
    return genai


def list_available_models(api_key=None):
    """List all available Gemini models."""
    try:
        genai = initialize_gemini(api_key=api_key)
        models = genai.list_models()
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name.replace('models/', ''))
        return available_models
    except Exception as e:
        return [f"Error listing models: {str(e)}"]


def extract_text_from_pdf(file):
    """Extract text from PDF file."""
    try:
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None


def extract_text_from_txt(file):
    """Extract text from text file."""
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading text file: {str(e)}")
        return None


def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file based on file type."""
    file_extension = uploaded_file.name.lower().split('.')[-1]
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_extension == 'txt':
        return extract_text_from_txt(uploaded_file)
    else:
        st.error(f"Unsupported file type: {file_extension}")
        return None


def summarize_medical_record(text, model_name="gemini-pro", api_key=None):
    """
    Summarize medical record using Gemini API.
    
    Args:
        text: The medical record text to summarize
        model_name: The Gemini model to use
        api_key: Optional API key (if not provided, uses config)
        
    Returns:
        Summary of the medical record
    """
    try:
        genai = initialize_gemini(api_key=api_key)
        
        # Try to list models first to see what's available and find a working one
        working_model = None
        try:
            models = genai.list_models()
            available_model_names = []
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    # Store both with and without 'models/' prefix
                    model_short = m.name.replace('models/', '')
                    available_model_names.append(model_short)
            
            # Try the requested model first
            if model_name in available_model_names:
                working_model = model_name
            else:
                # Try common alternatives in order of preference
                alternatives = [
                    'gemini-pro',
                    'gemini-1.5-pro-latest', 
                    'gemini-1.5-flash-latest',
                    'gemini-1.5-pro',
                    'gemini-1.5-flash',
                    'models/gemini-pro',
                    'models/gemini-1.5-pro-latest'
                ]
                for alt in alternatives:
                    alt_clean = alt.replace('models/', '')
                    if alt_clean in available_model_names:
                        working_model = alt_clean
                        break
                
                # If still no match, use first available
                if not working_model and available_model_names:
                    working_model = available_model_names[0]
        except Exception as list_error:
            # If listing fails, try common model names directly
            pass
        
        # Use working model if found, otherwise use the requested one
        final_model_name = working_model if working_model else model_name
        model = genai.GenerativeModel(final_model_name)
        
        prompt = f"""You are a medical records summarization expert. Please analyze the following medical record and provide a comprehensive summary.

Medical Record:
{text}

Please provide a structured summary including:
1. Patient Information (if available)
2. Chief Complaint / Primary Diagnosis
3. Key Medical History
4. Current Medications
5. Vital Signs (if mentioned)
6. Test Results (if mentioned)
7. Treatment Plan / Recommendations
8. Important Notes or Warnings

Format the summary in a clear, professional manner suitable for healthcare professionals."""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_TOKENS,
            }
        )
        
        return response.text
    except Exception as e:
        # Try to get available models for better error message
        try:
            genai = initialize_gemini(api_key=api_key)
            models = genai.list_models()
            available_models = [m.name.replace('models/', '') for m in models if 'generateContent' in m.supported_generation_methods]
            error_msg = f"Error generating summary: {str(e)}\n\nAvailable models: {', '.join(available_models[:5])}"
            raise Exception(error_msg)
        except:
            raise Exception(f"Error generating summary: {str(e)}")


def stream_summarization(text, model_name="gemini-pro", api_key=None):
    """
    Stream summarization response from Gemini API.
    
    Args:
        text: The medical record text to summarize
        model_name: The Gemini model to use
        api_key: Optional API key (if not provided, uses config)
        
    Yields:
        Chunks of the summary as they are generated
    """
    try:
        genai = initialize_gemini(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""You are a medical records summarization expert. Please analyze the following medical record and provide a comprehensive summary.

Medical Record:
{text}

Please provide a structured summary including:
1. Patient Information (if available)
2. Chief Complaint / Primary Diagnosis
3. Key Medical History
4. Current Medications
5. Vital Signs (if mentioned)
6. Test Results (if mentioned)
7. Treatment Plan / Recommendations
8. Important Notes or Warnings

Format the summary in a clear, professional manner suitable for healthcare professionals."""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_TOKENS,
            },
            stream=True
        )
        
        for chunk in response:
            yield chunk.text
    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")
