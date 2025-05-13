import spacy

tok=None
def tokenize_text(text):
    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        text = text.lower()
        words = [token.text for token in doc]
        sentences = [sent.text for sent in doc.sents]

        print("Tokens (Words):")

        tok = {"words": words, "sentences": sentences}
        print('tokenize_text: ')
        return tok
    except Exception as e:
        print(f"---------Error in tokenization: {e}")
        raise e




