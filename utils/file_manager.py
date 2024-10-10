import os

def save_uploaded_file(uploaded_file):
    """
    Saves the uploaded file to a temporary directory.

    Parameters:
        uploaded_file (UploadedFile): The file uploaded by the user via the Streamlit app.

    Returns:
        str: The file path where the uploaded file is saved.
    """
    temp_dir = 'temp_cv'
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)

    # Save the uploaded file to the temporary directory
    with open(file_path, 'wb') as file:
        file.write(uploaded_file.read())

    return file_path
