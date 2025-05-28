import spacy
import re
nlp = spacy.load("en_core_web_sm")

def clean_text(text):   
    text = re.sub(r'/G\d+', '', text)  # הסרת רצפי G כמו /G37
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # הסרת תווים לא באנגלית
    text = re.sub(r'\n+', '\n', text)  # הסרת שורות ריקות מרובות
    text = text.replace('\n', ' ')
    text = re.sub(r'[ ]{2,}', ' ', text)  # הסרת רווחים כפולים
    text = re.sub(r'(?m)^\s*(Page\s*)?\d+\s*$', '', text)
    text = text.strip()
    return text





