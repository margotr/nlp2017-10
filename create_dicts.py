from nltk.tokenize import TweetTokenizer
from collections import Counter

tokenizer = TweetTokenizer()

def create_ngram_vocabulary(location, n, min):
    ngrams = []

    tokens = tokenizer.tokenize(location)

    for i, token in enumerate(tokens):
        print token
        if n == 1:
            ngrams.append(token)
        if n == 2 and tokens[i] != tokens[-1]:
            ngrams.append(token, tokens[i + 1])
        if n == 3 and tokens[i] != tokens[-1]:
            ngrams.append(token, tokens[i + 1], tokens[i + 2])
        if n == 4 and tokens[i] != tokens[-1]:
            ngrams.append(token, tokens[i + 1], tokens[i + 2], tokens[i + 3])
        if n == 5 and tokens[i] != tokens[-1]:
            ngrams.append(token, tokens[i + 1], tokens[i + 2], tokens[i + 3], token[i + 4])

    d = Counter(ngrams)
    result = []
    for k, v in d.items():
        if v >= min:
            result.append(k)
    return result

print create_ngram_vocabulary(open("realdonaldtrump_tweets.csv").read().decode('utf8'), 2, 2)
