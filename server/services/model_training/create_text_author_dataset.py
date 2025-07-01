import os
import pandas as pd
from services.file_analysis.extraction_and_cutting import split_text_into_chapters
import csv  


def undersample_dataframe(df):
    min_count = df['author'].value_counts().min()
    print(f"\nApplying undersampling: taking {min_count} samples from each author...")
    balanced_df = df.groupby('author').sample(n=min_count, random_state=42)
    return balanced_df

def process_authors_pdfs(base_path):
    all_texts = []
    all_authors = []
       
    author_folders = ['Charles_Dickens', 'H_G_Wells', 'Jane_Austen', 'Mark_Twain']

    for author_folder in author_folders:
        author_path = os.path.join(base_path, author_folder)
        
        if not os.path.exists(author_path):
            print(f"the folder {author_path} not found")
            continue
            
        print(f"processor Connector: {author_folder}")
        
# קבל את כל קבצי ה-PDF בתיקיה
        pdf_files = [f for f in os.listdir(author_path) if f.endswith('.pdf')]
        
        if not pdf_files:
            print(f"no PDF files found in the folder{author_folder}")
            continue
            
# עבור כל קובץ PDF של המחבר
        for pdf_file in pdf_files:
            pdf_path = os.path.join(author_path, pdf_file)
            print(f"file reader: {pdf_file}")
# חלק את הטקסט לפרקים
            chapters = split_text_into_chapters(pdf_path)
            
            print(f"found {len(chapters)} sections")
            
# הוסף כל פרק עם שם המחבר
            for chapter in chapters:
                # בדוק אם הפרק לא ריק ושהוא ארוך מ-50 תווים
                if chapter and isinstance(chapter, str) and len(chapter.strip()) > 50:
                    all_texts.append(chapter.strip())
                    all_authors.append(author_folder.replace('_', ' ').replace('-', ' '))
    
    return all_texts, all_authors

def create_csv_file():
    base_path = r"D:\Textify\server\dal\textData"
    texts, authors = process_authors_pdfs(base_path)
    if not texts:
        print("no texts found for processing!")
        return
    
# יצור DataFrame
    data = {
        'text': texts,
        'author': authors
    }
    df = pd.DataFrame(data)
    df["text"] = df["text"].str.replace(r'\s+', ' ', regex=True).str.strip()
    df = undersample_dataframe(df)

    output_file = 'texts_authors.csv'
    df.to_csv(output_file, index=False, encoding='utf-8', quoting=csv.QUOTE_MINIMAL)
    print(f"\n completed! file created{output_file}")
