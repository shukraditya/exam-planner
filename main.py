import streamlit as st
from google import genai
import PyPDF2
import os
import re
from collections import Counter
import pandas as pd
from dotenv import load_dotenv
import markdown
import io

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    client = genai.Client(api_key=GOOGLE_API_KEY)
else:
    st.error("Please set GOOGLE_API_KEY in your environment variables or .env file")

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def chunk_text(text, chunk_size=6000, overlap=500):
    """Split text into overlapping chunks for processing"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        
        if start >= len(text):
            break
    
    return chunks

def analyze_chunk_with_gemini(chunk, chunk_num, total_chunks, pdf_name):
    """Analyze a single chunk with Gemini"""
    if not GOOGLE_API_KEY:
        return None
    
    try:
        prompt = f"""
        You are analyzing chunk {chunk_num} of {total_chunks} from the PDF "{pdf_name}".
        
        Extract ALL topics, subtopics, and concepts from this text chunk. Focus on:
        1. Main topics and their subtopics
        2. Key concepts and terms
        3. Important definitions
        4. Any numbered or bulleted items
        5. Chapter/section titles
        
        Text chunk to analyze:
        {chunk}
        
        Provide your response in this EXACT format:
        
        ## TOPICS_FOUND:
        - Topic 1
        - Topic 2
        - Subtopic 1.1
        - Subtopic 1.2
        - Concept A
        - Concept B
        
        ## KEY_TERMS:
        - Term 1: brief description
        - Term 2: brief description
        
        ## IMPORTANT_POINTS:
        - Point 1
        - Point 2
        
        Be comprehensive and extract everything that could be a study topic or concept.
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        st.error(f"Error analyzing chunk {chunk_num}: {str(e)}")
        return None

def combine_and_analyze_topics(all_chunk_results, pdf_name):
    """Combine all chunk results and analyze overall topics with frequency"""
    if not GOOGLE_API_KEY:
        return None
    
    try:
        # Combine all extracted topics
        combined_text = "\n\n".join(all_chunk_results)
        
        prompt = f"""
        You have analyzed the entire PDF "{pdf_name}" in chunks. Here are all the extracted topics and concepts:

        {combined_text}

        Now provide a comprehensive analysis with the following EXACT format:

        ## COMPLETE_TOPIC_ANALYSIS:
        ### Main Topics (with frequency estimates):
        - Topic 1 (estimated frequency: X mentions)
        - Topic 2 (estimated frequency: Y mentions)
        - Topic 3 (estimated frequency: Z mentions)

        ### Subtopics and Concepts:
        - Subtopic 1.1 (frequency: A mentions)
        - Subtopic 1.2 (frequency: B mentions)
        - Concept A (frequency: C mentions)
        - Concept B (frequency: D mentions)

        ## FREQUENCY_CATEGORIZATION:
        ### High Frequency Topics (5+ mentions) - Critical for Study:
        - Topic A: X mentions
        - Topic B: Y mentions

        ### Medium Frequency Topics (2-4 mentions) - Important:
        - Topic C: Z mentions
        - Topic D: A mentions

        ### Low Frequency Topics (1 mention) - Supplementary:
        - Topic E: 1 mention
        - Topic F: 1 mention

        ## STUDY_CHECKLIST:
        ### High Priority Study Items:
        - [ ] Topic A - Master thoroughly (X mentions)
        - [ ] Topic B - Practice extensively (Y mentions)

        ### Medium Priority Study Items:
        - [ ] Topic C - Understand well (Z mentions)
        - [ ] Topic D - Review carefully (A mentions)

        ### Low Priority Study Items:
        - [ ] Topic E - Basic understanding (1 mention)
        - [ ] Topic F - Quick review (1 mention)

        ## REPEATED_CONCEPTS:
        - Concept X appears in multiple sections
        - Concept Y is mentioned throughout the document

        ## STUDY_STRATEGY:
        - Focus 70% of time on high-frequency topics
        - Spend 25% of time on medium-frequency topics
        - Allocate 5% of time to low-frequency topics
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        st.error(f"Error in final analysis: {str(e)}")
        return None

def create_markdown_from_ai_analysis(analysis_result, pdf_name):
    """Create markdown output from AI analysis"""
    if not analysis_result:
        return "Error: No analysis result available"
    
    markdown_content = f"""# {pdf_name} - Study Guide

## 📚 AI-Generated Study Guide

This document has been comprehensively analyzed using Gemini AI to create a detailed study guide with topic frequency analysis and prioritized study recommendations.

---

{analysis_result}

---

## 📋 Study Progress Tracker

### Overall Progress
- [ ] Review high-frequency topics first
- [ ] Complete medium-frequency topics
- [ ] Review low-frequency topics
- [ ] Create summary notes
- [ ] Practice with focus on repeated concepts

### Daily Study Plan
- [ ] Morning: Focus on high-priority topics
- [ ] Afternoon: Review medium-priority topics
- [ ] Evening: Quick review of low-priority topics

---

*Generated by PDF Study Guide Generator with Gemini AI*
"""
    
    return markdown_content

def main():
    st.set_page_config(
        page_title="PDF to Study Guide Converter",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 PDF to Study Guide Converter")
    st.markdown("Convert your PDF documents into comprehensive study guides using AI-powered analysis")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        if not GOOGLE_API_KEY:
            st.warning("⚠️ Gemini API key not found")
            st.info("Please set GOOGLE_API_KEY in your environment variables")
            st.stop()
        
        st.markdown("---")
        st.markdown("### How to use:")
        st.markdown("1. Upload your PDF file")
        st.markdown("2. AI will analyze in chunks")
        st.markdown("3. Get comprehensive study guide")
        st.markdown("4. Download the markdown file")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📄 Upload PDF")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF document to convert into a study guide"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Extract text from PDF
            with st.spinner("Extracting text from PDF..."):
                pdf_text = extract_text_from_pdf(uploaded_file)
            
            if pdf_text:
                st.info(f"📊 Extracted {len(pdf_text)} characters of text")
                
                # Chunk the text
                chunks = chunk_text(pdf_text)
                st.info(f"📑 Split into {len(chunks)} chunks for analysis")
                
                # Analyze each chunk
                all_chunk_results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, chunk in enumerate(chunks):
                    status_text.text(f"Analyzing chunk {i+1} of {len(chunks)}...")
                    with st.spinner(f"🤖 Analyzing chunk {i+1}/{len(chunks)}"):
                        result = analyze_chunk_with_gemini(chunk, i+1, len(chunks), uploaded_file.name)
                        if result:
                            all_chunk_results.append(result)
                    progress_bar.progress((i + 1) / len(chunks))
                
                if all_chunk_results:
                    st.success(f"✅ Successfully analyzed {len(all_chunk_results)} chunks")
                    
                    # Combine and analyze all results
                    with st.spinner("🔍 Combining analysis and creating final study guide..."):
                        final_analysis = combine_and_analyze_topics(all_chunk_results, uploaded_file.name)
                    
                    if final_analysis:
                        st.success("✅ Final analysis completed!")
                        
                        # Generate markdown
                        markdown_output = create_markdown_from_ai_analysis(final_analysis, uploaded_file.name)
                        
                        # Display preview
                        st.header("📖 Generated Study Guide Preview")
                        st.markdown("---")
                        st.markdown(markdown_output[:3000] + "..." if len(markdown_output) > 3000 else markdown_output)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Markdown Study Guide",
                            data=markdown_output,
                            file_name=f"{uploaded_file.name.replace('.pdf', '')}_study_guide.md",
                            mime="text/markdown"
                        )
                    else:
                        st.error("❌ Failed to create final analysis")
                else:
                    st.error("❌ No chunks were successfully analyzed")
    
    with col2:
        st.header("📊 Analysis Progress")
        
        if 'chunks' in locals():
            st.subheader("📑 Processing Status")
            st.markdown(f"- **Total Chunks**: {len(chunks)}")
            if 'all_chunk_results' in locals():
                st.markdown(f"- **Analyzed**: {len(all_chunk_results)}")
                st.markdown(f"- **Success Rate**: {len(all_chunk_results)/len(chunks)*100:.1f}%")
        
        st.markdown("---")
        st.markdown("### 💡 AI Analysis Features")
        st.markdown("- **Chunk-based processing** for large documents")
        st.markdown("- **Comprehensive topic extraction**")
        st.markdown("- **Frequency-based categorization**")
        st.markdown("- **Smart study recommendations**")
        st.markdown("- **Repeated concept identification**")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        Made with ❤️ using Streamlit and Gemini AI
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
