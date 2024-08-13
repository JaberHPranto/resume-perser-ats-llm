import base64
import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
   
def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash',generation_config={"response_mime_type": "application/json"})
    response = model.generate_content([input,pdf_content[0],prompt])
    return response

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        ## Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        ## encode bytes to base64
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode(), 
            }
        ]

        return pdf_parts
    else:
        raise Exception("No file uploaded")

## Streamlit App
st.set_page_config(page_title="ATS Resume Perser", page_icon="📄")
st.header("Resume Parser")
input_text = st.text_area("Enter Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload Resume", type="pdf")

if uploaded_file is not None:
    st.write("File uploaded successfully")

submit1 = st.button("Tell me about your resume")
submit2 = st.button("Percentage Match")

input_prompt1 = """ 
You are an experienced HR with Technical Experience in the field of Software Engineering area (Full Stack Developer, Frontend Developer, Backend Developer, Devops, etc). Your task is to review the provided resume against the job description for this profile.
Please share your professional evaluation on whether the candidate is a good fit for the position. Highlight the strengths and weaknesses of the candidate in relation to the specific job description.
"""
input_prompt2 = """ 
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Software Engineering area (Full Stack Developer, Frontend Developer, Backend Developer, Devops, etc). You have a good understanding of deep ATS functionality. Your task is to evaluate the resume against the job description for this profile. Give me the percentage of match if the resume matches the job description. First the output should come as percentage and then keywords missing and at finally share share your final thoughts about the candidate.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is...")
        st.write(response.text)
    else:
        st.write("Please upload your resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text,pdf_content,input_prompt2)
        st.subheader("The Response is...")
        st.write(response.text)
    else:
        st.write("Please upload your resume")
     

