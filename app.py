import streamlit as st
import os
from openai import OpenAI
from docx import Document
from PyPDF2 import PdfReader

# Load the OpenAI API key from the Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

def generate_cover_letter(cv_text, job_description):
    """
    Generates a cover letter using GPT model based on the provided CV and job description.

    Parameters:
        cv_text (str): The text extracted from the user's CV.
        job_description (str): The job description entered by the user.

    Returns:
        str: The generated cover letter text.
    """
    prompt = f"""
    Based on the following CV and job description, generate a professional cover letter tailored to the job description:

    CV:
    {cv_text}

    Job Description:
    {job_description}

    The cover letter should be concise, professional, and highlight relevant experience and skills.
    """

    # Use the OpenAI chat-based API to generate the cover letter
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can change this to gpt-4 if needed
        messages=[
            {
                "role": "system",
                "content": "You are a professional assistant generating cover letters based on CV and job descriptions.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    # Extract the generated cover letter from the API response
    cover_letter = completion.choices[0].message.content
    return cover_letter

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
st.title('AI Cover Letter Generator')

# File uploader for CV (PDF or DOCX)
uploaded_cv = st.file_uploader('Upload your CV (PDF or DOCX)', type=['pdf', 'docx'])

# Text area for job description
job_description = st.text_area('Paste the job description here', height=200)

# Button to generate cover letter
if st.button('Generate Cover Letter'):
    if uploaded_cv is None or job_description.strip() == '':
        st.warning('Please upload your CV and enter a job description.')
    else:
        # Detect file type and extract text accordingly
        file_type = uploaded_cv.type
        if file_type == "application/pdf":
            cv_text = extract_text_from_pdf(uploaded_cv)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            cv_text = extract_text_from_docx(uploaded_cv)

        # Generate the cover letter using the CV and job description
        cover_letter = generate_cover_letter(cv_text, job_description)

        # Save the cover letter as a DOCX file
        docx_file_path = save_cover_letter_to_docx(cover_letter, "cover_letter.docx")

        # Display the cover letter to the user
        st.success('Cover Letter generated successfully!')
        st.download_button(
            label='Download Cover Letter',
            data=open(docx_file_path, 'rb').read(),
            file_name='cover_letter.docx',
            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
