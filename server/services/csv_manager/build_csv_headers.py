# פונקציה שמחזירה את כותרות העמודות הדרושות והכותרות המלאות + האינדקסים של אלו שנרצה לשמור
def build_csv_headers():
    csv_header = [
        "num_words", "word_info", "entity_identification", "number_of_words_in_each_sentence",
        "calculate_average_word_count", "std_dev_words_per_sentence",
        "number_of_words_per_text", "word_count_info", "frequency_info",
        "average_word_length", "sentence_types", "word_frequencies",
        "count_personification", "book", "chapter", "author"
    ]
    full_header = [
        "num_words", "clean_text", "tokenize_text", "word_info",
        "entity_identification", "number_of_words_in_each_sentence",
        "calculate_average_word_count", "std_dev_words_per_sentence",
        "number_of_words_per_text", "word_count_info", "frequency_info",
        "average_word_length", "sentence_types", "word_frequencies",
        "count_personification", "book", "chapter", "author"
    ]
    indices_to_keep = [full_header.index(col) for col in csv_header if col in full_header]
    return csv_header, full_header, indices_to_keep