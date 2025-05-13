import io
from .extract_from_PDF import extract_text_from_pdf
from .Balanced_data_check import count_lines
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



def main(file):
    file_stream = io.BytesIO(file.read())
    text=extract_text_from_pdf(file_stream)
    count_lines(text)
    clean_txt=clean_text(text)
    tok=tokenize_text(clean_txt)
    word_info(clean_txt)
    entity_identification(clean_txt)
    words_per_sentence=number_of_words_in_each_sentence(clean_txt)
    calculate_average_word_count(words_per_sentence)
    Standard_deviation_of_the_number_of_words_in_a_sentence(words_per_sentence)
    num_words=number_of_words_per_text(tok)
    word_count=number_of_times_a_word_appears_in_text(tok)
    frequency_of_each_word(word_count,num_words)
    average_word_length(tok,num_words)
    classify_sentence_type(tok["sentences"])
    get_word_frequencies(tok["words"])  
    return "hello"
