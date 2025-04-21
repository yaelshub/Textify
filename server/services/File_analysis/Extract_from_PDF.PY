import PyPDF2
from flask import Blueprint, jsonify


pdf_bp = Blueprint('pdf', __name__)

@pdf_bp.route("/extract_text_from_pdf")
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

pdf_path = 'file:///D:/Textify/server/dal/textData/A-Little-Princess-By-Frances-Hodgson-Burnett-Retold-by-Jennifer-Bassett-Book-PDF.pdf'  # שימי את הנתיב של הקובץ שלך כאן
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)