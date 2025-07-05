import streamlit as st
import tempfile
from PyPDF2 import PdfReader
import google.generativeai as genai
import re

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyDgfhEgHaeoq59HufC5L7fm4HFbrkg2jKo")

model = genai.GenerativeModel("models/gemini-1.5-flash")

def clean_output(text):
    return re.sub(r"\*+", "", text).strip()

def analyze_resume(text):
    prompt = f"""
You are an AI Resume Screener and Career Coach.

Analyze the following resume and return the result in plain text (no asterisks, no markdown). Follow this format exactly:

1. Resume Summary  
- Name:  
- Email:  
- Phone:  
- LinkedIn:  
- GitHub:  
- Skills:  
- Education:  
- Internships:  

2. Feedback for Improvement  
Give 4–5 bullet-style points (just hyphens, no stars)

3. Suggested Job Roles  
List 2–3 job roles ideal for the candidate's profile.

4. Skill Gap Recommender  
Suggest 3–5 skills, tools, or domains to learn further.

5. Resume Score (out of 100)  
Breakdown by:
- Technical Skills (out of 20)  
- Projects & Impact (out of 20)  
- Internship/Experience (out of 20)  
- Structure & Clarity (out of 20)  
- Keyword Optimization (out of 20)  

Also provide a one-line explanation for each sub-score based on the resume text.

Resume:
{text}
"""
    result = model.generate_content(prompt)
    return clean_output(result.text)

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# UI Design
st.set_page_config(page_title="AI Resume Screener", layout="centered")
st.title("AI Resume Screener")
st.markdown("Upload your **PDF resume**, and let the AI analyze it to give feedback, job suggestions, and section-wise scores.")

uploaded_file = st.file_uploader("📄 Upload your resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    try:
        with st.spinner("🔍 Extracting text from resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)

        with st.spinner("🧠 Analyzing with Gemini AI..."):
            analysis_result = analyze_resume(resume_text)

        st.success("✅ Analysis Complete!")
        st.text_area("📋 Resume Review Output", analysis_result, height=500)

        # Download .txt file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(analysis_result.encode("utf-8"))
            temp_file_path = temp_file.name

        with open(temp_file_path, "rb") as file:
            st.download_button(
                label="📥 Download as .txt",
                data=file,
                file_name="AI_Resume_Review.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
else:
    st.info("📝 Please upload a PDF resume to begin analysis.")
