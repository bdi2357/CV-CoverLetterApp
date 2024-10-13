from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="CV-CoverLetterApp",  # Your project's name
    version="0.1.0",  # Initial version number
    author="Your Name",  # Replace with your name or your organization
    author_email="your.email@example.com",  # Replace with your email
    description="A Streamlit app for generating AI-powered cover letters and tailored resumes using the CoverLetterGen API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/CV-CoverLetterApp",  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.25.0",
        "openai",  # Updated to the latest version to match your code requirements
        "python-docx>=0.8.11",
        "reportlab>=3.6.13",
        "requests>=2.31.0",
        "PyYAML>=6.0",
        "python-dotenv>=1.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'coverletter-app=app:main',  # Optional: CLI entry point to run your Streamlit app
        ],
    },
)
