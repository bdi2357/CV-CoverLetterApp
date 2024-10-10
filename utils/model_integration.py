import os
from CoverLetterGen.main import main as generate_from_model

def generate_documents(cv_file_path, job_description, generate_cover_letter, generate_resume):
    """
    Generates a cover letter and/or tailored resume using the CoverLetterGen module.

    Parameters:
        cv_file_path (str): Path to the uploaded CV file.
        job_description (str): Job description provided by the user.
        generate_cover_letter (bool): Whether to generate a cover letter.
        generate_resume (bool): Whether to generate a tailored resume.

    Returns:
        dict: A dictionary containing the paths to the generated cover letter and resume files.
    """
    output_dir = 'Output'
    os.makedirs(output_dir, exist_ok=True)
    results = {'cover_letter': None, 'resume': None}

    # Call the CoverLetterGen module only if at least one document needs to be generated
    if generate_cover_letter or generate_resume:
        generate_from_model(cv_file_path, job_description)

    if generate_cover_letter:
        results['cover_letter'] = os.path.join(output_dir, 'cover_letter.pdf')
    if generate_resume:
        results['resume'] = os.path.join(output_dir, 'tailored_resume.docx')

    return results
