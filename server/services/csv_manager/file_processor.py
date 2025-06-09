from ..file_analysis import extraction_and_cutting
from ..file_analysis import file_analysis1
from server.services.csv_manager.csv_operations import format_row_for_csv
import os


# פונקציה שמחזירה רשימת קבצי PDF  מתיקייה נתונה
def get_pdf_files_from_directory(author_path):
    return [f for f in os.listdir(author_path) if f.endswith(".pdf")]

# פונקציה שמבצעת את כל תהליך העיבוד לקובץ PDF אחד ומחזירה שורות מוכנות לכתיבה
def process_file(file_path, author, full_header, indices_to_keep):
    rows = []
    full_text = extraction_and_cutting.extract_text_from_pdf(file_path)
    if full_text.strip():
        chapters = extraction_and_cutting.split_text_into_chapters(full_text)
        print(f"Split into {len(chapters)} chapters")
        rows = extract_features_from_chapters(chapters, author, full_header, indices_to_keep)

    return rows

def extract_features_from_chapters(chapters, author, full_header, indices_to_keep):
    rows = []
    for i, chapter in enumerate(chapters):
        if chapter.strip():
            result = file_analysis1.file_analysis(chapter)
            chapter_rows = format_row_for_csv(result, author, full_header, indices_to_keep, chapter)
            if chapter_rows:
                rows.extend(chapter_rows)

    return rows