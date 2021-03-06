from nltk.tokenize import TweetTokenizer
from collections import Counter
import os
import json

tokenizer = TweetTokenizer()
locationRep = "train_data/rep"
locationDem = "train_data/dem"

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
    fulltext_decoded = fulltext.decode('utf8', errors='ignore').lower()
    return create_ngram_vocabulary(fulltext_decoded, ngram, min)


def all_tokens_in_class(ngram, DorM):
    tokens = []
    ngrams = []
    fulltext = " "
    if DorM == "D":
        for root, dirs, files in os.walk(locationDem):
            for f in files:
                fulltext = fulltext + open(locationDem + "/" + f).read()
            fulltext = fulltext.lower()
            tokens = tokenizer.tokenize(fulltext.decode('utf8', errors='ignore'))
    if DorM == "R":
        for root, dirs, files in os.walk(locationRep):
            for f in files:
                fulltext = fulltext + open(locationRep + "/" + f).read()
            fulltext = fulltext.lower()
            tokens = tokenizer.tokenize(fulltext.decode('utf8', errors='ignore'))
    for i, token in enumerate(tokens):
        if ngram == 1:
            ngrams.append(token)
        if ngram == 2 and tokens[i] != tokens[-1]:
            ngrams.append((token, tokens[i + 1]))
        if ngram == 3 and tokens[i] != tokens[-2] and tokens[i] != tokens[-1]:
            ngrams.append((token, tokens[i + 1], tokens[i + 2]))
        if ngram == 4 and tokens[i] != tokens[-3] and tokens[i] != tokens[-2] and tokens[i] != tokens[-1]:
            ngrams.append((token, tokens[i + 1], tokens[i + 2], tokens[i + 3]))
        if ngram == 5 and tokens[i] != tokens[-4] and tokens[i] != tokens[-3] and tokens[i] != tokens[-2] and tokens[i] != tokens[-1]:
            ngrams.append((token, tokens[i + 1], tokens[i + 2], tokens[i + 3], tokens[i + 4]))
    return ngrams


def create_dict(ngram, min, filename):
    print("creating vocabulary")
    vocabulary = create_vocaubaly(ngram, min)
    print vocabulary
    print type(vocabulary)
    V = len(vocabulary)
    k = 1
    print("create DEM tokens")
    dem_token = all_tokens_in_class(ngram, 'D')
    dem_token_len = len(dem_token)
    print("create REP tokens")
    rep_token = all_tokens_in_class(ngram, 'R')
    rep_token_len = len(rep_token)

    # Create a dict with the words in the vocabulary as keys
    rep_wordcount = dict.fromkeys(vocabulary, 0)
    dem_wordcount = dict.fromkeys(vocabulary, 0)

    print("length vocab: ", len(vocabulary))

    # For each republican ngram, 'turf' if it's in the vocabulary
    progress = 0
    for rep_token_ngram in rep_token:
        progress += 1
        print "Progress for rep: ", float(progress) / float(rep_token_len) * 100, "%"
        print "Checking ngram ", rep_token_ngram
        if rep_token_ngram in vocabulary:
            rep_wordcount[rep_token_ngram] += 1

    # For each republican ngram, 'turf' if it's in the vocabulary
    progress = 0
    for dem_token_ngram in dem_token:
        progress += 1
        print "Progress for dem: ", float(progress) / float(dem_token_len) * 100, "%"
        print "Checking ngram ", dem_token_ngram
        if dem_token_ngram in vocabulary:
            dem_wordcount[dem_token_ngram] += 1

    combined_wordmeasure = dict.fromkeys(vocabulary, 0)
    for ngram in vocabulary:
        combined_wordmeasure[ngram] = [(float(rep_wordcount[ngram]) + k) / ((rep_token_len) + (k * V)),
                                   (float(dem_wordcount[ngram]) + k) / ((dem_token_len) + (k * V))]

    with open(filename, 'w+') as outfile:
        json.dump(str(combined_wordmeasure), outfile)

    outfile.close()

create_dict(1, 90, "1gram_min90.txt")
create_dict(2, 75, "2gram_min75.txt")
create_dict(3, 30, "3gram_min30.txt")
create_dict(4, 21, "4gram_min21.txt")
create_dict(5, 15, "5gram_min15.txt")