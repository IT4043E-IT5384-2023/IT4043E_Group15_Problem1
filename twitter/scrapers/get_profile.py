import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from typing import List

from .config import LIMIT, ACCOUNT_DB_PATH

async def get_profile(api:API, user_id:str, limit:int=20):
    followers = await gather(api.followers(user_id, limit=limit))  # list[User]
    following = await gather(api.following(user_id, limit=limit))  # list[User]
    tweets = await gather(api.user_tweets(user_id, limit=limit))  # list[Tweet]

    return user_id, dict(
        follower=followers,
        following=following,
        tweet=tweets
    )

async def run(users: List, limit:int=LIMIT):
    api = API(ACCOUNT_DB_PATH)  # or API("path-to.db") - default is `accounts.db`

    # LOGIN ACCOUNTS (for CLI usage see BELOW)
    await api.pool.login_all()

    # change log level, default info
    set_log_level("DEBUG")

    profiles = {}
    async for user in users:
        user_id, profile = await get_profile(api, user.id, limit)
        profiles[str(user_id)] = profile
    
    return profiles

    
