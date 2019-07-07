# Reddit User Subscriber

Are you interested in a particular redditor contributions to a certain subreddit but don't care about what they have to say in others? Me too, that's why I made this bot.

I frequent [r/AndroidDev](https://www.reddit.com/r/androiddev/), a section of [Reddit](https://en.wikipedia.org/wiki/Reddit) where people share news, articles, libraries and opinions about Android application development. As I got to know the community I started to notice some developers making consistent contributions (e.g [u/JakeWharton](https://www.reddit.com/user/JakeWharton), [u/VasiliyZukanov](https://www.reddit.com/user/VasiliyZukanov) or [u/Zhuinden](https://www.reddit.com/user/Zhuinden)).

While Reddit offers [a function](https://www.reddit.com/r/friends/) similar to Twitter's *follow* there is no easy way to filter user activity by subreddit. This means that their [r/AndroidDev](https://www.reddit.com/r/androiddev/) comments got mixed with posts to other communities rendering that feature useless.

With this bot you can subscribe to multiple redditors of a subreddit and recieve a list of their recent posts and comments directly into your inbox every few days.

⚠️ **I'm not currently hosting this bot. See [Installation](#installation) to run your own version** ⚠️

# Available commands

You can interact with the bot by sending him a DM. If you are logged into Reddit clicking the command name will compose the message automatically:

| [Check current subscriptions](https://www.reddit.com/message/compose/?to=UserSubscriberBot&subject=Check+subscriptions&message=.)  | [Add subscriptions](https://www.reddit.com/message/compose/?to=UserSubscriberBot&subject=Add+subscriptions&message=Subreddit:+ExampleSubreddit%0ARedditors:+ExampleRedditor1,+ExampleRedditor2,+ExampleRedditor3) | [Remove subscriptions](https://www.reddit.com/message/compose/?to=UserSubscriberBot&subject=Remove+subscriptions&message=Subreddit:+ExampleSubreddit%0ARedditors:+ExampleRedditor1,+ExampleRedditor2,+ExampleRedditor3) |
| ------------- | ------------- | ------------- |
| ![CheckSubscriptions](/readme-resources/CheckSubscriptions.png)  | ![AddSubscriptions](/readme-resources/AddSubscriptions.png) | ![RemoveSubscriptions](/readme-resources/RemoveSubscriptions.png) |

# Installation

This bot can be run locally or hosted in multiple services. This guide will cover how to run it on Heroku (for free).

1. Make an account on [Heroku](https://www.heroku.com/) and create a new, empty app.

2. [Fork](https://help.github.com/en/articles/fork-a-repo) this repository into your own GitHub account.

3. Set up Github as the deployment method on Heroku.
```
Heroku > Select your App > Deploy > Deployment Method > Connect to GitHub > Select your GitHub repo
```

4. Add *mLab MongoDB* and *Heroku Scheduler* as add-ons (choose free tier) to your Heroku application
```
Heroku > Select your App > Resources > Add-ons
```

5. Add a new collection to the MongoDB instance named "Users". It will hold a document for each user of the bot with their subscriptions information.
```
Heroku > Select your App > Resources > Add-ons > access mLab MongoDB > Add collection
```
6. Add another collection named "Counters". This is a workaround for Heroku limitations on its scheduler add-on. Add a document to this collection with this content:
```
{
    "_id": 1,
    "name": "daysSinceLastSend",
    "days": 0
}
```

7. Create a Reddit user and application for the bot. Don't use your personal Reddit account or you won't receive alerts for the feed messages. To create the Reddit application, once logged in, simply [click here](https://www.reddit.com/prefs/apps/) and select the type *script*. *Redirect uri* won't be used so just input "http://localhost:8080".

8. Try sending a DM from the bot Reddit account, it may ask for a CAPTCHA the first time to unlock the feature.

9. Prepare the config vars on Heroku on your application dashboard > Settings > Config Vars. You will need:
   * **USERNAME**. The username of the Reddit account.
   * **PASSWORD**. The password of the Reddit account.
   * **CLIENT_ID**. The client ID is the 14 character string listed just under “personal use script” on the Reddit application.
   * **CLIENT_SECRET**. The client secret is the 27 character string listed adjacent to secret on the Reddit application.
   * **SEND_PERIOD_DAYS**. Integer, will be how often the subscription feeds are sent. For example choose "3" if you would like to receive the DM every three days.
   * **MONGODB_URI**. This one should already exist, don't touch it.

10. Configure the schedulers that will run the scripts:
```
Heroku > Select your App > Resources > Add-ons > access Heroku Scheduler > Create job
```
   * Create one with the command "*python Scripts/script_process_requests.py*" running every 10 mins, hourly or daily. The more frequently it runs the faster the bot will respond to DMs but you risk running out of free dyno hours on Heroku. This won't be a problem if this is your only app on the Heroku account.
   * Create another with the command "*python Scripts/script_send_feeds.py*" running daily. It won't actually send feeds every day, don't worry.
