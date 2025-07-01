# from .extraction_and_cutting import extract_text_from_pdf
from .balanced_data_check import count_lines
from .tokenization import tokenize_text
from .clean import clean_text
from .collect_data import (word_info,
                           entity_identification,
                           number_of_words_in_each_sentence,
                           calculate_average_word_count,
                           Standard_deviation_of_the_number_of_words_in_a_sentence,
                           number_of_words_per_text,
                           number_of_times_a_word_appears_in_text,
                           frequency_of_each_word,
                           average_word_length
                           )
from .identification_of_sentence_type import classify_sentence_type
from .frequency_of_word_use import get_word_frequencies
from .personification import count_personifications

def file_analysis(text):
    results =[]
    try:
        print("start function count_lines")
        cnt_lines = count_lines(text)
        results.append(f"num_words: {cnt_lines}")  
        print("end function count_lines")
    except Exception as e:
        raise e
    try:
        print("try function clean_text")
        clean_txt = clean_text(text)
        results.append(f"clean_text: {clean_txt}")
        print("end function clean_text")
    except Exception as e:
        raise e

    try:
        print("start function tokenize_text")
        tok = tokenize_text(clean_txt)
        results.append(f"tokenize_text: {tok}")
        print("end function tokenize_text")
    except Exception as e:
        raise e

    try:
        print("start function word_info")
        word_statistics = word_info(clean_txt)
        results.append(f"word_info: {word_statistics}")
        print("end function word_info")
    except Exception as e:
        raise e

    try:
        print("start function entity_identification")
        named_entities = entity_identification(clean_txt)
        results.append(f"entity_identification: {named_entities}")
        print("end function entity_identification")
    except Exception as e:
        raise e
    try:
        print("start function number_of_words_in_each_sentence")
        words_per_sentence = number_of_words_in_each_sentence(clean_txt)
        results.append(f"number_of_words_in_each_sentence: {words_per_sentence}")
        print("end function number_of_words_in_each_sentence")
    except Exception as e:
        raise e

    try:
        print("start function calculate_average_word_count")
        average_word_count = calculate_average_word_count(words_per_sentence)
        results.append(f"calculate_average_word_count: {average_word_count}")
        print("end function calculate_average_word_count")
    except Exception as e:
        raise e        
    try:
        print("start function Standard_deviation_of_the_number_of_words_in_a_sentence") 
        std_dev_words_per_sentence = Standard_deviation_of_the_number_of_words_in_a_sentence(words_per_sentence)
        results.append(f"Standard_deviation_of_the_number_of_words_in_a_sentence: {std_dev_words_per_sentence}")    
        print("end function Standard_deviation_of_the_number_of_words_in_a_sentence")
    except Exception as e:
        raise e
    try:
        print("start function number_of_words_per_text")
        num_words = number_of_words_per_text(tok)
        results.append(f"number_of_words_per_text: {num_words}")
        print("end function number_of_words_per_text")
    except Exception as e:
        raise e

    try:
        print("start function number_of_times_a_word_appears_in_text")
        word_count = number_of_times_a_word_appears_in_text(tok)
        results.append(f"number_of_times_a_word_appears_in_text: {word_count}")
        print("end function number_of_times_a_word_appears_in_text")    
    except Exception as e:
        raise e

    try:
        print("start function frequency_of_each_word")
        word_frequencies= frequency_of_each_word(word_count, num_words)
        results.append(f"frequency_of_each_word: {word_frequencies}")
        print("end function frequency_of_each_word")
    except Exception as e:
        raise e
    try:
        print("start function average_word_length")
        avg_word_length = average_word_length(tok, num_words)
        results.append(f"average_word_length: {avg_word_length}")
        print("end function average_word_length")
    except Exception as e:
        raise e
    try:
        print("start function classify_sentence_type")
        sentence_types = classify_sentence_type(tok["sentences"])
        results.append(f"classify_sentence_type: {sentence_types}")
        print("end function classify_sentence_type")
    except Exception as e:
        raise e
    try:
        print("start function get_word_frequencies")
        word_frequencies = get_word_frequencies(tok["words"])
        results.append(f"get_word_frequencies: {word_frequencies}")
        print("end function get_word_frequencies")
    except Exception as e:
        raise e
    try:
        print("start function count_personifications")
        count_personification = count_personifications(tok["sentences"])
        results.append(f"count_personification: {count_personification}")
        print("end function count_personifications")
    except Exception as e:
        raise e
    
    results.append("author: unknown")
    results.append("text: unknown")

    results.append([cnt_lines, clean_txt, tok, word_statistics, named_entities, words_per_sentence, average_word_count, std_dev_words_per_sentence, num_words, word_count, word_frequencies, avg_word_length, sentence_types, word_frequencies, count_personification])
    return results
