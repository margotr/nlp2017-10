# Code adapted from https://gist.github.com/yanofsky/5436496 for academic use

#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv
import os
import re

# Twitter API credentials
consumer_key = "e1iHkgum9tHvTuWUtjwqoTOO6"
consumer_secret = "wbF6OrDiQf1bMdghVo27HUpYLd2E0eiw5iARXZKWfmIhiVDP6v"
access_key = "919862426300043264-YCjEBrp6s5IsvL4RH9zTaKgkTabekzN"
access_secret = "NOIgJ7yHXi2bU2n3xDLzrTSr8DBw739h2vv3YvDNLNOWa"

def get_all_tweets(screen_name, dir=os.getcwd()):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    except:
        print 'Issues for', screen_name,'. Not indexing this one.'
        return

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

        if len(alltweets) >= 1000:
            break
        print "for %s" % screen_name

    cleaned_text = [re.sub(r'http[s]?:\/\/.*[\W]*', '', i.text, flags=re.MULTILINE) for i in alltweets]  # remove urls
    cleaned_text = [re.sub(r'RT.*', '', i, flags=re.MULTILINE) for i in cleaned_text]  # delete the retweets

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[cleaned_text[idx].encode("utf-8")] for idx, tweet in
                 enumerate(alltweets)]

    # write the csv
    filename = '%s_tweets.csv' % screen_name
    fullpath = os.path.join(dir, filename)
    with open(fullpath, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(outtweets)
    pass

# Do not run this unless you want to reindex all tweets and want to have a coffee break
def get_labeled_tweets():
    with open('TwitterAccounts.csv', 'rb') as accounts_csv:
        reader = csv.reader(accounts_csv)
        for row in reader:
            label = row[3]

            filename = '%s_tweets.csv' % row[1]
            dempath = os.path.join(os.getcwd(), "no_retweets_or_urls/train_data/dem")
            reppath = os.path.join(os.getcwd(), "no_retweets_or_urls/train_data/rep")
            othpath = os.path.join(os.getcwd(), "no_retweets_or_urls/train_data/other")
            dempath_f = os.path.join(dempath, filename)
            reppath_f = os.path.join(reppath, filename)
            othpath_f = os.path.join(othpath, filename)

            # Don't try to index tweets we already have
            if not(os.path.exists(dempath_f) or os.path.exists(reppath_f) or os.path.exists(othpath_f)):
                if label == 'r':
                    get_all_tweets(row[1], reppath)
                elif label == 'd':
                    get_all_tweets(row[1], dempath)
                else:
                    get_all_tweets(row[1], othpath)
                print "Done: ", row[1], row[3]
            else:
                print "Already indexed ", row[1]
        accounts_csv.close()

get_labeled_tweets()