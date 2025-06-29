# 📚 PDF to Study Guide Converter

A Streamlit application that converts PDF documents into organized study guides with AI-powered topic analysis, checklists, and repeated topic identification using Google's Gemini AI.

## ✨ Features

- **PDF Text Extraction**: Automatically extracts text from uploaded PDF files
- **AI-Powered Analysis**: Uses Gemini AI to identify topics, create study checklists, and find repeated concepts
- **Manual Fallback**: Includes regex-based topic extraction when AI is unavailable
- **Interactive UI**: Beautiful Streamlit interface with real-time progress tracking
- **Markdown Export**: Generates downloadable markdown study guides with checkboxes
- **Topic Frequency Analysis**: Identifies which topics appear multiple times for focused study

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Gemini API Key

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### 3. Run the Application

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 How to Use

1. **Upload PDF**: Click "Browse files" and select your PDF document
2. **Wait for Analysis**: The app will extract text and analyze topics
3. **Review Results**: Check the sidebar for topic count and analysis results
4. **Download Guide**: Click the download button to get your markdown study guide

## 🛠️ Technical Details

### Dependencies

- `streamlit`: Web application framework
- `google-generativeai`: Gemini AI integration
- `PyPDF2`: PDF text extraction
- `python-dotenv`: Environment variable management
- `pandas`: Data manipulation
- `markdown`: Markdown processing

### Architecture

- **Text Extraction**: Uses PyPDF2 to extract text from PDF files
- **AI Analysis**: Sends text to Gemini AI for topic identification and checklist generation
- **Fallback System**: Regex patterns for manual topic extraction when AI is unavailable
- **Markdown Generation**: Creates structured markdown with checkboxes and sections

### AI Prompt Structure

The application sends carefully crafted prompts to Gemini AI requesting:
- Comprehensive topic lists
- Actionable study checklists
- Repeated topic identification
- Topic frequency analysis

## 🎯 Use Cases

- **Students**: Convert textbooks and study materials into organized guides
- **Researchers**: Analyze research papers for key topics and concepts
- **Professionals**: Create study guides from technical documentation
- **Educators**: Generate structured learning materials from existing content

## 🔧 Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Your Gemini API key (required for AI features)

### Customization

You can modify the AI prompt in the `analyze_topics_with_gemini()` function to customize the analysis output format.

## 📝 Output Format

The generated markdown includes:

```markdown
# Document Name - Study Guide

## 📚 Document Analysis Summary
[AI-generated analysis or manual topic list]

## 📋 Study Progress Tracker
### Overall Progress
- [ ] Review all topics
- [ ] Complete practice questions
- [ ] Create summary notes

### Topic Mastery Checklist
#### Topic Name
- [ ] Read and understand the concept
- [ ] Take notes
- [ ] Practice related questions
- [ ] Review and revise

## 🔄 Repeated Topics (Focus Areas)
[Topics that appear multiple times]
```

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License. 