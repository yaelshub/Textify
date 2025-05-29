from File_analysis import extraction_and_cutting
from File_analysis import file_analysis
from chapter_processor import process_chapter_result
import io
import os


# פונקציה שמחזירה רשימת קבצי PDF  מתיקייה נתונה
def get_pdf_files_from_directory(author_path):
    return [f for f in os.listdir(author_path) if f.endswith(".pdf")]

# פונקציה שמבצעת את כל תהליך העיבוד לקובץ PDF אחד ומחזירה שורות מוכנות לכתיבה
def process_file(file_path, filename, author, full_header, indices_to_keep):
    rows = []
    try:
        with open(file_path, "rb") as f:
            file_stream = io.BytesIO(f.read())
            full_text = extraction_and_cutting.extract_text_from_pdf(file_stream)
            if not full_text.strip():
                print(f"Warning: No text extracted from {filename}")
                return rows
            chapters = extraction_and_cutting.split_text_into_chapters(full_text)
            print(f"Split into {len(chapters)} chapters")
            for i, chapter in enumerate(chapters):
                if not chapter.strip():
                    continue
                try:
                    result = file_analysis.file_analysis(chapter)
                    chapter_rows = process_chapter_result(result, filename, i + 1, author, full_header, indices_to_keep)
                    if chapter_rows:
                        rows.extend(chapter_rows)
                    else:
                        print(f"Warning: No valid result for chapter {i + 1}")
                except Exception as e:
                    print(f"Error processing chapter {i + 1}: {e}")
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
    return rows