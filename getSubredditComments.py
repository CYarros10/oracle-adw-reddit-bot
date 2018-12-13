#!/usr/bin/python
import praw
import re
import random
import mysql.connector
import datetime
import cx_Oracle as co
import pandas as pd
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
import sys


def remove_emoji(comment):
    emoji_pattern = re.compile("["
       u"\U0001F600-\U0001F64F"  # emoticons
       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
       u"\U0001F680-\U0001F6FF"  # transport & map symbols
       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
       u"\U00002702-\U00002f7B0"
       u"\U000024C2-\U0001F251"
       "]+", flags=re.UNICODE)

    cleaned_comment =  emoji_pattern.sub(r'', comment)

    return cleaned_comment

def get_comment_sentiment(comment):

    tb = Blobber(analyzer=NaiveBayesAnalyzer())

    pattern_analysis = TextBlob(comment)
    naives_analysis = tb(comment)
    return [pattern_analysis.sentiment, naives_analysis.sentiment]

if len(sys.argv) == 2:
    try:
        sr = sys.argv[1]
        connection = co.connect('CY', 'WElcome_123#', 'ChallengeADW_high')
        cursor = connection.cursor()

        insertStatement = ("INSERT INTO RedditComments (comment_id, term, subreddit, author, r_comment, r_date, pattern_polarity, naivesbayes_positive) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)")

        reddit = praw.Reddit('bot1')
        term = sr + " user "
        subreddit = reddit.subreddit(sr)

        for comment in subreddit.stream.comments():
            print("====================================")
            print("ID: ", comment.id)
            print("Author: ", comment.author)
            cleaned_comment = remove_emoji(str(comment.body))
            comment_date = str(datetime.datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'))
            sentiment = get_comment_sentiment(cleaned_comment)
            pattern_polarity = sentiment[0].polarity
            naivesbayes_positive = sentiment[1].p_pos
            print("Body: ", cleaned_comment)
            try:
                data = [str(comment.id), term, str(subreddit),str(comment.author), cleaned_comment, comment_date, pattern_polarity, naivesbayes_positive]
                cursor.execute(insertStatement, data)
                connection.commit()
            except Exception as e:
                print("----- Error inserting into database ------")
                print (e)
                print("------------------------------------------")

        cursor.close()
        cnx.close()
    except Exception as e:
        print(e)
else:
    print("please enter subreddit.")
