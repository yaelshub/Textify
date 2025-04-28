import spacy

tok=None
def tokenize_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    words = [token.text for token in doc]
    sentences = [sent.text for sent in doc.sents]

    print("Tokens (Words):")
    for word in words:
        print(word)

    print("\nSentences:")
    for sentence in sentences:
        print(sentence)
        print()

    tok = {"words": words, "sentences": sentences}
    return tok



# def collect_data(text):
#     tiyug=func_get_tiuyg(text)
#     ner=func_get_ner(text)
#     return recognize_writer(tiyug,ner)

