from twscrape import API, gather
from twscrape.logger import set_log_level
from typing import List

from .config import *

async def get_profile(api:API, user_id:str, limit:int=20):
    try:
        user = await api.user_by_id(user_id)
    except:
        user = {}
    try:
        followers = await gather(api.followers(user_id, limit=limit))
    except:
        followers = []
    try:
        following = await gather(api.following(user_id, limit=limit))
    except:
        following = []
    try:
        tweets = await gather(api.user_tweets(user_id, limit=limit))
    except:
        tweets = []

    return user_id, dict(
        user=user,
        follower=followers,
        following=following,
        tweet=tweets
    )

async def run(api:API, users: List, limit:int=LIMIT):
    # change log level, default info
    set_log_level("DEBUG")

    profiles = {}
    for uid in users:
        user_id, profile = await get_profile(api, uid, limit)
        profiles[str(user_id)] = profile
    
    return profiles

    

