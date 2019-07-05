import os
from datetime import datetime, timedelta

from Scripts import login

#TODO: Include posts
#TODO: Create other acc to get notifications
#TODO: Filter by subreddit
#TODO: Test on Heroku

def get_minimum_utc():
    return (datetime.now() - timedelta(days=int(os.environ["activity_age_days"]))).timestamp()


def get_redditors():
    return [reddit.redditor(username) for username in os.environ["subscribed_redditors"].split(", ")]


def get_comments_from_redditor(redditor, minimum_utc):
    redditor_comments = []
    for comment in [comment for comment in redditor.comments.new(limit=None)]:
        if comment.created_utc < minimum_utc:
            break
        redditor_comments.append(comment)
    return redditor_comments


def compose_message(redditors_and_comments):
    message = ""
    for redditor_and_comments in redditors_and_comments:
        redditor = redditor_and_comments[0]
        comments = redditor_and_comments[1]
        if len(comments) > 0:
            message += f"**{redditor}** activity the last {os.environ['activity_age_days']} day(s):"
            for comment in comments:
                message += f"\n\n* {comment.permalink}"
            message += "\n\n"
        else:
            message += f"**{redditor}** has not posted the last {os.environ['activity_age_days']} day(s).\n\n"
    return message


def run_script():
    minimum_utc = get_minimum_utc()
    redditors_and_comments = []
    for redditor in get_redditors():
        redditors_and_comments.append((redditor, get_comments_from_redditor(redditor, minimum_utc)))
    message = compose_message(redditors_and_comments)
    reddit.user.me().message("This is a test", message)


if __name__ == "__main__":
    reddit = login.login()
    run_script()
