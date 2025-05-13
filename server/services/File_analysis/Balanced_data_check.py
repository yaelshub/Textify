import os
import pandas as pd
import matplotlib.pyplot as plt
from extract_from_PDF import extract_text_from_pdf

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


root_dir = 'dal\\textData'
author_line_counts = get_author_line_counts(root_dir)

df = pd.DataFrame(list(author_line_counts.items()), columns=['Author', 'Line Count'])

plt.figure(figsize=(8, 8))
plt.pie(df['Line Count'], labels=df['Author'], autopct='%1.1f%%', startangle=140, pctdistance=0.85)
plt.title('Checking whether the data is balanced according to the number of lines in the text')
plt.axis('equal') 
plt.show()


