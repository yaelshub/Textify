import spacy


def tokenize_text(text):

    tok=None

    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        text = text.lower()
        words = [token.text for token in doc]
        sentences = [sent.text for sent in doc.sents]
        tok = {"words": words, "sentences": sentences}

        return tok

    except Exception as e:
        print(f"---------Error in tokenization: {e}")
        raise e
