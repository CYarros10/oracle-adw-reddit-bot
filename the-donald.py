#!/usr/bin/python
import praw
import re
import random
import pymysql
import datetime

def remove_emoji(comment):
    emoji_pattern = re.compile("["
       u"\U0001F600-\U0001F64F"  # emoticons
       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
       u"\U0001F680-\U0001F6FF"  # transport & map symbols
       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
       u"\U00002702-\U000027B0"
       u"\U000024C2-\U0001F251"
       "]+", flags=re.UNICODE)

    cleaned_comment =  emoji_pattern.sub(r'', comment)

    return cleaned_comment

# Connect to the database
cnx = pymysql.connect(host='localhost',
                             user='redditbot',
                             password='pennstate88',
                             db='reddit',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


cursor = cnx.cursor()

add_comment = ("INSERT INTO redditcomments "
               "(commentid, term, subreddit, author, comment, submitdate)"
               " VALUES (%s, %s, %s, %s, %s, %s)")

reddit = praw.Reddit('bot1')
term = "the_donald"
subreddit = reddit.subreddit("the_donald")

for comment in subreddit.stream.comments():
            print("====================================")
            print("ID: ", comment.id)
            #print("Body: ", comment.body)
            print("Author: ", comment.author)
            cleaned_comment = remove_emoji(str(comment.body))
            print("Body: ", cleaned_comment)
            try:
                data_comment = (str(comment.id), term, str(subreddit),str(comment.author), cleaned_comment, str(datetime.datetime.now()))
                cursor.execute(add_comment, data_comment)
                cnx.commit()
            except:
                print("----- Error inserting into database ------")

cursor.close()
cnx.close()
