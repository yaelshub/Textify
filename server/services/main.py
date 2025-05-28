from File_analysis import extraction_and_cutting
from File_analysis import file_analysis
import os
import csv
import io

def main():
    base_path = r"D:\Textify\server\dal\textData"
    authors = ["Charles_Dickens"]

    for author in authors:
        print(f"Processing author: {author}")
        author_path = os.path.join(base_path, author)

        if not os.path.exists(author_path):
            print(f"Warning: Directory not found for {author}: {author_path}")
            continue
        
        output_file = os.path.join(author_path, f"{author.replace(' ', '_')}_features.csv")
        rows = []
        
        # הכותרות שצריכות להישמר בקובץ CSV
        csv_header = [
            "num_words", "word_info", "entity_identification", "number_of_words_in_each_sentence",
            "calculate_average_word_count", "std_dev_words_per_sentence",
            "number_of_words_per_text", "word_count_info", "frequency_info",
            "average_word_length", "sentence_types", "word_frequencies",
            "count_personification", "book", "chapter", "author"
        ]
        
        # כל הכותרות המקוריות כדי לדעת מה המיקום של כל עמודה
        full_header = [
            "num_words", "clean_text", "tokenize_text", "word_info", 
            "entity_identification", "number_of_words_in_each_sentence",
            "calculate_average_word_count", "std_dev_words_per_sentence",
            "number_of_words_per_text", "word_count_info", "frequency_info",
            "average_word_length", "sentence_types", "word_frequencies",
            "count_personification", "book", "chapter", "author"
        ]
        
        # אינדקסים של העמודות שצריכות להישמר
        indices_to_keep = []
        for col in csv_header:
            if col in full_header:
                indices_to_keep.append(full_header.index(col))

        try:
            pdf_files = [f for f in os.listdir(author_path) if f.endswith(".pdf")]
            if not pdf_files:
                print(f"No PDF files found for {author}")
                continue
            print(f"Found {len(pdf_files)} PDF files for {author}")
            
            for filename in pdf_files:
                print(f"Processing: {filename}")
                file_path = os.path.join(author_path, filename)
                try:
                    with open(file_path, "rb") as f:
                        file_stream = io.BytesIO(f.read())
                        full_text = extraction_and_cutting.extract_text_from_pdf(file_stream)
                        if not full_text.strip():
                            print(f"Warning: No text extracted from {filename}")
                            continue
                        chapters = extraction_and_cutting.split_text_into_chapters(full_text)
                        print(f"Split into {len(chapters)} chapters")

                        for i, chapter in enumerate(chapters):
                            if not chapter.strip():
                                continue
                            try:
                                # הקובץ עובר את כל התהליך של file_analysis
                                result = file_analysis.file_analysis(chapter)
                                
                                if isinstance(result, list) and result:
                                    if len(result) > 0 and isinstance(result[-1], list):
                                        processed_data = result[-1]
                                        # הוספת מידע על הספר, פרק ומחבר
                                        full_row = processed_data + [filename, i + 1, author]
                                        
                                        # בחירת רק העמודות הרצויות
                                        filtered_row = [full_row[idx] for idx in indices_to_keep if idx < len(full_row)]
                                        rows.append(filtered_row)
                                    else:
                                        # אם אין רשימה בסוף, ננסה לחלץ נתונים מהמחרוזות
                                        processed_row = []
                                        for item in result[:-1]:  # לא כולל את האלמנט האחרון
                                            if isinstance(item, str) and ": " in item:
                                                # חילוץ הערך אחרי ":"
                                                value = item.split(": ", 1)[1]
                                                processed_row.append(value)
                                            else:
                                                processed_row.append(str(item))
                                        
                                        # השלמה לגודל הנדרש אם חסרים נתונים
                                        while len(processed_row) < len(full_header) - 3:  # -3 עבור book, chapter, author
                                            processed_row.append("")
                                        
                                        full_row = processed_row + [filename, i + 1, author]
                                        
                                        # בחירת רק העמודות הרצויות
                                        filtered_row = [full_row[idx] for idx in indices_to_keep if idx < len(full_row)]
                                        rows.append(filtered_row)
                                else:
                                    print(f"Warning: No valid result for chapter {i + 1}")
                            except Exception as e:
                                print(f"Error processing chapter {i + 1}: {e}")
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")
            
            # שמירת הנתונים עם הכותרות המסוננות בלבד
            if rows and csv_header:
                with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(csv_header)
                    writer.writerows(rows)
                print(f"Processed {len(rows)} rows for {author}")
            else:
                print(f"No data saved for {author}")
        except Exception as e:
            print(f"Error processing author {author}: {e}")
    
    print("Feature extraction completed!")

main()