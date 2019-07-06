import os
from datetime import datetime, timedelta
from itertools import groupby

from Scripts import reddit_utils, mongodb_utils

# TODO: Include posts
# TODO: Test on Heroku

activity_age_days = int(os.environ["activity_age_days"])


def get_minimum_utc():
    return (datetime.now() - timedelta(days=activity_age_days)).timestamp()


def comment_passes_filters(comment, subreddits):
    return comment.subreddit.display_name in subreddits


def get_comments_from_redditor(redditor, subreddits, minimum_utc):
    redditor_comments = []
    for comment in [comment for comment in redditor.comments.new(limit=None)]:
        # Messages are ordered by post datetime from most recent, when minimum is reached ignore the rest
        if comment.created_utc < minimum_utc:
            break
        if comment_passes_filters(comment, subreddits):
            redditor_comments.append(comment)
    return redditor_comments


def shorten_comment_permalink(permalink):
    # Some elements of the permalink can be safely removed to keep the DM below the 10k character limit
    elements = permalink.split('/')
    del elements[0]
    del elements[-1]
    elements[-2] = ""
    return '/'.join(elements)


def compose_message(redditors_and_comments):
    message = ""
    for redditor_and_comments in redditors_and_comments:
        redditor = redditor_and_comments[0]
        comments = redditor_and_comments[1]
        if len(comments) > 0:
            message += f"**{redditor}** activity:"
            for comment in comments:
                message += f"\n\n* {shorten_comment_permalink(comment.permalink)}"
            message += "\n\n"
        else:
            message += f"**{redditor}** has not posted.\n\n"
    return message


def run_script():
    minimum_utc = get_minimum_utc()

    for user in mongodb_utils.get_users(db):
        redditors_and_comments = []
        for redditor_username, subscriptions in groupby(user['subscriptions'], key=lambda x: x['username']):
            redditor = reddit.redditor(redditor_username)
            subreddits = [subscription['subreddit'] for subscription in subscriptions]
            redditors_and_comments.append((redditor, get_comments_from_redditor(redditor, subreddits, minimum_utc)))
        message = compose_message(redditors_and_comments)
        destination = reddit.redditor(user['username'])
        destination.message(f"Subscribed redditors activity the last {activity_age_days} day(s)", message)


if __name__ == "__main__":
    db = mongodb_utils.login()
    reddit = reddit_utils.reddit_login()
    run_script()
