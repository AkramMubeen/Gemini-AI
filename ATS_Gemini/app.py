import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def pdf_to_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template

input_prompt = """
Pretend to be an ATS (Application Tracking System) expert, proficient in job domains such as technology, marketing, finance, and design.  
Your role is crucial in evaluating resumes against specific job descriptions. 
Given the intense competition in the job market, your objective is to provide precise assistance in resume enhancement. 
Assign percentage matching scores based on the job description and the resume, accurately identify missing keywords between the job description and the resume, 
and succinctly summarize the resume profile in accordance with the job description.

Here is the job description: {}
And here is the resume: {}

Please structure your response as follows:
{{"Job Description Match":"Percentage", "MissingKeywords":["Keyword1","Keyword2",...], "Profile Summary":"SummaryText"}}
"""

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://ibb.co/NZq817h");
    }
   </style>
    """,
    unsafe_allow_html=True
)

st.title("AI Powered ATS")
st.text("Upgrade your Resume")
job_desc = st.text_area("Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Upload your resume PDF here.")
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = pdf_to_text(uploaded_file)
        formatted_prompt = input_prompt.format(json.dumps(job_desc), json.dumps(text))
        response_text = response(formatted_prompt)
        st.subheader(response_text)
