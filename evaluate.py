import sys
import os
from nltk.tokenize import TweetTokenizer
import json
import csv

tokenizer = TweetTokenizer()


def classify_files(dir, eval_file_name, n):
    # Open ngrams dict fil
    dict_file = ""
    if n == 1:
        dict_file = "1gram_min30.txt"
    elif n == 2:
        dict_file = "2gram_min20.txt"
    elif n == 3:
        dict_file = "3gram_min10.txt"
    elif n == 4:
        dict_file = "4gram_min7.txt"
    elif n == 5:
        dict_file = "5gram_min5.txt"

    with open(dict_file) as json_file:
        data = json.load(json_file)[0]

    # Open evaluation file
    eval_file = open(eval_file_name, 'w+')

    # Put the predictions in a dict
    predictions = {}

    for root, dirs, filenames in os.walk(dir):
        for f in filenames:
            tokens = tokenizer.tokenize(open(os.path.join(root, f)).read().decode('utf8').lower())
            ngrams = []

            pRep = 0  # For each file, we calculate the probability it is in Rep
            pDem = 0  # For each file, we calculate the probability it is in Dem
            for i, token in enumerate(tokens):
                if n == 1:
                    ngrams.append(token)
                if n == 2 and tokens[i] != tokens[-1]:
                    ngrams.append((token, tokens[i + 1]))
                if n == 3 and tokens[i] != tokens[-2] and tokens[i] != tokens[-1]:
                    ngrams.append((token, tokens[i + 1], tokens[i + 2]))
                if n == 4 and tokens[i] != tokens[-3] and tokens[i] != tokens[-2] and tokens[i] != tokens[-1]:
                    ngrams.append((token, tokens[i + 1], tokens[i + 2], tokens[i + 3]))
                if n == 5 and tokens[i] != tokens[-4] and tokens[i] != tokens[-3] and tokens[i] != tokens[-2] and \
                                tokens[i] != tokens[-1]:
                    ngrams.append((token, tokens[i + 1], tokens[i + 2], tokens[i + 3], tokens[i + 4]))

            # Find the likelihood for each ngram in the file
            for ngram in ngrams:
                try:
                    if str(ngram) in data:
                        pRep += data[str(ngram)][0]
                        pDem += data[str(ngram)][1]
                except:
                    print "Something went from for", ngram

            if pRep > pDem:
                predictions[f] = "r"
            else:
                predictions[f] = "d"

    json.dump(predictions, eval_file)


def evaluate_scores(n):
    classify_files('train_data/rep', 'evaluationREP%s.txt' % n, n)
    classify_files('train_data/dem', 'evaluationDEM%s.txt' % n, n)

    demcorrect = 0
    demwrong = 0
    repcorrect = 0
    repwrong = 0

    with open('evaluationDEM%s.txt'%n) as dem_file:
        dem_classifications = json.load(dem_file)

    for c in dem_classifications:
        if dem_classifications[c] == 'd':
            demcorrect += 1
        if dem_classifications[c] == 'r':
            demwrong += 1

    with open('evaluationREP%s.txt'%n) as rep_file:
        rep_classifications = json.load(rep_file)

    for c in rep_classifications:
        if rep_classifications[c] == 'r':
            repcorrect += 1
        if rep_classifications[c] == 'd':
            repwrong += 1

    print "FOR N = ", n
    print "Correctly classified as democrat: ", demcorrect
    print "Correctly classified as republican: ", repcorrect
    print "Incorrectly classified as republican: ", demwrong
    print "Incorrectly classified as democrat ", repwrong
    print "Total guessed correct: ", (demcorrect + repcorrect), " out of ", (demcorrect + repcorrect + demwrong + repwrong)


evaluate_scores(1)
evaluate_scores(2)
evaluate_scores(3)
evaluate_scores(4)
evaluate_scores(5)
