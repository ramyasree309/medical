"""
File storage utility for saving uploaded files and generated summaries.
"""
import os
import zipfile
from datetime import datetime
from pathlib import Path


# Storage directory - all files in one folder
STORAGE_DIR = "medical_records"

def ensure_directories():
    """Create storage directory if it doesn't exist."""
    os.makedirs(STORAGE_DIR, exist_ok=True)


def save_uploaded_file(uploaded_file):
    """
    Save uploaded file to the storage folder.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Path to saved file
    """
    ensure_directories()
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    filepath = os.path.join(STORAGE_DIR, filename)
    
    # Save file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return filepath


def save_summary(summary_text, original_filename=None):
    """
    Save generated summary to the storage folder.
    
    Args:
        summary_text: The summary text to save
        original_filename: Optional original filename for reference
        
    Returns:
        Path to saved summary file
    """
    ensure_directories()
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if original_filename:
        base_name = os.path.splitext(original_filename)[0]
        filename = f"summary_{timestamp}_{base_name}.txt"
    else:
        filename = f"summary_{timestamp}.txt"
    
    filepath = os.path.join(STORAGE_DIR, filename)
    
    # Save summary
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(summary_text)
    
    return filepath


def create_zip_archive():
    """Create a zip file of all stored files."""
    ensure_directories()
    
    if not os.path.exists(STORAGE_DIR) or not os.listdir(STORAGE_DIR):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(STORAGE_DIR, f"medical_records_{timestamp}.zip")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(STORAGE_DIR):
            filepath = os.path.join(STORAGE_DIR, file)
            if os.path.isfile(filepath) and not file.endswith('.zip'):
                zipf.write(filepath, file)
    
    return zip_filename


def get_storage_stats():
    """Get statistics about stored files."""
    ensure_directories()
    
    if not os.path.exists(STORAGE_DIR):
        return {
            "total_files": 0,
            "total_size_mb": 0
        }
    
    files = [f for f in os.listdir(STORAGE_DIR) if os.path.isfile(os.path.join(STORAGE_DIR, f)) and not f.endswith('.zip')]
    total_size = sum(os.path.getsize(os.path.join(STORAGE_DIR, f)) 
                    for f in files)
    
    # Count uploads and summaries
    uploads_count = len([f for f in files if not f.startswith('summary_')])
    summaries_count = len([f for f in files if f.startswith('summary_')])
    
    return {
        "total_files": len(files),
        "uploads_count": uploads_count,
        "summaries_count": summaries_count,
        "total_size_mb": total_size / (1024 * 1024)
    }
