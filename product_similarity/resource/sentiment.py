from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from nltk.corpus import names

import plotly as py
import tweepy

from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
import re
import pandas as pd
from dash.dependencies import Output, State, Input
import preprocessor as p
import plotly.graph_objs as go
import random
from plotly.offline import iplot
import datetime
import io
import csv
import json
import nltk
nltk.download('names')

consumer_key = 'GFYPmseNxSYRaJBurE2fCOgCR'
consumer_secret = '6DZEfk8BadhdeFDlKcgwUE60tuG6NvkR9xPjzBSgRoZupVLmSx'
access_token_key = '1227165190929756160-0bcQB2yS1BaewofzavjlZrlSB0sprX'
access_token_secret = 'l7N645nQbwPuPqhfjanm8gEl6LpIYWuVOUTfE9wegsElw'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)


def clean_tweets(txt):
    txt = " ".join(re.sub(
        "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", "", txt).split())
    #p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.NUMBER)
    tweet_cleean = txt
    return tweet_cleean


def gender_features(word):
    return {'last_letter': word[-1]}


labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
                 [(name, 'female') for name in names.words('female.txt')])

random.shuffle(labeled_names)

# we use the feature extractor to process the names data.
featuresets = [(gender_features(n), gender)
               for (n, gender)in labeled_names]

# Divide the resulting list of feature
# sets into a training set and a test set.
train_set, test_set = featuresets[500:], featuresets[:500]

# The training set is used to
# train a new "naive Bayes" classifier.
classifier = nltk.NaiveBayesClassifier.train(train_set)


class Sentiment(Resource):
    def post(self):
        postedData = request.get_json()

        twitter = postedData['twitters']

        data = []
        data1 = []
        topic = twitter
        topicname = topic
        # input Number Search Terms
        noOfSearchTerms = 3200
        pubic_tweets = api.search(
            q=topicname, lang="en", count=noOfSearchTerms, tweet_mode="extended")
        positive = 0
        negative = 0
        neutral = 0

        for tweet in pubic_tweets:
            timestamp = tweet.created_at
            followers_count = tweet.user.followers_count
            location = tweet.user.location
            name = tweet.user.name
            verified = tweet.user.verified
            created_at = tweet.user.created_at
            description = tweet.user.description
            text = tweet.full_text
            cleanedTweet = clean_tweets(text)
            analysis = TextBlob(cleanedTweet)
            age = int(((timestamp - created_at).days / 365.25)+20)
            gender = classifier.classify(gender_features(name))
            print(analysis.sentiment)
            polarity = 'Negative'
            if analysis.sentiment.polarity > 0.2:
                polarity = 'Positive'
            if -0.2 <= analysis.sentiment.polarity <= 0.2:
                polarity = 'Neutral'
            dic = {'Tweet': cleanedTweet, 'Sentiment': polarity, 'Polarity': analysis.sentiment.polarity,
                   'Subject': analysis.sentiment.subjectivity}
            dic1 = {'Sentiment': polarity, 'Followers': followers_count, 'Location': location,
                    'Name': name, 'Verified': verified, 'Description': description, 'Age': age, 'Gender': gender}
            data.append(dic)
            data1.append(dic1)
            if analysis.sentiment.polarity > 0.2:
                positive += 1
            if -0.2 <= analysis.sentiment.polarity <= 0.2:
                neutral += 1
            if analysis.sentiment.polarity < -0.2:
                negative += 1
        #df = pd.DataFrame(data)
        df1 = pd.DataFrame(data1)
        df1["Location"].fillna("USA", inplace=True)
        df1["Description"].fillna("No thing to say", inplace=True)
        df1.to_csv('tweetdash.csv', index=False)
        file = open("tweetdash.csv", encoding="utf8")
        dict_reader = csv.DictReader(file)
        json_data = json.dumps(list(dict_reader))

        retJson = {
            "status": 200,
            "message": "Succesfuly signed up for this api",
            "data": json.loads(json_data),
            "response": {
                "twitter": twitter,
            }
        }

        return jsonify(retJson)