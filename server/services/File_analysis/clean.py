import spacy
import re
nlp = spacy.load("en_core_web_sm")

def clean_text(text):   
    text = re.sub(r'/G\d+', '', text)  # הסרת רצפי G כמו /G37
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # הסרת תווים לא באנגלית
    text = re.sub(r'\n+', '\n', text)  # הסרת שורות ריקות מרובות
    text = re.sub(r'[ ]{2,}', ' ', text)  # הסרת רווחים כפולים
    text = re.sub(r'(?i)^COPYRIGHT.*\n?', '', text)  # הסרת שורות של זכויות יוצרים
    text = re.sub(r'(?m)^\s*(Page\s*)?\d+\s*$', '', text)
    text = text.strip()
    return text

import re

def detect_author_name(text, max_intro_lines=100):
    lines = text.splitlines()
    potential_names = []
    for i, line in enumerate(lines[:max_intro_lines]):
        lower_line = line.lower()
        if "by" in lower_line or "author" in lower_line:
            names = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b", line)
            potential_names.extend(names)
    return list(set(potential_names))


def clean_intro_auto(text, max_intro_lines=100):
    try:
        author_names = detect_author_name(text, max_intro_lines)
        lines = text.splitlines()
        cleaned_lines = []
        removed_lines = []  # רשימה לשמירת השורות שהוסרו
        for i, line in enumerate(lines):
            if i < max_intro_lines:
                lower_line = line.lower()
                if any(name.lower() in lower_line for name in author_names):
                    removed_lines.append(line)  # שמירה של השורה שנמחקה
                    continue
                if "author" in lower_line or "by" in lower_line:
                    removed_lines.append(line)  # שמירה של השורה שנמחקה
                    continue
                if line.strip().isdigit():
                    removed_lines.append(line)  # שמירה של השורה שנמחקה
                    continue
            cleaned_lines.append(line)
        print("Removed Lines:")
        for removed in removed_lines:
            print('removed') 
        return "\n".join(cleaned_lines)
    except Exception as e:
        print("שגיאה ב-clean_intro_auto:", e)
        return text  # מחזיר את הטקסט המקורי במקרה של שגיאה
