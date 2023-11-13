from twscrape import API, gather
from twscrape.logger import set_log_level
from typing import List
from .config import *

async def get_user_ids(api:API, keyword:str, limit:int=20):
    tweets = await gather(api.search(keyword, limit=limit)) 
    user_ids = list(set([tweet.user.id_str for tweet in tweets]))
    return user_ids

async def run(api:API, keywords:str=KEYWORDS, limit:int=N_TWEETS):
    # change log level, default info
    set_log_level("DEBUG")

    user_ids = []
    for keyword in keywords:
        user_id = await get_user_ids(api, keyword, limit//len(keywords))
        user_ids += user_id
    
    user_ids = list(set(user_ids))
    return user_ids