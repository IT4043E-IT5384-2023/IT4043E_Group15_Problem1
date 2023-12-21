import pandas as pd
import json
from typing import List
import pycountry_convert as pc

from ..config import LOCATION_PATH, MISSING_CN_TO_CNT


def country_to_continent(country_name: str) -> str:
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
    except:
        if country_name in ["Europe", "Africa", "Antarctica"]:
            return country_name
        return MISSING_CN_TO_CNT[country_name]

def load_profile(fpath: str) -> pd.DataFrame:
    profiles = pd.read_json(fpath)
    profiles = profiles.transpose()
    idxs = [i for i in range(len(profiles))]
    profiles.index = idxs
    return profiles

## --> USERS

def _extract_users(profiles: pd.DataFrame) -> pd.DataFrame:
    users = []
    for user in profiles["user"]:
        users.append(user)
    users = pd.DataFrame.from_records(users, index=profiles.index)
    return users

def _label_users(users: pd.DataFrame) -> List:
    '''Label by continent'''
    with open(LOCATION_PATH, "r") as f:
        location_dict = json.load(f)
    for k, v in location_dict.items():
        if v == "None":
            location_dict[k] = None

    location = []
    for i in range(users.shape[0]):
        k = users["location"][i]
        if k == "" or str(k) == "nan":
            location.append(None)
        else:
            v = location_dict[k]
            if isinstance(v, str):
                v = v.strip()
            location.append(v)

    for i, country in enumerate(location):
        if country is not None:
            location[i] = country_to_continent(country)
        else:
            location[i] = None
    
    return location

def clean_users(
    profiles: pd.DataFrame,
    drop_cols: List = ['profileImageUrl','profileBannerUrl','descriptionLinks','_type', 
                       'id_str','url','created', 'rawDescription', 'protected', 'blueType', 
                       'displayname'],
) -> pd.DataFrame:
    
    df_user = _extract_users(profiles)
    df_user = df_user.drop(columns=drop_cols, axis=1, inplace=False)
    df_user["location"] = _label_users(df_user)

    return df_user

### --> TWEETS

def _extract_tweets(profiles: pd.DataFrame) -> pd.DataFrame:
    tweets = []
    for twt_lst in profiles['tweet']:
        for tweet in twt_lst:
            tweets.append(tweet)
    tweets = pd.DataFrame.from_records(tweets)

    return tweets

def clean_tweets(
    profiles: pd.DataFrame,
    keep_cols: List = ["id", "user", "replyCount", "retweetCount", 
                       "likeCount", "quoteCount", "viewCount"]
) -> pd.DataFrame:
    
    df_tweet = _extract_tweets(profiles)

    df_tweet["user"] = df_tweet["user"].map(lambda x: x["id"])
    df_tweet = df_tweet[keep_cols]
    df_tweet.rename(columns={"user": "user_id"}, inplace=True)

    return df_tweet


