from .clean_data import clean_tweets, clean_users, load_profile
from ..config import CLEAN_USER_PATH, CLEAN_TWEET_PATH, PROFILE_PATH, PROCESS_USER_PATH, PROCESS_TWEET_PATH, PROCESS_DATA_PATH
from .preprocess_data import preprocess_tweets, preprocess_users, merge_data

import pandas as pd

def clean_data(dry_run: bool = True):
    profiles = load_profile(PROFILE_PATH)
    
    df_user = clean_users(profiles)
    df_tweet = clean_tweets(profiles)

    if not dry_run:
        df_user.to_csv(CLEAN_USER_PATH, index=False)
        df_tweet.to_csv(CLEAN_TWEET_PATH, index=False)
    
    return df_user, df_tweet

def preprocess_data(dry_run: bool = True):
    df_tweet = pd.read_csv(CLEAN_TWEET_PATH)
    df_user = pd.read_csv(CLEAN_USER_PATH)

    df_tweet = preprocess_tweets(df_tweet)
    df_user = preprocess_users(df_user)

    df_processed = merge_data(df_user, df_tweet)

    if not dry_run:
        df_processed.to_csv(PROCESS_DATA_PATH, index=False)
        df_user.to_csv(PROCESS_USER_PATH, index=False)
        df_tweet.to_csv(PROCESS_TWEET_PATH, index=False)

    return df_processed