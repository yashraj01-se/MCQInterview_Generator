from setuptools import find_packages, setup

setup(
    name='MCQInterview_Generator',
    version='0.0.1',
    author='Yashraj Sharma',
    author_email='yashsharma000098@gmail.com',
    install_requires=[
        "google-generativeai",        
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    packages=find_packages()
)
