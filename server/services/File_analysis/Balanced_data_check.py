import os
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from .extraction_and_cutting import extract_text_from_pdf

def extract_text_from_pdf(file_stream):
    try:
        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print("שגיאה בקריאת ה-PDF:", e)
    return text

def count_lines(text):
    return len(text.splitlines())

def count_lines_in_author_dir(author_path):
    total_lines = 0
    for filename in os.listdir(author_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(author_path, filename)
            try:
                text = extract_text_from_pdf(file_path)
                total_lines += count_lines(text)
            except Exception as e:
                print(f"שגיאה בעיבוד הקובץ {file_path}: {e}")
    return total_lines

def get_author_line_counts(root_dir):
    author_line_counts = {}
    for author in os.listdir(root_dir):
        author_path = os.path.join(root_dir, author)
        if not os.path.isdir(author_path):
            continue
        author_line_counts[author] = count_lines_in_author_dir(author_path)
    return author_line_counts

def data_balance_and_pie_drawing():
    root_dir = r"D:\Textify\server\dal\textData"
    author_line_counts = get_author_line_counts(root_dir)

    df = pd.DataFrame(list(author_line_counts.items()), columns=['Author', 'Line Count'])

    plt.figure(figsize=(8, 8))
    plt.pie(df['Line Count'], labels=df['Author'], autopct='%1.1f%%', startangle=140, pctdistance=0.85)
    plt.title('Balanced data',pad=5)
    plt.axis('equal') 
    plt.show()


# data_balance_and_pie_drawing()
