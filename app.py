import streamlit as st
from utils.file_manager import save_uploaded_file
from utils.model_integration import generate_documents
import os

# Streamlit app title and description
st.title('Cover Letter and Resume Generator')
st.write('Upload your CV and provide the job description to generate a tailored cover letter and resume.')

# File uploader for CV
uploaded_cv = st.file_uploader('Upload your CV (PDF or DOCX)', type=['pdf', 'docx'])

# Text area for job description
job_description = st.text_area('Paste the job description here', height=200)

# Checkboxes for options
generate_cover_letter = st.checkbox('Generate Cover Letter')
generate_resume = st.checkbox('Generate Tailored Resume')

# Button to trigger generation
if st.button('Generate'):
    if uploaded_cv is None or job_description.strip() == '':
        st.warning('Please upload your CV and enter a job description.')
    else:
        # Save the uploaded file to a temporary location
        cv_file_path = save_uploaded_file(uploaded_cv)

        # Generate the cover letter and/or tailored resume
        result = generate_documents(cv_file_path, job_description, generate_cover_letter, generate_resume)

        # Display download links if files are successfully generated
        if result['cover_letter']:
            st.success('Cover Letter generated successfully!')
            st.download_button(
                label='Download Cover Letter',
                data=open(result['cover_letter'], 'rb').read(),
                file_name='cover_letter.pdf',
                mime='application/pdf'
            )

        if result['resume']:
            st.success('Tailored Resume generated successfully!')
            st.download_button(
                label='Download Tailored Resume',
                data=open(result['resume'], 'rb').read(),
                file_name='tailored_resume.docx',
                mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
