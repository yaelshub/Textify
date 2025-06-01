import spacy
import re
import numpy as np
# from .tokenization import tokenize_text
from collections import Counter

nlp = spacy.load("en_core_web_sm")

#המילה המקורית, הצורה הבסיסית של המילה, תג תחבירי המספק מידע מפורט יותר, תפקידה התחבירי של המילה, תבנית המילה מבחינת תווים ואותיות, האם מורכבת מאותיות בלבד, האם מילת עצירה 
def word_info(text):
    doc = nlp(text)
    results = []
    for token in doc:
        results.append({
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "shape": token.shape_,
            "is_alpha": token.is_alpha,
            "is_stop": token.is_stop
        })
    return results
        
def entity_identification(text):  
    doc = nlp(text)
    result = []    
    for ent in doc.ents: 
        result.append({
            "text": ent.text,
            "start_char": ent.start_char,
            "end_char": ent.end_char,
            "label": ent.label_
        })
    return result

#מספר המילים שבכל משפט
def number_of_words_in_each_sentence(text):
    sentences = re.split(r'[.!?]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    words_per_sentence = [len(re.findall(r'\b\w+\b', sentence)) for sentence in sentences]
    return words_per_sentence

#ממוצע מילים במשפט
def calculate_average_word_count(words_per_sentence):
    average = sum(words_per_sentence) / len(words_per_sentence) if words_per_sentence else 0
    return average

#סטיית תקן של  כמות המילים במשפט
def Standard_deviation_of_the_number_of_words_in_a_sentence(words_per_sentence):
    if not words_per_sentence:
        print("Warning: Empty list provided for words_per_sentence.")
        return 0
    if len(words_per_sentence) == 1:
        print("Warning: Only one sentence, standard deviation is 0 by definition.")
        return 0
    return np.std(words_per_sentence)

#מספר המילים בטקסט
def number_of_words_per_text(tok):
    num_words=len(tok["words"])
    return num_words

#סופר מספר פעמים בו כל מילה מופיעה בטקסט
def number_of_times_a_word_appears_in_text(tok):
    word_count = Counter(tok["words"])
    return word_count

#מחשב תדירות של כל מילה
def frequency_of_each_word(word_count,num_words):
    word_freq={}
    for word in word_count:
     word_freq[word]=word_count[word]/num_words
    return word_freq

#מחשב ממוצע אורך מילה 
def average_word_length(tok,num_words):
    if num_words == 0:
        return 0
    total_length = sum(len(word) for word in tok["words"])
    return total_length/num_words


