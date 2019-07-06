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


def shorten_comment_permalink(permalink):
    # Some elements of the permalink can be safely removed to keep the DM below the 10k character limit
    elements = permalink.split('/')
    del elements[0]
    del elements[-1]
    elements[-2] = ""
    return '/'.join(elements)


def shorten_submission_permalink(permalink):
    # Some elements of the permalink can be safely removed to keep the DM below the 10k character limit
    elements = permalink.split('/')
    del elements[0]
    del elements[-1]
    return '/'.join(elements)
