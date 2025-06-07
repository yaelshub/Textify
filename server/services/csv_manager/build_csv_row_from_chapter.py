def process_chapter_result(result_dict, author, full_header, indices_to_keep, chapter_text):
    row = result_dict.copy()
    row["author"] = author
    row["text"] = chapter_text 

    full_row = [row.get(col, "") for col in full_header]
    filtered_row = [full_row[i] for i in indices_to_keep]
    return [filtered_row]
