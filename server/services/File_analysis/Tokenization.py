import spacy

def tokenize_words(doc):
    return [token.text for token in doc]

def tokenize_sentences(doc):
    return [sent.text for sent in doc.sents]

def tokenize_text(text):
    tok = None
    try:
        nlp = spacy.load("en_core_web_sm")
        text = text.lower()
        doc = nlp(text)

        words = tokenize_words(doc)
        sentences = tokenize_sentences(doc)

        tok = {"words": words, "sentences": sentences}
        return tok

    except Exception as e:
        print(f"error in tokenization: {e}")
        raise e
    
