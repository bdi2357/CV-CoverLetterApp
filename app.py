import streamlit as st
import openai
from docx import Document
import os

# Load the OpenAI API key from the Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

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

    # Use the OpenAI API to generate the cover letter
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can adjust this based on the GPT model you want to use
        prompt=prompt,
        max_tokens=500
    )

    # Extract the generated cover letter from the API response
    cover_letter = response.choices[0].text.strip()
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
        # Read the uploaded CV file content
        cv_text = uploaded_cv.getvalue().decode("utf-8")

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
