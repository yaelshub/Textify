from server.services.csv_manager.file_processor import get_pdf_files_from_directory, process_file
from server.services.csv_manager.csv_operations import save_feature_data_to_csv 
from server.services.csv_manager.build_csv_headers import build_csv_headers   
import os


# פונקציה שמחזירה את הנתיב המלא לתיקיית מחבר
def get_author_path(base_path, author):
    return os.path.join(base_path, author)

def process_author_pdfs(pdf_files, author_path,full_header, indices_to_keep, all_rows, author):
    for filename in pdf_files:
        file_path = os.path.join(author_path, filename)
        file_rows = process_file(file_path, author, full_header, indices_to_keep)
        all_rows.extend(file_rows)
    return all_rows

# פונקציה שמבצעת את כל תהליך הניתוח למחבר אחד
def process_author(author, base_path):
    author_path = get_author_path(base_path, author)

    if os.path.exists(author_path):
        pdf_files = get_pdf_files_from_directory(author_path)

        if pdf_files:
            print(f"Found {len(pdf_files)} PDF files for {author}")
            all_rows = []
            csv_header, full_header, indices_to_keep = build_csv_headers()

         
            all_rows = process_author_pdfs(pdf_files, author_path, full_header, indices_to_keep, all_rows, author)
            if all_rows and csv_header:
                output_file = os.path.join(author_path, f"{author.replace(' ', '_')}_features.csv")
                save_feature_data_to_csv(all_rows, csv_header, output_file)
            else:
                print(f"No data saved for {author}")
