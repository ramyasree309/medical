"""
Medical Records Summarization App
A beautiful Streamlit application for summarizing medical records using Gemini API.
"""
import streamlit as st
import time
from datetime import datetime
from gemini_service import (
    extract_text_from_file,
    summarize_medical_record,
    stream_summarization
)
from config import APP_TITLE, APP_SUBTITLE, ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB, GEMINI_API_KEY
from file_storage import save_uploaded_file, save_summary, get_storage_stats, create_zip_archive

# Page Configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    /* Main App Styling */
    .main {
        padding: 2rem 1rem;
    }
    
    /* Header Styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Card Styling */
    .stCard {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Upload Area Styling */
    .upload-area {
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        background: #f8f9fa;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #764ba2;
        background: #e9ecef;
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Summary Box Styling */
    .summary-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin-top: 2rem;
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    /* Success Message */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    /* Error Message */
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* File Info Styling */
    .file-info {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Stats Styling */
    .stat-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


def display_header():
    """Display the main header."""
    st.markdown("""
        <div class="main-header">
            <h1>🏥 Medical Records Summarization</h1>
            <p>AI-Powered Medical Document Analysis & Summarization</p>
        </div>
    """, unsafe_allow_html=True)


def display_file_info(uploaded_file):
    """Display information about the uploaded file."""
    if uploaded_file:
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # Size in MB
        st.markdown(f"""
            <div class="file-info">
                <strong>📄 File:</strong> {uploaded_file.name}<br>
                <strong>📊 Size:</strong> {file_size:.2f} MB<br>
                <strong>📅 Uploaded:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </div>
        """, unsafe_allow_html=True)


def display_stats(text_length, summary_length, processing_time):
    """Display statistics about the processing."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{text_length:,}</div>
                <div class="stat-label">Characters Processed</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{summary_length:,}</div>
                <div class="stat-label">Summary Length</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{processing_time:.1f}s</div>
                <div class="stat-label">Processing Time</div>
            </div>
        """, unsafe_allow_html=True)


def main():
    """Main application function."""
    display_header()
    
    # Initialize session state
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'uploaded_text' not in st.session_state:
        st.session_state.uploaded_text = None
    if 'processing_stats' not in st.session_state:
        st.session_state.processing_stats = None
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = GEMINI_API_KEY
    
    # Sidebar with team info and API key configuration
    with st.sidebar:
        # Team Information Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; color: white;">
            <h2 style="color: white; margin-bottom: 0.5rem; font-size: 1.3rem;">👥 Team Information</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Team Name
        st.markdown("#### 🏢 Team Name")
        st.info("**Medical AI Team**")
        
        st.markdown("---")
        
        # Project Name
        st.markdown("#### 📋 Project Name")
        st.info("**Medical Records Summarization**")
        
        st.markdown("---")
        
        # Team Members
        st.markdown("#### 👨‍💻 Team Members")
        team_members = [
            "Shaik Afroz",
            "Shaik Sudheer Basha",
            "P. Lakshmi Narendra"
        ]
        
        for member in team_members:
            st.markdown(f"• **{member}**")
        
        st.markdown("---")
        
        # API Key Configuration
        st.markdown("### 🔑 API Configuration")
        
        # API Key Input
        api_key_input = st.text_input(
            "Gemini API Key",
            value=st.session_state.gemini_api_key if st.session_state.gemini_api_key else "",
            type="password",
            help="Enter your Google Gemini API key. Get one from https://makersuite.google.com/app/apikey",
            placeholder="Enter your API key here..."
        )
        
        if api_key_input:
            st.session_state.gemini_api_key = api_key_input
            st.success("✅ API key saved!")
        elif st.session_state.gemini_api_key:
            st.info("✅ API key is configured")
        else:
            st.warning("⚠️ Please enter your API key to continue")
        
        st.markdown("---")
        
        # Model Selection
        st.markdown("### 🤖 Model Selection")
        
        # Try to get available models
        from gemini_service import list_available_models
        try:
            available_models = list_available_models(st.session_state.gemini_api_key if st.session_state.gemini_api_key else None)
            if available_models and not isinstance(available_models[0], str) or (isinstance(available_models[0], str) and not available_models[0].startswith("Error")):
                model_options = {model: model for model in available_models[:5]}  # Limit to first 5
            else:
                # Fallback to common model names
                model_options = {
                    "gemini-pro": "Gemini Pro (Default)",
                    "gemini-1.5-pro-latest": "Gemini 1.5 Pro Latest",
                    "gemini-1.5-flash-latest": "Gemini 1.5 Flash Latest"
                }
        except:
            # Fallback to common model names
            model_options = {
                "gemini-pro": "Gemini Pro (Default)",
                "gemini-1.5-pro-latest": "Gemini 1.5 Pro Latest",
                "gemini-1.5-flash-latest": "Gemini 1.5 Flash Latest"
            }
        
        if 'selected_model' not in st.session_state:
            st.session_state.selected_model = "gemini-pro"
        
        selected_model = st.selectbox(
            "Choose AI Model",
            options=list(model_options.keys()),
            format_func=lambda x: f"{x} - {model_options[x]}" if isinstance(model_options[x], str) and model_options[x] != x else x,
            index=list(model_options.keys()).index(st.session_state.selected_model) if st.session_state.selected_model in model_options else 0
        )
        st.session_state.selected_model = selected_model
        
        st.markdown("---")
        
        # Storage Statistics
        st.markdown("### 📁 Storage")
        try:
            stats = get_storage_stats()
            st.metric("Total Files", stats['total_files'])
            st.metric("Uploaded Files", stats.get('uploads_count', 0))
            st.metric("Generated Summaries", stats.get('summaries_count', 0))
            st.metric("Total Storage", f"{stats['total_size_mb']:.2f} MB")
            
            # Download all files as zip
            if stats['total_files'] > 0:
                if st.button("📦 Download All Files as ZIP", use_container_width=True):
                    try:
                        zip_path = create_zip_archive()
                        if zip_path and os.path.exists(zip_path):
                            with open(zip_path, "rb") as f:
                                st.download_button(
                                    label="⬇️ Download ZIP File",
                                    data=f.read(),
                                    file_name=os.path.basename(zip_path),
                                    mime="application/zip",
                                    use_container_width=True
                                )
                    except Exception as e:
                        st.error(f"Error creating zip: {str(e)}")
        except Exception as e:
            st.info("Storage stats unavailable")
        
        st.markdown("---")
        
        st.markdown("### 📖 Instructions")
        st.markdown("""
        1. **Enter** your Gemini API key above
        2. **Upload** a medical record file (PDF or TXT)
        3. **Preview** the extracted text (optional)
        4. **Click** "Generate Summary" to analyze
        5. **Review** the AI-generated summary
        6. **Download** the summary if needed
        
        ---
        
        ### ⚙️ Settings
        """)
        
        use_streaming = st.checkbox("Use Streaming (Experimental)", value=False)
        
        st.markdown("""
        ---
        
        ### ℹ️ About
        This application uses Google's Gemini AI to summarize medical records.
        All processing is done securely and your data is not stored.
        
        ### 🔒 Privacy
        - Files are processed in memory only
        - No data is stored on servers
        - API calls are made securely
        """)
    
    # Check if API key is available
    current_api_key = st.session_state.gemini_api_key or GEMINI_API_KEY
    if not current_api_key:
        st.warning("⚠️ **API Key Required**")
        st.info("""
        Please enter your Gemini API key in the sidebar to get started.
        
        **How to get an API key:**
        1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy the key and paste it in the sidebar
        """)
        
        # Show a nice card for API key input in main area too
        with st.container():
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 2rem 0;">
                <h2>🔑 Get Started</h2>
                <p style="font-size: 1.1rem;">Enter your API key in the sidebar (←) to begin</p>
            </div>
            """, unsafe_allow_html=True)
        return
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Medical Record")
        st.markdown("""
            <div class="upload-area">
                <p style="font-size: 1.2rem; color: #667eea;">
                    📄 Drag and drop your medical record here<br>
                    or use the file uploader below
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt'],
            help="Upload PDF or TXT files containing medical records",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            display_file_info(uploaded_file)
            
            # Save uploaded file to folder
            try:
                saved_path = save_uploaded_file(uploaded_file)
                st.success(f"✅ File saved to: {saved_path}")
            except Exception as e:
                st.warning(f"⚠️ Could not save file: {str(e)}")
            
            # Extract text from file
            with st.spinner("📖 Extracting text from document..."):
                extracted_text = extract_text_from_file(uploaded_file)
            
            if extracted_text:
                st.session_state.uploaded_text = extracted_text
                
                # Show extracted text preview
                with st.expander("📝 Preview Extracted Text", expanded=False):
                    st.text_area(
                        "Extracted Text",
                        extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
                        height=200,
                        disabled=True
                    )
                
                # Summarize button
                if st.button("🔍 Generate Summary", type="primary", use_container_width=True):
                    if st.session_state.uploaded_text:
                        start_time = time.time()
                        
                        # Create placeholder for summary
                        summary_placeholder = st.empty()
                        
                        # Show loading animation
                        with summary_placeholder.container():
                            st.markdown("""
                                <div class="loading-spinner">
                                    <h3>🔄 Processing your medical record...</h3>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                # Stream the summarization
                                status_text.text("📊 Analyzing document structure...")
                                progress_bar.progress(20)
                                
                                status_text.text("🤖 Generating summary with AI...")
                                progress_bar.progress(50)
                                
                                # Generate summary
                                summary = summarize_medical_record(
                                    st.session_state.uploaded_text,
                                    model_name=st.session_state.selected_model,
                                    api_key=st.session_state.gemini_api_key
                                )
                                
                                progress_bar.progress(80)
                                status_text.text("✨ Finalizing summary...")
                                
                                processing_time = time.time() - start_time
                                progress_bar.progress(100)
                                
                                # Store results
                                st.session_state.summary = summary
                                st.session_state.processing_stats = {
                                    'text_length': len(st.session_state.uploaded_text),
                                    'summary_length': len(summary),
                                    'processing_time': processing_time
                                }
                                
                                # Save summary to folder
                                try:
                                    summary_path = save_summary(summary, uploaded_file.name if uploaded_file else None)
                                    st.session_state.saved_summary_path = summary_path
                                except Exception as e:
                                    st.warning(f"⚠️ Could not save summary: {str(e)}")
                                
                                status_text.text("✅ Summary generated successfully!")
                                time.sleep(0.5)
                                
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                                st.info("💡 Please check your API key and try again.")
    
    with col2:
        st.markdown("### 📋 Generated Summary")
        
        if st.session_state.summary:
            # Display statistics
            if st.session_state.processing_stats:
                stats = st.session_state.processing_stats
                display_stats(
                    stats['text_length'],
                    stats['summary_length'],
                    stats['processing_time']
                )
            
            # Display summary
            st.markdown("""
                <div class="summary-box">
            """, unsafe_allow_html=True)
            
            st.markdown(st.session_state.summary)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Show saved path if available
            if 'saved_summary_path' in st.session_state and st.session_state.saved_summary_path:
                st.info(f"💾 Summary saved to: `{st.session_state.saved_summary_path}`")
            
            # Download button
            st.download_button(
                label="📥 Download Summary",
                data=st.session_state.summary,
                file_name=f"medical_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Clear button
            if st.button("🗑️ Clear Summary", use_container_width=True):
                st.session_state.summary = None
                st.session_state.uploaded_text = None
                st.session_state.processing_stats = None
                st.rerun()
        else:
            st.info("👈 Upload a medical record and click 'Generate Summary' to see the results here.")
    


if __name__ == "__main__":
    main()
