# 🏥 Medical Records Summarization

A beautiful, advanced Streamlit application for summarizing medical records using Google's Gemini AI API. This application provides an intuitive interface for healthcare professionals to quickly analyze and summarize medical documents.

## ✨ Features

- **📤 Advanced File Upload**: Support for PDF and TXT files with drag-and-drop interface
- **🎨 Beautiful UI**: Modern, gradient-based design with smooth animations
- **⚡ Real-time Processing**: Fast document analysis with progress indicators
- **📊 Statistics Dashboard**: View processing stats including character count and processing time
- **💾 Download Summaries**: Export summaries as text files
- **🔒 Privacy-Focused**: All processing done in-memory, no data storage
- **📱 Responsive Design**: Works on desktop and tablet devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /root/shahid
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

## 📖 Usage

1. **Upload a Medical Record:**
   - Click the upload area or use the file uploader
   - Supported formats: PDF, TXT
   - Maximum file size: 10MB

2. **Preview Extracted Text:**
   - Optionally preview the extracted text before summarization

3. **Generate Summary:**
   - Click the "Generate Summary" button
   - Watch the progress indicator as the AI processes your document

4. **Review Results:**
   - View the comprehensive summary in the right panel
   - Check processing statistics
   - Download the summary if needed

## 🏗️ Project Structure

```
medical-records-summarization/
├── app.py                 # Main Streamlit application
├── gemini_service.py      # Gemini API integration
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Configuration

Edit `config.py` to customize:

- **Model Settings**: Change the Gemini model (default: `gemini-pro`)
- **Temperature**: Adjust creativity (default: 0.3 for more focused summaries)
- **Max Tokens**: Control summary length (default: 2000)
- **File Size Limit**: Maximum upload size (default: 10MB)

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Google Gemini AI**: AI model for summarization
- **PyPDF2**: PDF text extraction
- **python-dotenv**: Environment variable management

## 🔒 Privacy & Security

- All file processing is done in-memory
- No data is stored on disk or servers
- API calls are made securely to Google's servers
- Your API key is stored locally in `.env` file (never commit this!)

## 📝 License

This project is open source and available for use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Important Notes

- This application is for demonstration purposes
- Always verify AI-generated summaries with medical professionals
- Ensure compliance with HIPAA and local medical data regulations
- Keep your API key secure and never share it publicly

## 🆘 Troubleshooting

**Issue: "GEMINI_API_KEY not found"**
- Make sure you've created a `.env` file with your API key
- Check that the `.env` file is in the project root directory

**Issue: "Error extracting text from PDF"**
- Ensure the PDF is not password-protected
- Try converting to TXT format if issues persist

**Issue: "Error generating summary"**
- Verify your API key is valid and has sufficient quota
- Check your internet connection
- Try with a smaller document first

## 📞 Support

For issues or questions, please open an issue on the repository.

---

Made with ❤️ for healthcare professionals
