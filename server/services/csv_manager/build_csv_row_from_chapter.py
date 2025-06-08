def process_chapter_result(result_dict, author, full_header, indices_to_keep, chapter_text):
    try:
        row = {}
        for item in result_dict:
            if ':' in item:
                key, value = item.split(':', 1)  # מפריד רק לפי ה-':' הראשון
                row[key.strip()] = value.strip()
        row["author"] = author
        row["text"] = chapter_text 

        full_row = [row.get(col, "") for col in full_header]
        filtered_row = [full_row[i] for i in indices_to_keep]
    except Exception as e:
        print("eroor {e}")

    return [filtered_row]
