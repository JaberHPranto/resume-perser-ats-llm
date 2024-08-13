from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    # model = genai.GenerativeModel('gemini-pro')
    model = genai.GenerativeModel('gemini-1.5-flash',generation_config={"response_mime_type": "application/json"})
    response = model.generate_content(input)
    return response.text

# Extracting Text from PDF
def pdf_to_text(pdf_file):
    pdfReader = pdf.PdfReader(pdf_file)
    text = ''
    for page in range(len(pdfReader.pages)):
        page = pdfReader.pages[page] 
        text += str(page.extract_text())
    return text
    
input_prompt="""
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Software Engineering area (Full Stack Developer, Frontend Developer, Backend Developer, Devops, etc). You have a good understanding of deep ATS functionality. Your task is to evaluate the resume against the job description for this profile. Give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and at finally share share your final thoughts about the candidate.
Assign the percentage Matching based on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=pdf_to_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.write(response)