import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from typing import List, Dict
import json

from .config import *
from .get_uids import run as get_uids
from .get_profiles import run as get_profiles

def load_uids(path:str=UID_PATH):
    with open(path, 'r') as f:
        uids = json.load(f)
    return uids

def save_uids(uids: List, path:str=UID_PATH):
    with open(path, 'w') as f:
        json.dump(uids, f, indent=4, default=str)
    print(f"[UID] Crawl {len(uids)} UIDs succesfully!")

def add_profiles(profiles:Dict, cur_idx, path:str=PROFILE_PATH):
    with open(path, 'r+') as f:
        data = json.load(f)
        data.update(profiles)
        f.seek(0)
        json.dump(data, f, indent=4, default=str)
    print(f"[Profile] Scrape users from {cur_idx} to {cur_idx+BATCH_SIZE} succesfully!")

def update_log(cur_idx, path:str=LOG_PATH):
    with open(path, 'r+') as f:
        log = json.load(f)
        log["cursor_idx"] = cur_idx
        f.seek(0)
        json.dump(log, f, indent=4)

def load_log(path:str=LOG_PATH):
    with open(path, 'r') as f:
        log = json.load(f)
    return int(log["cursor_idx"])

def main(
        keywords:str=KEYWORDS, 
        n_tweets:int=N_TWEETS, 
        limit:int=LIMIT,
        do_load_uids:bool=False
    ):
    api = API(ACCOUNT_DB_PATH)  # or API("path-to.db") - default is `accounts.db`

    # LOGIN ACCOUNTS (for CLI usage see BELOW)
    asyncio.run(api.pool.login_all())

    # Crawl UIDs
    if do_load_uids:
        uids = load_uids(UID_PATH)
    else:
        uids = asyncio.run(get_uids(api, keywords, n_tweets))
        save_uids(uids, UID_PATH)

    # Scrape profiles
    i = load_log(LOG_PATH)
    while i+BATCH_SIZE <= len(uids):
        profiles = asyncio.run(get_profiles(api, uids[i:i+BATCH_SIZE], limit))
        add_profiles(profiles, i, PROFILE_PATH)
        update_log(i+BATCH_SIZE, LOG_PATH)
        i += BATCH_SIZE
    if len(uids) % BATCH_SIZE != 0:
        profiles = asyncio.run(get_profiles(api, uids[i:-1], limit))
        add_profiles(profiles, i, PROFILE_PATH)
        update_log(len(uids), LOG_PATH)