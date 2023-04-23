from fastapi import UploadFile
from fastapi.responses import FileResponse
import PyPDF2
import aspose.words as aw
from docx import Document
from io import BytesIO
import generate_summary

def summary_generator(file: UploadFile):
    inputText = extract_text(file)
    print(inputText)
    summary = generate_summary.summarize(inputText)
    print("\nDone with generate_summary function in crud\n")
    return summary

def extract_text(file: UploadFile):
    inputText = ""
    print("generating summary of ", file.filename)
    f = file.file
    f.seek(0)
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        inputText += page.extract_text()
    return inputText