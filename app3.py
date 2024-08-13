from dotenv import load_dotenv
import openai
load_dotenv()

from openai import OpenAI
import streamlit as st
import os
import PyPDF2 as pdf


def extract_information_from_cv(resume_text):
    prompt = """
            You are an AI bot expert in extracting information from resumes. You are given the text of the resume of a candidate. Your task is to extract the below information from the resume and store it in JSON format. An example JSON output is given. Avoid the section if the information is not available in resume.

            Name: 
            Contact Information: 
            Skills: 
            Work Experience: 
            Education: 
            Skills:
            Projects: 

            Please provide the extracted details in JSON format.
            Output:
            {
            "Name": "",
            "Contact Information": {
                "Email": "",
                "Phone": "",
                "Address": ""
            },
            "Skills": {
                "Technical Skills": [],
                "Soft Skills": [],
                "Tools": []
            },
            "Education": [
                {
                "Degree": "",
                "Institution": "",
                "Location": "",
                "Graduation Date": ""
                }
            ],
            "Projects": [
                {
                "Project Name": "",
                "Description": "",
                "Technologies Used": "",
                "Role": ""
                }
            ],
            "Work Experience": [
                {
                "Job Title": "",
                "Company": "",
                "Location": "",
                "Dates": "",
                "Responsibilities": ""
                }
            ]
            }
            """
    
    messages = [{"role":"system","content":prompt},{"role":"user","content":resume_text}]
    
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    output = response.choices[0].message.content
    return output


def pdf_to_text(pdf_file):
    pdfReader = pdf.PdfReader(pdf_file)
    text = ''
    for page in range(len(pdfReader.pages)):
        page = pdfReader.pages[page] 
        text += str(page.extract_text())
    return text
    

## streamlit app
st.title("Smart ATS - OPEN-AI")
st.text("Improve Your Resume ATS")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text=pdf_to_text(uploaded_file)
        response=extract_information_from_cv(resume_text)
        st.write(response)