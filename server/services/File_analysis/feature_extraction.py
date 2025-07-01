import os, csv, io
from server.services.file_analysis.file_analysis1 import file_analysis
from server.services.file_analysis.extraction_and_cutting import extract_text_from_pdf, split_text_into_chapters
from server.services.csv_manager.config import AUTHORS, BASE_PATH

HEADER = [
    "num_words",                      
    "word_info",                      
    "entity_identification",          
    "number_of_words_in_each_sentence",
    "calculate_average_word_count",    
    "std_dev_words_per_sentence",      
    "number_of_words_per_text",        
    "word_count_info",                
    "frequency_info",                  
    "average_word_length",            
    "sentence_types",                  
    "word_frequencies",                
    "count_personification",          
    "book", "chapter", "author"        
]

EXPECTED_LEN = len(HEADER) - 3       
# אינדקסים של הפריטים שרוצים להסיר מה-file_analysis (clean_text=1, tokenize_text=2)
DROP_IDX = {1, 2}

def strip_label(x):
#מסיר את התווית מהערך - מחזיר רק את הערך עצמו
    if isinstance(x, str):
        if ": " in x:
            return x.split(": ", 1)[1]
        elif ":" in x:
            return x.split(":", 1)[1].strip()
    return x

def process_chapter(chapter, filename, chap_idx, author):
 #עיבוד פרק יחיד והמרה לשורת CSV
    feat = file_analysis(chapter)
    
    if isinstance(feat, list):
        # הסרת הרשימה האחרונה אם קיימת (לא נחוצה)
        if len(feat) > 0 and isinstance(feat[-1], list):
            feat = feat[:-1]
        
        # הסרת העמודות שלא רוצים (clean_text, tokenize_text)
        feat = [v for i, v in enumerate(feat) if i not in DROP_IDX]
        
        # ניקוי הערכים מהתוויות
        cleaned_feat = []
        for item in feat:
            cleaned_value = strip_label(item)
            cleaned_feat.append(cleaned_value)
        
        # בדיקה שהאורך נכון
        if len(cleaned_feat) == EXPECTED_LEN:
            return cleaned_feat + [filename, chap_idx + 1, author]
        else:
            print(f"Length mismatch: expected {EXPECTED_LEN}, got {len(cleaned_feat)} in {filename} chap {chap_idx+1}")
    
    print(f"Format mismatch in {filename} chap {chap_idx+1}")
    return None

def process_author(author):
#עיבוד כל הקבצים של סופר אחד
    print(f"Processing {author}")
    author_dir = os.path.join(BASE_PATH, author)
    
    if not os.path.exists(author_dir):
        print(f"Directory not found: {author_dir}")
        return
    
    pdfs = [f for f in os.listdir(author_dir) if f.endswith(".pdf")]
    
    if not pdfs:
        print(f"No PDF files found in {author_dir}")
        return
    
    rows = []
    
    for pdf in pdfs:
        print(f"Processing {pdf}")
        try:
            with open(os.path.join(author_dir, pdf), "rb") as fh:
                text = extract_text_from_pdf(io.BytesIO(fh.read()))
            
            chapters = split_text_into_chapters(text)
            print(f"Found {len(chapters)} chapters in {pdf}")
            
            for i, chap in enumerate(chapters):
                row = process_chapter(chap, pdf, i, author)
                if row:
                    rows.append(row)
                    
        except Exception as e:
            print(f"Error processing {pdf}: {e}")
    
    if rows:    
        out_csv = os.path.join(author_dir, f"{author}_features.csv")
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # כתיבת הכותרת
            writer.writerow(HEADER)
            # כתיבת הנתונים 
            writer.writerows(rows)
        print(f"Saved {len(rows)} rows → {out_csv}")
    else:
        print("No valid rows – nothing saved")

def feature_extraction():
#פונקציה ראשית להפקת מאפיינים
    for author in AUTHORS:
        try:
            process_author(author)
        except Exception as e:
            print(f"Error processing author {author}: {e}")
    print("Feature extraction completed!")
