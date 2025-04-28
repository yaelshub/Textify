from PyPDF2 import PdfReader
from services.File_analysis.tokenization import tokenize_text

def extract_text_from_pdf(file_stream):
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
