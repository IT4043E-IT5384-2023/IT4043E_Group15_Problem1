import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from typing import List, Dict
import json

from .config import *
from .get_uids import run as get_uids
from .get_profiles import run as get_profiles

def save_uids(uids: List, path:str=UID_PATH):
    with open(path, 'w') as f:
        json.dump(uids, f, ensure_ascii=False, indent=4)
    print(f"[UID] Crawl {len(uids)} UIDs succesfully!")

def add_profiles(profiles:Dict, cur_idx, path:str=PROFILE_PATH):
    with open(path, 'r+') as f:
        data = json.load(f)
        data.update(profiles)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[Profile] Scrape users from {cur_idx} to {cur_idx+BATCH_SIZE} succesfully!")

def update_log(cur_idx, path:str=LOG_PATH):
    with open(path, 'r+') as f:
        log = json.load(f)
        log["cursor_idx"] = cur_idx + BATCH_SIZE
        f.seek(0)
        json.dump(log, f, ensure_ascii=False, indent=4)

async def main(keywords:str=KEYWORDS, n_tweets:int=N_TWEETS, limit:int=LIMIT):
    api = API(ACCOUNT_DB_PATH)  # or API("path-to.db") - default is `accounts.db`

    # LOGIN ACCOUNTS (for CLI usage see BELOW)
    await api.pool.login_all()

    # Crawl UIDs
    uids = await get_uids(api, keywords, n_tweets)
    save_uids(uids)

    # Scrape profiles
    for i in range(0, len(uids), BATCH_SIZE):
        profiles = await get_profiles(api, uids[i:i+BATCH_SIZE], limit)
        add_profiles(profiles, i, UID_PATH)
        update_log(i+BATCH_SIZE, LOG_PATH)