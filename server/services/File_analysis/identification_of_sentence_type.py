import spacy
nlp = spacy.load("en_core_web_sm")

def classify_sentence_type(text):
    doc = nlp(text)
    
    verb_roots = [token for token in doc if token.dep_ in ("ROOT", "conj") and token.pos_ == "VERB"]
    has_subordinate_clause = any(token.dep_ == "mark" for token in doc)

    if has_subordinate_clause:
        return "Complex"
    elif len(verb_roots) >= 2:
        return "Compound"
    elif len(verb_roots) == 1:
        return "Simple"
    else:
        return "Unknown"


sentences = [
"I wanted to sleep early, but my phone kept buzzing.",
"She made coffee, and he prepared breakfast.",
"The sun was shining, so we went for a walk.",
"He didn’t know the answer, nor did he try to guess.",
"You can take the train, or you can drive.",
"The kids were playing outside, yet it started to rain.",
"I love reading books, and my sister enjoys drawing.",
"He studied all night, but he still failed the test.",
"The dog barked loudly, so we checked the yard.",
"They arrived late, and the meeting had already started."
    
]

for s in sentences:
    result = classify_sentence_type(s)
    print(result)

