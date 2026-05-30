"""
Script to create a zip file of the complete project for sharing.
Excludes unnecessary files like venv, __pycache__, etc.
"""
import os
import zipfile
from datetime import datetime

# Files and folders to exclude
EXCLUDE_PATTERNS = [
    '__pycache__',
    '.pyc',
    '.pyo',
    '.pyd',
    'venv',
    'env',
    '.env',
    'medical_records',
    'uploads',
    'summaries',
    '.git',
    '__pycache__',
    '*.pyc',
    '.DS_Store',
    'Thumbs.db',
    '.streamlit',
]

# Files to include (will be added explicitly)
INCLUDE_FILES = [
    'app.py',
    'config.py',
    'gemini_service.py',
    'file_storage.py',
    'requirements.txt',
    'README.md',
    'env.example',
    '.gitignore',
]

def should_exclude(filepath):
    """Check if file should be excluded from zip."""
    for pattern in EXCLUDE_PATTERNS:
        if pattern in filepath:
            return True
    return False

def create_project_zip():
    """Create a zip file of the complete project."""
    # Get current directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    if not project_dir:
        project_dir = os.getcwd()
    
    # Create zip filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"medical_records_summarization_{timestamp}.zip"
    
    # Create zip file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # First, add all files from root directory
        for file in os.listdir(project_dir):
            filepath = os.path.join(project_dir, file)
            
            # Skip directories
            if os.path.isdir(filepath):
                continue
            
            # Skip excluded files (but allow .gitignore and env.example)
            if should_exclude(filepath) and file not in ['.gitignore', 'env.example']:
                continue
            
            # Skip the zip file itself
            if filepath.endswith('.zip'):
                continue
            
            # Add file to zip
            try:
                zipf.write(filepath, file)
                print(f"Added: {file}")
            except Exception as e:
                print(f"Error adding {file}: {str(e)}")
        
        # Also check for any Python files in subdirectories (excluding venv, etc.)
        for root, dirs, files in os.walk(project_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
            
            for file in files:
                filepath = os.path.join(root, file)
                
                # Skip excluded files
                if should_exclude(filepath):
                    continue
                
                # Skip the zip file itself
                if filepath.endswith('.zip'):
                    continue
                
                # Get relative path for zip
                arcname = os.path.relpath(filepath, project_dir)
                
                # Skip if already added (root level files)
                if arcname == file:
                    continue
                
                # Add file to zip
                try:
                    zipf.write(filepath, arcname)
                    print(f"Added: {arcname}")
                except Exception as e:
                    print(f"Error adding {arcname}: {str(e)}")
    
    # Get file size
    file_size = os.path.getsize(zip_filename) / (1024 * 1024)  # Size in MB
    
    print(f"\n✅ Project zip created successfully!")
    print(f"📦 File: {zip_filename}")
    print(f"📊 Size: {file_size:.2f} MB")
    print(f"📍 Location: {os.path.abspath(zip_filename)}")
    
    return zip_filename

if __name__ == "__main__":
    create_project_zip()
