from fastapi import UploadFile
from fastapi.responses import FileResponse
import PyPDF2
import aspose.words as aw
from docx import Document
from io import BytesIO
import generate_summary

def summary_generator(file: UploadFile):
    inputText = extract_text(file)
    summary = generate_summary.summarize(inputText)
    return summary

def extract_text(file: UploadFile):
    inputText = ""
    f = file.file
    f.seek(0)
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        inputText += page.extract_text()
    return inputText