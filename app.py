import streamlit as st
import os
from docx import Document
from PyPDF2 import PdfReader
import openai

import logging
##
import os
from  openai import OpenAI
from CoverLetterGen.ai_interaction import OpenAIModel, CoverLetterGenerator
#from CoverLetterGen.basic_itera tive import BasicIterativeAgent
from CoverLetterGen.cover_letter_wrapper import wrap_cover_letter_generation
from CoverLetterGen.parsing_cv_to_dict import CVParserAI
api_key =  st.secrets["OPENAI_API_KEY"]
openai.api_key = api_key

import os
import streamlit as st

def save_uploaded_file(uploaded_file, save_directory="uploads"):
    """
    Saves the uploaded file to a specific directory based on its type.

    :param uploaded_file: Streamlit UploadedFile object.
    :param save_directory: Base directory to save files. Default is "uploads".
    :return: Full path of the saved file or None if the file type is unsupported.
    """
    if uploaded_file is None:
        st.warning("No file uploaded.")
        return None

    # Extract the file name and extension
    file_name = uploaded_file.name
    file_extension = file_name.split('.')[-1].lower()

    # Prepare subdirectories based on file type
    file_type_directories = {
        "images": ['jpg', 'jpeg', 'png'],
        "texts": ['txt', 'csv'],
        "videos": ['mp4', 'avi'],
        "doc": ['pdf','docx']
    }

    sub_directory = None
    for directory, extensions in file_type_directories.items():
        if file_extension in extensions:
            sub_directory = directory
            break

    if not sub_directory:
        st.warning("Unsupported file type. Please upload an image, text, or video file.")
        return None

    # Full path for saving
    save_path = os.path.join(save_directory, sub_directory)
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, file_name)

    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved to {file_path}")
    return file_path


import requests



#ai_model = OpenAIModel(api_key= api_key, model_name='gpt-4o')

#cover_letter_gen = CoverLetterGenerator(ai_model)
#agent = BasicIterativeAgent(cover_letter_gen)


def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    """Extracts text from a DOCX file."""
    doc = Document(docx_file)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

def save_cover_letter_to_docx(cover_letter_text, file_name):
    """
    Saves the generated cover letter as a DOCX file.

    Parameters:
        cover_letter_text (str): The generated cover letter text.
        file_name (str): The name of the DOCX file to save.
    """
    doc = Document()
    doc.add_paragraph(cover_letter_text)
    os.makedirs("Output", exist_ok=True)
    file_path = os.path.join("Output", file_name)
    doc.save(file_path)
    return file_path

# Streamlit UI components
st.title('📄 AI Cover Letter Generator')

st.write("Upload your CV and paste the job description to generate a professional cover letter.")
st.write("")

# File uploader for CV (PDF or DOCX)
uploaded_cv = st.file_uploader('📁 Upload your CV (PDF or DOCX)', type=['pdf', 'docx'])

# Text area for job description
job_description = st.text_area('✍️ Paste the job description here:', height=200)

if uploaded_cv:
    cv_saved_path = save_uploaded_file(uploaded_cv, save_directory="uploads")
    """
    if saved_path:
        st.write(f"File saved successfully at: {saved_path}")
    """

# Button to generate cover letter
if st.button('Generate Cover Letter'):
    if uploaded_cv is None or job_description.strip() == '':
        st.warning('⚠️ Please upload your CV and enter a job description.')
    else:
        st.info("✍️ Generating your cover letter... Please wait.")

        # Detect file type and extract text accordingly
        file_type = uploaded_cv.type
        if file_type == "application/pdf":
            cv_text = extract_text_from_pdf(uploaded_cv)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            cv_text = extract_text_from_docx(uploaded_cv)

        # Generate initial cover letter using BasicIterativeAgent


        #cover_letter = agent.generate_cover_letter(cv_text, job_description)

        # Optionally improve the generated cover letter
        #improved_cover_letter, final_critique = agent.improve_cover_letter(cv_text, cover_letter, job_description)
        parser = CVParserAI(OpenAI(api_key=api_key))
        ai_model = OpenAIModel(api_key=api_key, model_name='gpt-4o')
        print(type(uploaded_cv))
        #print("*"*70 +"\n" + uploaded_cv +"\n" +"*"*70)
        print(cv_saved_path)
        output_path,critique_cover_file_path = wrap_cover_letter_generation(cv_saved_path, job_description, ai_model, parser, method='basic')
        # Save the improved cover letter as a DOCX file
        #docx_file_path = save_cover_letter_to_docx(improved_cover_letter, "cover_letter.docx")
        #critique_cover_file_path = save_cover_letter_to_docx(final_critique, "cover_letter_critique.docx")

        st.session_state.output_path = output_path
        st.session_state.critique_cover_file_path = critique_cover_file_path
        # Display the cover letter to the user
        st.success('✅ Cover Letter generated successfully!')
        print(output_path)
        print("st.session_state.output_path", st.session_state.output_path)
        print("st.session_state.critique_cover_file_path",st.session_state.critique_cover_file_path)

if "output_path" not in st.session_state:
    st.session_state.output_path = None
if "critique_cover_file_path" not in st.session_state:
    st.session_state.critique_cover_file_path = None

if st.session_state.output_path and st.session_state.critique_cover_file_path:
    with open(st.session_state.output_path, 'rb') as f:
        st.download_button(
            label='📥 Download Cover Letter',
            #data=open(docx_file_path, 'rb').read(),
            data=f.read(),
            file_name='cover_letter.docx',
            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        print("H1")
    with open(st.session_state.critique_cover_file_path, 'rb') as f:
        st.download_button(
            label='📥 Download Cover Letter Critique',
            data=f.read(),
            file_name='cover_letter_critique.docx',
            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        print("H2")
