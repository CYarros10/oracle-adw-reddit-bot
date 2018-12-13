#!/usr/bin/python
import praw
import re
import random
import mysql.connector
import datetime

cnx = mysql.connector.connect(user='RedditBot', password='test', host='localhost', database='TEST')
cursor = cnx.cursor()

add_comment = ("INSERT INTO RedditComments "
               "(term, subreddit, author, comment, date)"
               " VALUES (%s, %s, %s, %s, %s)")


reddit = praw.Reddit('bot1')
terms = ["Liverpool FC", "LFC", "Liverpool", "Chelsea FC", "Chelsea", "Man U", "Man Utd", "Manchester United"] 
subreddit = reddit.subreddit("soccer")
count = 0

for comment in subreddit.stream.comments():
    print(count)
    count = count + 1
    for term in terms:
        if re.search(term, comment.body, re.IGNORECASE):
            print("====================================")
            print("Term: ", term)
            print("Body: ", comment.body)
            print("Author: ", comment.author)
            data_comment = (term, str(subreddit),str(comment.author), str(comment.body), str(datetime.datetime.now()))
            cursor.execute(add_comment, data_comment)
            cnx.commit()

cursor.close()
cnx.close()
