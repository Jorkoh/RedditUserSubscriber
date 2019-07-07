import os
from datetime import datetime, timedelta

from Scripts import reddit_utils, mongodb_utils


def current_subscriptions_message(username):
    user = mongodb_utils.get_user(db, username)
    message = "Current subscriptions:\n\nRedditor | Subreddit\n---|---"
    for subscription in user['subscriptions']:
        message += f"\n{subscription['username']} | {subscription['subreddit']}"
    return message


def manage_check_subscriptions(message):
    message.reply(current_subscriptions_message(message.author.name))
    print(f"Checked subscriptions for {message.author.name}")


def manage_add_subscriptions(message):
    try:
        username = message.author.name

        lines = message.body.split("\n")
        # Add validations for subreddit and redditors
        subreddit = lines[0][11:]
        redditors = lines[1][11:].split(', ')

        user = mongodb_utils.get_user(db, username)
        new_subscriptions_counter = 0
        for redditor in redditors:
            subscription = {'username': redditor, 'subreddit': subreddit}
            if subscription not in user['subscriptions']:
                user['subscriptions'].append(subscription)
                new_subscriptions_counter += 1
        mongodb_utils.persist_user(db, user)

        print(f"Added {new_subscriptions_counter} new subscriptions for {username}")

        message.reply(f"Added {new_subscriptions_counter} new subscription(s).\n\n"
                      f"{current_subscriptions_message(username)}")
    except:
        # Make this more specific
        message.reply("Wrong formatting, check how this bot works "
                      "at [github](https://github.com/Jorkoh/RedditUserSubscriber)")


def manage_remove_subscriptions(message):
    try:
        username = message.author.name

        lines = message.body.split("\n")
        # Add validations for subreddit and redditors
        subreddit = lines[0][11:]
        redditors = lines[1][11:].split(', ')

        user = mongodb_utils.get_user(db, username)
        removed_subscriptions_counter = 0
        for redditor in redditors:
            subscription = {'username': redditor, 'subreddit': subreddit}
            if subscription in user['subscriptions']:
                user['subscriptions'].remove(subscription)
                removed_subscriptions_counter += 1
        mongodb_utils.persist_user(db, user)

        print(f"Removed {removed_subscriptions_counter} subscriptions for {username}")

        message.reply(f"Removed {removed_subscriptions_counter} subscription(s).\n\n"
                      f"{current_subscriptions_message(username)}")
    except:
        # Make this more specific
        message.reply("Wrong formatting, check how this bot works "
                      "at [github](https://github.com/Jorkoh/RedditUserSubscriber)")


def manage_unrecognized_message(message):
    message.reply('Command not recognized, check how this bot works '
                  'at [github](https://github.com/Jorkoh/RedditUserSubscriber)')


def run_script():
    unread_messages = []
    for new_message in reddit.inbox.unread(limit=None):
        unread_messages.append(new_message)

        if new_message.subject == "Add subscriptions":
            manage_add_subscriptions(new_message)
        elif new_message.subject == "Check subscriptions":
            manage_check_subscriptions(new_message)
        elif new_message.subject == "Remove subscriptions":
            manage_remove_subscriptions(new_message)
        else:
            manage_unrecognized_message(new_message)
    reddit.inbox.mark_read(unread_messages)


if __name__ == "__main__":
    db = mongodb_utils.login()
    reddit = reddit_utils.reddit_login()
    run_script()
