import spacy
nlp = spacy.load("en_core_web_sm")

def classify_sentence_type(sentences):
    verb_roots = []

    for sentence in sentences:
        sentence = nlp(sentence)
        for token in sentence:
            if token.dep_ in ("ROOT", "conj") and token.pos_ == "VERB":
              verb_roots.append(token)
        has_subordinate_clause = any(token.dep_ == "mark" for token in sentence)


        if has_subordinate_clause:
            sentence_type = "Complex"
        elif len(verb_roots) > 1:
            sentence_type = "Compound"
        elif len(verb_roots) == 1:
            sentence_type = "Simple"
        else:
            sentence_type = "Unknown"

    return sentence_type
