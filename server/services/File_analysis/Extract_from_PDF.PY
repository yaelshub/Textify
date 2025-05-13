from PyPDF2 import PdfReader

def extract_text_from_pdf(file_stream):
    try:
        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print("שגיאה בקריאת ה-PDF:", e)
    return text
