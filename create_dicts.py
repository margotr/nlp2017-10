from nltk.tokenize import TweetTokenizer
from collections import Counter
import os

tokenizer = TweetTokenizer()
locationRep = "rep"
locationDem = "dem"

def create_ngram_vocabulary(file, n, min):
    ngrams = []
    tokens = tokenizer.tokenize(file)
    for i, token in enumerate(tokens):
        if n == 1:
            ngrams.append(token)
        if n == 2 and tokens[i] != tokens[-1]:
            ngrams.append((token, tokens[i + 1]))
        if n == 3 and tokens[i] != tokens[-2] and tokens[i] != tokens[-1]:
            ngrams.append((token, tokens[i + 1], tokens[i + 2]))
        if n == 4 and tokens[i] != tokens[-3] and tokens[i] != tokens[-2] and tokens[i] != tokens[-1]:
            ngrams.append((token, tokens[i + 1], tokens[i + 2], tokens[i + 3]))
        if n == 5 and tokens[i] != tokens[-4] and tokens[i] != tokens[-3] and tokens[i] != tokens[-2] and tokens[i] != tokens[-1]:
            ngrams.append((token, tokens[i + 1], tokens[i + 2], tokens[i + 3], tokens[i + 4]))
    d = Counter(ngrams)
    result = []
    for k, v in d.items():
        if v >= min:
            result.append(k)
    return result


def create_vocaubaly(ngram, min):
    fulltext = " "
    for root, dirs, filenames in os.walk(locationRep):
        for f in filenames:
            fulltext = fulltext + open(locationRep + "/" + f).read()
    for root, dirs, filenames in os.walk(locationDem):
        for f in filenames:
            fulltext = fulltext + open(locationDem + "/" + f).read()
    return create_ngram_vocabulary(fulltext.decode('utf8').lower(), ngram, min)


def all_tokens_in_class(DorM):
    tokens = []
    fulltext = " "
    if DorM == "D":
        for root, dirs, files in os.walk("dem"):
            for f in files:
                fulltext = fulltext + open(locationDem + "/" + f).read()
            fulltext = fulltext.lower()
            tokens = tokenizer.tokenize(fulltext.decode('utf8'))
    if DorM == "R":
        for root, dirs, files in os.walk("rep"):
            for f in files:
                fulltext = fulltext + open(locationRep + "/" + f).read()
            fulltext = fulltext.lower()
            tokens = tokenizer.tokenize(fulltext.decode('utf8'))
    return tokens


def create_dict(ngram, min, filename):
    print("creating vocabulary")
    vocabulary = create_vocaubaly(ngram, min)
    V = len(vocabulary)
    k = 1
    print("create DEM tokens")
    dem_token = all_tokens_in_class('D')
    dem_token_len = len(dem_token)
    print("create REP tokens")
    rep_token = all_tokens_in_class('R')
    rep_token_len = len(rep_token)
    with open(filename, "w+") as f:
        print("creating ")
        print("length vocab: ", len(vocabulary))
        for word in vocabulary:
            print("count rep occurances of ",word)
            repOc = 0
            for term in rep_token:
                if term == word:
                    repOc += 1
            print("count dem occurances of ",word)
            demOc = 0
            for term in dem_token:
                if term == word:
                    demOc += 1
            print("calculating and writing measures")
            rep_probability = ((float(repOc) + k) / (float(rep_token_len) + (k * V)))
            dem_probablity = ((float(demOc) + k) / (float(dem_token_len) + (k * V)))
            f.write(str(word) + ", " + str(rep_probability) + ", " + str(dem_probablity) + "\n")
            # debug printing
            print(word, "rep: " + str(repOc), "dem: " + str(demOc))
    f.close()

create_dict(5, 25, "bigram_min25.txt")