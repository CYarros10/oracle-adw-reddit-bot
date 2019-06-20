#!/usr/bin/python
import praw
import re
import random
import datetime
import cx_Oracle as co
import pandas as pd
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from better_profanity import profanity
import sys

tb = Blobber(analyzer=NaiveBayesAnalyzer())


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
    pattern_analysis = TextBlob(comment)
    naives_analysis = tb(comment)
    return [pattern_analysis.sentiment, naives_analysis.sentiment]


if len(sys.argv) >= 2:
    try:
        censored_comments = 0
        connection = co.connect("dbuser/WElcome_123#@gr1hb26xqe9aiee.cseiystga0o8.us-east-1.rds.amazonaws.com:1521/emp")
        cursor = connection.cursor()

        insertStatement = ("INSERT INTO RedditComments (comment_id, subreddit, author, r_comment, r_score, r_date, pattern_polarity, naivesbayes_positive) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)")

        r = praw.Reddit('bot1')


        # build stream. add first subreddit to start.
        subreddits = sys.argv[1]
        for sr in sys.argv[2:]:
            subreddits = subreddits + "+" + sr

        comment_stream = r.subreddit(subreddits)

        print(subreddits)

        for comment in comment_stream.stream.comments():
            print("====================================")
            print("Author: ", comment.author)
            print("Subreddit: ", comment.subreddit)

            if profanity.contains_profanity(str(comment.body)):
                censored_comments = censored_comments + 1
                print(censored_comments)

            cleaned_comment = profanity.censor((remove_emoji(str(comment.body))))
            comment_date = str(datetime.datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'))
            sentiment = get_comment_sentiment(cleaned_comment)
            pattern_polarity = round(sentiment[0].polarity,4)
            naivesbayes_positive = round(sentiment[1].p_pos,4)
            print("Body: ", cleaned_comment)
            try:
                data = [str(comment.id), str(comment.subreddit),str(comment.author), cleaned_comment, comment.score, comment_date, pattern_polarity, naivesbayes_positive]
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
