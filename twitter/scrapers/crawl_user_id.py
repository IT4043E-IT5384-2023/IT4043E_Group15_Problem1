import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from typing import List
import json
import os 
from config import LIMIT, ACCOUNT_DB_PATH

async def get_user_id(api:API, keyword:str, limit:int=20):
    tweets = await gather(api.search(keyword, limit=20)) 
    user_ids = list(set([tweet.user.id_str for tweet in tweets]))
    return user_ids

async def main(keywords=['bitcoin', 'DeFi', 'crypto'], limit:int=LIMIT):
    api = API(ACCOUNT_DB_PATH)  # or API("path-to.db") - default is `accounts.db`

    # LOGIN ACCOUNTS (for CLI usage see BELOW)
    await api.pool.login_all()

    # change log level, default info
    set_log_level("DEBUG")
    profiles = []
    for keyword in keywords:
        user_ids = await get_user_id(api, keyword, limit)
        profiles += user_ids
    
    profiles = list(set(list(profiles)))
    print(profiles)
    with open("user_ids.json", 'w') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    return profiles
    

if __name__ == "__main__":
    asyncio.run(main())