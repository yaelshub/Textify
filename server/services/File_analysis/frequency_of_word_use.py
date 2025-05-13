from nltk.probability import FreqDist

def get_word_frequencies(tok):
    top_n=30
    freq_dist = FreqDist(tok)
    return freq_dist.most_common(top_n)

