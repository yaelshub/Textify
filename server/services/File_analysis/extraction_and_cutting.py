from pdfminer.high_level import extract_text
import re

def extract_text_from_pdf(file_path):
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print("Error reading PDF:", e)
        return ""
    
def split_text_into_chapters(pdf_file_path):
    text = extract_text_from_pdf(pdf_file_path)
    if not text:
        print(f"Unable to extract text from{pdf_file_path}")
        return []

    chapter_patterns = [
        r'^\s*(CHAPTER|Chapter|chapter)\s+(\d+|[IVXLCDM]+)\s*(?:[\-:.\n\r\s]*)$',  # CHAPTER 1, Chapter I
        r'^\s*(CHAPTER|Chapter|chapter)\s+(THE\s+)?(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|TENTH)\s*(?:[\-:.\n\r\s]*)$',  # CHAPTER FIRST, CHAPTER SECOND
        r'^\s*(BOOK|Book|Part|PART)\s+(\d+|[IVXLCDM]+)\s*(?:[\-:.\n\r\s]*)$',  # BOOK I, PART II
        r'^\s*[IVXLCDM]+\.\s+[A-Z][a-zA-Z\s\-:,\'"]{3,}$',  # I. 
        r'^\s*CHAPTER\s+\d+\.\s+[A-Z ]{3,}$'  # CHAPTER 1. 
    ]

    combined_pattern = '|'.join(f'({p})' for p in chapter_patterns)
    regex = re.compile(combined_pattern, re.MULTILINE)

    matches = list(regex.finditer(text))

    if not matches:
        print("No chapters found according to known patterns.")
        return []

    chapters = []
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chapter_text = text[start:end].strip()
        chapters.append(chapter_text)
    return chapters