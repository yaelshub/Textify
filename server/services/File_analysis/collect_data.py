import spacy
import re
from services.File_analysis.tokenization import tokenize_text   
from services.File_analysis.tokenization import tok 
from collections import Counter

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
#המילה המקורית, הצורה הבסיסית של המילה, תג תחבירי המספק מידע מפורט יותר, תפקידה התחבירי של המילה, תבנית המילה מבחינת תווים ואותיות, האם מורכבת מאותיות בלבד, האם מילת עצירה 
for token in doc:
    print(token.text, token.lemma_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

def labeling():
    for label in doc:
       print(f"{token.text}: {token.pos_}")


def Entity_identification():
    for ent in doc.ents:
     print(ent.text, ent.start_char, ent.end_char, ent.label_)

def calculate_average_word_count(text):
    sentences = re.split(r'[.!?]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    words_per_sentence = [len(re.findall(r'\b\w+\b', sentence)) for sentence in sentences]
    average = sum(words_per_sentence) / len(words_per_sentence) if words_per_sentence else 0
    return average

def Number_of_words_per_text():
    num_words=len(tok["words"])
    return num_words

#סופר מספר פעמים בו כל מילה מופיעה בטקסט
def Number_of_times_a_word_appears_in_text():
    word_count = Counter(tok["words"])
    return word_count

#מחשב תדירות של כל מילה
def Frequency_of_each_word():
    word_freq={}
    for word in word_count:
     word_freq[word]=word_count[word]/num_words
    return word_freq

#מחשב ממוצע אורך מילה 
def Average_word_length():
   