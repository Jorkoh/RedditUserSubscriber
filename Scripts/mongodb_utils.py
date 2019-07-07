import pymongo
import os
from urllib.parse import urlsplit

from bson import ObjectId


def login():
    print("Logging into MongoDB..")

    url = os.environ['MONGODB_URI']
    parsed = urlsplit(url)
    db_name = parsed.path[1:]
    db = pymongo.MongoClient(url)[db_name]
    user, password = parsed.netloc.split('@')[0].split(':')
    db.authenticate(user, password)

    print("Logged into MongoDB!")
    return db


def is_time_to_send_feeds(db):
    db['Counters'].update({'name': "daysSinceLastSend"}, {"$inc": {"days": 1}})
    return db['Counters'].find_one({'name': "daysSinceLastSend"})["days"] == int(os.environ['SEND_PERIOD_DAYS'])


def get_users(db):
    return db['Users'].find()


def get_user(db, username):
    # If it doesn't exist just create a new one
    return db['Users'].find_one({"username": username}) or {"_id": str(ObjectId()),
                                                            "username": username,
                                                            "subscriptions": []}


def persist_user(db, user):
    db['Users'].replace_one({'_id': user['_id']}, user, upsert=True)
