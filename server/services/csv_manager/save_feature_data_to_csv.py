import csv

# פונקציה ששומרת את השורות לקובץ CSV עם כותרות
def save_feature_data_to_csv(rows, csv_header, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        writer.writerows(rows)
    print(f"Processed {len(rows)} rows")