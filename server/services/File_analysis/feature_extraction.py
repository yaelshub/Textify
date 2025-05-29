import os
import csv
import io
from services.File_analysis import file_analysis
from services.File_analysis.extraction_and_cutting import extract_text_from_pdf, split_text_into_chapters

def feature_extraction():
    base_path = r"D:\Textify\server\dal\textData"
    authors = ["Charles_Dickens","H_G_Wells","Jane-Austen","Mark_Twain"]
    for author in authors:
        print(f"Processing author: {author}")
        author_path = os.path.join(base_path, author)

        if not os.path.exists(author_path):
            print(f"Warning: Directory not found for {author}: {author_path}")
            continue

        output_file = os.path.join(author_path, f"{author.replace(' ', '_')}_features.csv")
        rows = []
        header = [
            "num_words", "clean_text", "tokenize_text", "word_info", 
            "entity_identification", "number_of_words_in_each_sentence",
            "calculate_average_word_count", "std_dev_words_per_sentence",
            "number_of_words_per_text", "word_count_info", "frequency_info",
            "average_word_length", "sentence_types", "word_frequencies",
            "count_personification", "book", "chapter", "author"
        ]

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
                        full_text = extract_text_from_pdf(file_stream)

                        if not full_text.strip():
                            print(f"Warning: No text extracted from {filename}")
                            continue

                        chapters = split_text_into_chapters(full_text)
                        print(f"Split into {len(chapters)} chapters")

                        for i, chapter in enumerate(chapters):
                            if not chapter.strip():
                                continue

                            try:
                                result = file_analysis(chapter)
                                if isinstance(result, list) and len(result) == len(header) - 3:
                                    row = result + [filename, i + 1, author]
                                    rows.append(row)
                                else:
                                    print(f"Warning: Unexpected result format in chapter {i + 1}")
                            except Exception as e:
                                print(f"Error processing chapter {i + 1}: {e}")
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")

            if rows:
                with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(rows)
                print(f"Processed {len(rows)} rows for {author}")
            else:
                print(f"No data saved for {author}")
        except Exception as e:
            print(f"Error processing author {author}: {e}")

    print("Feature extraction completed!")

feature_extraction()