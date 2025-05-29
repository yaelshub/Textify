# CSV פונקציה שמעבדת את תוצאת ניתוח פרק ומחזירה את השורה המתאימה לקובץ 
def process_chapter_result(result, filename, chapter_index, author, full_header, indices_to_keep):
    rows = []
    if isinstance(result, list) and result:
        if len(result) > 0 and isinstance(result[-1], list):
            processed_data = result[-1]
            full_row = processed_data + [filename, chapter_index, author]
            filtered_row = [full_row[idx] for idx in indices_to_keep if idx < len(full_row)]
            rows.append(filtered_row)
        else:
            processed_row = []
            for item in result[:-1]:
                if isinstance(item, str) and ": " in item:
                    value = item.split(": ", 1)[1]
                    processed_row.append(value)
                else:
                    processed_row.append(str(item))
            while len(processed_row) < len(full_header) - 3:
                processed_row.append("")
            full_row = processed_row + [filename, chapter_index, author]
            filtered_row = [full_row[idx] for idx in indices_to_keep if idx < len(full_row)]
            rows.append(filtered_row)
    return rows

