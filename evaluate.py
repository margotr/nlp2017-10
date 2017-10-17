import sys
import os
from nltk.tokenize import TweetTokenizer
import json
import csv
import ast


tokenizer = TweetTokenizer()


def classify_files(dir, eval_file_name, n, threshold):
    # Open ngrams dict fil
    dict_file = n,"gram_min",threshold,".txt"
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
        data = json.load(json_file)

    data = ast.literal_eval(data)

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
                if ngram in data:
                    pRep += data[ngram][0]
                    pDem += data[ngram][1]
            if pRep > pDem:
                predictions[f] = "r"
            else:
                predictions[f] = "d"

    json.dump(predictions, eval_file)


def evaluate_scores(n, threshold, trainortest):
    classify_files('%s_data/rep'%trainortest, 'evaluationREP%s.txt' % n, n, threshold)
    classify_files('%s_data/dem'%trainortest, 'evaluationDEM%s.txt' % n, n, threshold)

    demcorrect = 0
    demwrong = 0
    repcorrect = 0
    repwrong = 0

    with open('evaluationDEM%s.txt' % n) as dem_file:
        dem_classifications = json.load(dem_file)

    for c in dem_classifications:
        if dem_classifications[c] == 'd':
            demcorrect += 1
        if dem_classifications[c] == 'r':
            demwrong += 1

    with open('evaluationREP%s.txt' % n) as rep_file:
        rep_classifications = json.load(rep_file)

    for c in rep_classifications:
        if rep_classifications[c] == 'r':
            repcorrect += 1
        if rep_classifications[c] == 'd':
            repwrong += 1

    print "FOR N = ", n, " threshold = ", threshold, "on data: ", trainortest
    print "Correctly classified as democrat: ", demcorrect
    print "Correctly classified as republican: ", repcorrect
    print "Incorrectly classified as republican: ", demwrong
    print "Incorrectly classified as democrat ", repwrong
    print "Total guessed correct: ", (demcorrect + repcorrect), " out of ", (
        demcorrect + repcorrect + demwrong + repwrong)
    print "-------------------------------------"

evaluate_scores(1, 25, 'train')
evaluate_scores(2, 25, 'train')
evaluate_scores(3, 25, 'train')
evaluate_scores(4, 25, 'train')
evaluate_scores(5, 25, 'train')

evaluate_scores(1, 25, 'test')
evaluate_scores(2, 25, 'test')
evaluate_scores(3, 25, 'test')
evaluate_scores(4, 25, 'test')
evaluate_scores(5, 25, 'test')

def typical_ngrams(n):

    ranked_ngrams_democrat = {}
    ranked_ngrams_republicans = {}

    filename = str(n) + "gram_min5.txt"

    with open(filename) as json_file:
        data = json.load(json_file)
    data = ast.literal_eval(data)

    for ngram in data:
        rep = data[ngram][0] / data[ngram][1]
        ranked_ngrams_republicans[ngram] = rep
        dem = data[ngram][1] / data[ngram][0]
        ranked_ngrams_democrat[ngram] = dem

    ranked_ngrams_democrat = sorted(ranked_ngrams_democrat, key=ranked_ngrams_democrat.get, reverse=True)
    ranked_ngrams_republicans = sorted(ranked_ngrams_republicans, key=ranked_ngrams_republicans.get, reverse=True)

    print str(n), "- grams ranked for democrat: "
    c = 0
    for ngram in ranked_ngrams_democrat:
        c += 1
        for n in ngram:
            print n.encode("utf-8"),
        print ""
        if c==10:
            break

    print " ------------------- "

    c = 0
    print str(n), "- grams Ranked for republican: "
    for ngram in ranked_ngrams_republicans:
        c += 1
        for n in ngram:
            print n.encode("utf-8"),
        print ""
        if c == 10:
            break


typical_ngrams(5)