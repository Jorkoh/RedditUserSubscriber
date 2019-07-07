import os
from datetime import datetime, timedelta
from itertools import groupby
from prawcore.exceptions import NotFound

from Scripts import reddit_utils, mongodb_utils

SEND_PERIOD_DAYS = int(os.environ["SEND_PERIOD_DAYS"])


def get_minimum_utc():
    return (datetime.now() - timedelta(days=SEND_PERIOD_DAYS)).timestamp()


def compose_message(redditors_and_comments):
    message = ""
    for redditor_and_comments in redditors_and_comments:
        redditor = redditor_and_comments[0]
        comments = redditor_and_comments[1]
        submissions = redditor_and_comments[2]
        # Composing submissions
        if len(submissions) > 0:
            message += f"**{redditor}** posts:"
            for submission in submissions:
                message += f"\n\n* {reddit_utils.shorten_submission_permalink(submission.permalink)}"
            message += "\n\n"
        else:
            message += f"**{redditor}** has not posted.\n\n"
        # Composing comments
        if len(comments) > 0:
            message += f"**{redditor}** comments:"
            for comment in comments:
                message += f"\n\n* {reddit_utils.shorten_comment_permalink(comment.permalink)}"
            message += "\n\n"
        else:
            message += f"**{redditor}** has not commented.\n\n"
        message += "---\n\n"
    return message


def send_message(redditors_activity, subscription_removed, username):
    message = compose_message(redditors_activity)
    if subscription_removed:
        message += "One or more subscriptions have been removed because the redditor doesn't exist."
    destination = reddit.redditor(username)
    destination.message(f"Subscribed redditors activity the last {SEND_PERIOD_DAYS} day(s)", message)
    print(f"Sent subscription message for {username}")


def run_script():
    minimum_utc = get_minimum_utc()
    # For each user group its subscriptions into redditors and query their activity, compose and send the message
    for user in mongodb_utils.get_users(db):
        redditors_activity = []
        subscription_removed = False
        for redditor_username, subscriptions_by_redditor in groupby(user['subscriptions'], lambda x: x['username']):
            subscription_removed = False
            redditor = reddit.redditor(redditor_username)
            subscriptions = list(subscriptions_by_redditor)
            subreddits = [subscription['subreddit'] for subscription in subscriptions]
            try:
                redditors_activity.append((
                    redditor,
                    reddit_utils.get_comments_from_redditor(redditor, subreddits, minimum_utc),
                    reddit_utils.get_submissions_from_redditor(redditor, subreddits, minimum_utc)))
            # If we got a 404 querying the comments or submissions the redditor doesn't exist, let's
            # remove the subscriptions that share this redditor and persist the new user subscriptions
            except NotFound:
                user['subscriptions'] = [e for e in user['subscriptions'] if e not in subscriptions]
                mongodb_utils.persist_user(db, user)
                subscription_removed = True
        send_message(redditors_activity, subscription_removed, user['username'])


if __name__ == "__main__":
    db = mongodb_utils.login()
    if mongodb_utils.is_time_to_send_feeds(db):
        reddit = reddit_utils.reddit_login()
        run_script()
