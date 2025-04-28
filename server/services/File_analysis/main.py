from extract_from_PDF import extract_text_from_pdf
from tokenization import tokenize_text
def main():
    text=extract_text_from_pdf(file_stream)
    tok=tokenize_text(text)
    collect_data(tok)
