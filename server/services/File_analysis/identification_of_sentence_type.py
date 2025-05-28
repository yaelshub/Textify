import spacy
nlp = spacy.load("en_core_web_sm")

def classify_sentence_type(sentences):

    for sentence in sentences:
        doc = nlp(sentence)
        verb_roots = [token for token in doc if token.dep_ in ("ROOT", "conj") and token.pos_ == "VERB"] # write by your own words
        has_subordinate_clause = any(token.dep_ == "mark" for token in doc)

        if has_subordinate_clause:
            sentence_type = "Complex"
        elif len(verb_roots) >= 2:
            sentence_type = "Compound"
        elif len(verb_roots) == 1:
            sentence_type = "Simple"
        else:
            sentence_type = "Unknown"

    return sentence_type
