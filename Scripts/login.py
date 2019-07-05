import praw
import os


def login():
    print("Logging in..")
    reddit = praw.Reddit(username=os.environ["username"],
                         password=os.environ["password"],
                         client_id=os.environ["client_id"],
                         client_secret=os.environ["client_secret"],
                         user_agent="testscript by /u/Kohru")
    print("Logged in!")
    return reddit
