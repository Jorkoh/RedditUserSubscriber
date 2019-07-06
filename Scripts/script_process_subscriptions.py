import os
from datetime import datetime, timedelta

from Scripts import reddit_utils, mongodb_utils


def manage_new_subscription(message):
    try:
        print(f"Adding new subscriptions for {message.author.name}")

        lines = message.body.split("\n")
        # Add validations for subreddit and redditors
        subreddit = lines[0][11:]
        redditors = lines[1][11:].split(', ')

        user = mongodb_utils.get_user(db, message.author.name)
        new_subscriptions_counter = 0
        for redditor in redditors:
            subscription = {'username': redditor, 'subreddit': subreddit}
            if subscription not in user['subscriptions']:
                user['subscriptions'].append(subscription)
                new_subscriptions_counter += 1
        mongodb_utils.persist_user(db, user)

        print(f"Added {new_subscriptions_counter} new subscriptions for {message.author.name}")
    except:
        # Make this more specific
        message.reply('Wrong formatting, check how this bot works '
                      'at [github](https://github.com/Jorkoh/RedditUserSubscriber)')


def manage_unrecognized_message(message):
    message.reply('Command not recognized, check how this bot works '
                  'at [github](https://github.com/Jorkoh/RedditUserSubscriber)')


def run_script():
    unread_messages = []
    for new_message in reddit.inbox.unread(limit=None):
        unread_messages.append(new_message)

        if new_message.subject == "New subscription":
            manage_new_subscription(new_message)
        else:
            manage_unrecognized_message(new_message)
    reddit.inbox.mark_read(unread_messages)


if __name__ == "__main__":
    db = mongodb_utils.login()
    reddit = reddit_utils.reddit_login()
    run_script()
