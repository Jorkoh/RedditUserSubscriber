import praw
import os


def reddit_login():
    print("Logging into Reddit..")

    reddit = praw.Reddit(username=os.environ['username'],
                         password=os.environ['password'],
                         client_id=os.environ['client_id'],
                         client_secret=os.environ['client_secret'],
                         user_agent='UserSubscriberBot by /u/Kohru')

    print("Logged into Reddit!")
    return reddit
