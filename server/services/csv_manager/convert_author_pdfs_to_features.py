from file_processor import get_pdf_files_from_directory, process_file
from save_feature_data_to_csv import save_feature_data_to_csv 
from build_csv_headers import build_csv_headers   
import os


# פונקציה שמחזירה את הנתיב המלא לתיקיית מחבר
def get_author_path(base_path, author):
    return os.path.join(base_path, author)

# פונקציה שמבצעת את כל תהליך הניתוח למחבר אחד
def process_author(author, base_path):
    print(f"Processing author: {author}")
    author_path = get_author_path(base_path, author)
    if not os.path.exists(author_path):
        print(f"Warning: Directory not found for {author}: {author_path}")
        return

    output_file = os.path.join(author_path, f"{author.replace(' ', '_')}_features.csv")
    csv_header, full_header, indices_to_keep = build_csv_headers()
    pdf_files = get_pdf_files_from_directory(author_path)

    if not pdf_files:
        print(f"No PDF files found for {author}")
        return

    print(f"Found {len(pdf_files)} PDF files for {author}")
    all_rows = []

    for filename in pdf_files:
        print(f"Processing: {filename}")
        file_path = os.path.join(author_path, filename)
        file_rows = process_file(file_path, filename, author, full_header, indices_to_keep)
        all_rows.extend(file_rows)

    if all_rows and csv_header:
        save_feature_data_to_csv(all_rows, csv_header, output_file)
    else:
        print(f"No data saved for {author}")
