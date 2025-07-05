import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# ✅ Your Gemini API Key (keep private!)
genai.configure(api_key="AIzaSyDgfhEgHaeoq59HufC5L7fm4HFbrkg2jKo")  # Replace with your key

# Page config
st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("📄 AI Resume Screener + Scorer")
st.caption("Built using Gemini | By Parimala Tejaswi")

# Step 1: Get Gemini models
available_models = [
    m.name for m in genai.list_models()
    if "generateContent" in m.supported_generation_methods
]

selected_model = st.selectbox("Choose a Gemini Model", available_models)
model = genai.GenerativeModel(selected_model)

# Step 2: Upload resume
uploaded_file = st.file_uploader("Upload Resume (.pdf or .txt)", type=["pdf", "txt"])

def generate_resume_output(text):
    prompt = f"""
You are an AI Resume Screener and Career Coach.

Analyze the resume text below and return the following sections in clean plain text:

1. Resume Summary: Name, Email, Phone, Skills, Education, Internships.

2. Feedback for Improvement: Give 4-5 specific suggestions.

3. Suggested Job Roles: Recommend 1-2 suitable roles.

4. Skill Gap Recommender: Suggest 3-5 tools/skills to become an AI/ML Engineer.

5. Resume Score (out of 100): 
Give scores for:
- Technical Skills (20)
- Projects & Impact (20)
- Experience (20)
- Structure & Clarity (20)
- Keyword Relevance (20)
Add a brief reason for each, and then total score.
    
Resume:
{text}
"""
    response = model.generate_content(prompt)
    return response.text

# Step 3: Run if resume is uploaded
if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1]

    if file_ext == "pdf":
        reader = PdfReader(uploaded_file)
        resume_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    if st.button("🔍 Analyze Resume"):
        with st.spinner("Thinking..."):
            result = generate_resume_output(resume_text)
            st.text_area("✅ Output", result, height=600)
