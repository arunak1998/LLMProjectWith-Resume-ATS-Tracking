import base64
from urllib import response
from click import prompt
from dotenv import load_dotenv
load_dotenv()
import os
import io
import streamlit as st
import base64
import os
import pdf2image
from PIL import Image

import google.generativeai as genai


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def get_gemini_response(input,pdf_content,promt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],promt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Convert PDF to image
            images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path='C:\\Program Files\\poppler-24.02.0\\Library\\bin')
            
            # Extract the first page
            first_page = images[0]
            
            
            img_byte_array = io.BytesIO()
            first_page.save(img_byte_array, format='JPEG')
            img_byte_array = img_byte_array.getvalue()
            
            # Construct dictionary containing MIME type and base64-encoded image data
            pdf_part =[ {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_array).decode()
            }]
            
            return pdf_part
        except Exception as e:
            raise FileNotFoundError ("Filenot found")
    else:
        raise FileNotFoundError("File not uploaded")



####Streamlit app

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking Ststem")


input_text=st.text_area("Job Description: ",key="input")

uploaded_file=st.file_uploader("Uploade your resume(PDF)....",type=["PDF"])
if uploaded_file is not None:
    st.write("File Uploaded SUcessfully")



Submit1=st.button("Tell me about the Resume")
Submit2=st.button("How can I Improve My Skills")



Submit3=st.button("Percentahe Match")



input_promt1="""
Yor are an  Experienced HR with Tech Experience in the Field of Data Science ,Big Data Engineering and Data Analyst. Your task is to review the Provided Resume againtes the Job Description for the Profiles.
Please Share Your professional evaluvation on weather the Candidate Profile aligns with the Role
Highlight the Strength and weakness of the Applicamt in relation to the Specified job requirements.


"""

# input_promt2="""
# Yor are an  Technical HR manager with expertise  Data Science,,Big Data Engineering and Data Analyst.Your Role  is to review the Provided Resume againtes the Job Description for the Profiles.
# Please Share Your professional evaluvation on weather the Candidate Profile aligns with the Role
# Highlight the Strength and weakness of the Applicamt in relation to the Specified job requirements


# """


input_promt3="""
yor are skilld ATS (APPLICANT TRACKING SYSTEM) Scanner with a deep understanding of Data Science,,Big Data Engineering and Data Analyst and deep ATS functionality
your Task is to evalvuate the resume againts the Provided Job description give me the Percentage match if the resume matches wuth the job description.
first the output should come as percentage and then keywords missing and final thoghts.

"""



if Submit1:
    if uploaded_file is not None:
       pdf_format= input_pdf_setup(uploaded_file)
       result=get_gemini_response(input_text,pdf_format,input_promt1)
       st.subheader("The Response is ")
       st.write(result)
    else:
         st.write("Please submit PDF")



elif Submit3:
    if uploaded_file is not None:
       pdf_format= input_pdf_setup(uploaded_file)
       result=get_gemini_response(input_text,pdf_format,input_promt3)
       st.subheader("The Response is ")
       st.write(result)
    else:
     st.write("Please submit PDF")




