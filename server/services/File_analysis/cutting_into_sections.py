import re

def split_text_into_chapters(text):
    pattern = re.compile(r'(Chapter\s+\d{1,3})', re.IGNORECASE)
    parts = pattern.split(text)
    chapters = []
    for i in range(1, len(parts), 2):
        content = parts[i + 1].strip() if (i + 1) < len(parts) else ''
        chapters.append(content)
    return chapters