import re
import fitz
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return full_text

#מגדירה רשימת תבניות של כותרות פרקים ומחברת את כולן ומחזירה עצם 
def get_chapter_regex():
    chapter_patterns = [
        r'^\s*(CHAPTER|Chapter|chapter)\s+(\d+|[IVXLCDM]+)\s*(?:[\-:.\n\r\s]*)$',
        r'^\s*(CHAPTER|Chapter|chapter)\s+(THE\s+)?(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|TENTH)\s*(?:[\-:.\n\r\s]*)$',
        r'^\s*(BOOK|Book|Part|PART)\s+(\d+|[IVXLCDM]+)\s*(?:[\-:.\n\r\s]*)$',
        r'^\s*[IVXLCDM]+\.\s+[A-Z][a-zA-Z\s\-:,\'"]{3,}$',
        r'^\s*CHAPTER\s+\d+\.\s+[A-Z ]{3,}$'
    ]
    combined = '|'.join(f'({p})' for p in chapter_patterns)
    return re.compile(combined, re.MULTILINE)
#מקבלת טקסט של פרק ואת  הביטויים ומחזירה את הטקסט הנקי בלי כותרת
def remove_chapter_header(text, chapter_regex):
    lines = text.splitlines()
    if lines and chapter_regex.match(lines[0]):
        return '\n'.join(lines[1:]).strip()
    return text.strip()

def split_text_into_chapters(text):
    chapter_regex = get_chapter_regex()

    chapters = []

    if text:
        #חיפוש כל כותרות הפרקים בטקסט לפי התבניות שהוגדרו בביטוי הרגולרי ושומר אותם ברשימה
        matches = list(chapter_regex.finditer(text))

        if matches:
            for i in range(len(matches)):
                start = matches[i].start()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                #חתיכת הקטע הזה 
                chapter_text = text[start:end].strip()
                #הסרת כותרת הפרק עצמה
                cleaned_text = remove_chapter_header(chapter_text, chapter_regex)
                # הוספת הטקסט הנקי לרשימת הפרקים
                chapters.append(cleaned_text)
        #אם אין זיהוי של פרקים — פיצול הטקסט בכוח ל־10 חלקים בגודל שווה 
        else:
            length = len(text)
            segment_size = length // 10
            #יצירת 10 קטעים באורך קבוע, האחרון גולש עד סוף הקובץ
            for i in range(10):
                start = i * segment_size
                end = (i + 1) * segment_size if i < 9 else length
                part_text = text[start:end].strip()
                chapters.append(part_text)

    return chapters
