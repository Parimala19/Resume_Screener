
import streamlit as st
import tempfile
from PyPDF2 import PdfReader
import google.generativeai as genai
import re

st.set_page_config(page_title="AI Resume Screener", layout="centered")

# 💄 Custom CSS for background and card
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #ddeeff, #ffffff);
        font-family: 'Segoe UI', sans-serif;
    }
    .card {
        background-color: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        margin-top: 30px;
    }
    .stButton > button, .stDownloadButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.5rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Use container so everything stays inside the card
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # 🎯 Title and description INSIDE the card
    st.markdown("<h2 style='text-align:center;'>AI Resume Screener</h2>", unsafe_allow_html=True)
    st.markdown("Upload your PDF resume, choose a Gemini model, and get AI-powered resume feedback and score.")

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyDgfhEgHaeoq59HufC5L7fm4HFbrkg2jKo")

# Fetch supported models
@st.cache_data
def get_supported_models():
    models = genai.list_models()
    return [m.name for m in models if 'generateContent' in m.supported_generation_methods]

model_list = get_supported_models()
selected_model = st.selectbox("Select Gemini Model", model_list, index=model_list.index("models/gemini-1.5-flash"))

# Clean up asterisks or markdown
def clean_output(text):
    return re.sub(r"\*+", "", text).strip()

# Analyze resume using selected Gemini model
def analyze_resume(text, selected_model):
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
    model = genai.GenerativeModel(selected_model)
    result = model.generate_content(prompt)
    return clean_output(result.text)

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# UI
st.title("AI Resume Screener")
st.markdown("Upload your **PDF resume**, choose a Gemini model, and get AI-powered resume feedback and score.")

uploaded_file = st.file_uploader("📄 Upload Resume PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        with st.spinner("📃 Reading your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)

        with st.spinner(f"🧠 Analyzing with Gemini Model: `{selected_model}`..."):
            analysis_result = analyze_resume(resume_text, selected_model)

        st.success("✅ Resume analyzed successfully!")

        # Display output with spacing
        sections = analysis_result.split("\n\n")
        st.markdown("Resume Review Output")
        for section in sections:
            st.markdown(section.strip())
            st.markdown(" ")

        # TXT Download
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
    st.info("📝 Please upload your resume in PDF format.")
st.markdown("</div>", unsafe_allow_html=True)
