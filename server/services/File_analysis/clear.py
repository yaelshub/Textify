import re

text='D:\Textify\server\dal\textData\A-Little-Princess-By-Frances-Hodgson-Burnett-Retold-by-Jennifer-Bassett-Book-PDF.pdf'

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text).lower()
    