import csv

# פונקציה ששומרת את השורות לקובץ CSV עם כותרות
def save_feature_data_to_csv(rows, csv_header, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        writer.writerows(rows)
    print(f"Processed {len(rows)} rows")

def format_row_for_csv(result_dict, author, full_header, indices_to_keep, chapter_text):
    try:
        row = {}
        for item in result_dict:
            if ':' in item:
                key, value = item.split(':', 1)
                row[key.strip()] = value.strip()
        row["author"] = author
        row["text"] = chapter_text 

        full_row = [row.get(col, "") for col in full_header]
        filtered_row = [full_row[i] for i in indices_to_keep]
    except Exception as e:
        print("eroor {e}")

    return [filtered_row]
