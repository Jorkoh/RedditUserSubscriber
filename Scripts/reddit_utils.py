import praw
import os


def reddit_login():
    print("Logging into Reddit..")

    reddit = praw.Reddit(username=os.environ['USERNAME'],
                         password=os.environ['PASSWORD'],
                         client_id=os.environ['CLIENT_ID'],
                         client_secret=os.environ['CLIENT_SECRET'],
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


def get_comments_from_redditor(redditor, subreddits, minimum_utc):
    redditor_comments = []
    for comment in redditor.comments.new(limit=None):
        # Messages are ordered by post datetime from most recent, when minimum is reached ignore the rest
        if comment.created_utc < minimum_utc:
            break
        if comment.subreddit.display_name in subreddits:
            redditor_comments.append(comment)
    return redditor_comments


def get_submissions_from_redditor(redditor, subreddits, minimum_utc):
    redditor_submissions = []
    for submission in redditor.submissions.new(limit=None):
        # Messages are ordered by post datetime from most recent, when minimum is reached ignore the rest
        if submission.created_utc < minimum_utc:
            break
        if submission.subreddit.display_name in subreddits:
            redditor_submissions.append(submission)
    return redditor_submissions
