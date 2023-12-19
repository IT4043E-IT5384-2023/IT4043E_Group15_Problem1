from .clean_data import clean_tweets, clean_users, load_profile
from ..config import CLEAN_USER_PATH, CLEAN_TWEET_PATH, PROFILE_PATH

def clean_data(dry_run: bool = True):
    profiles = load_profile(PROFILE_PATH)
    
    df_user = clean_users(profiles)
    df_tweet = clean_tweets(profiles)

    if not dry_run:
        df_user.to_csv(CLEAN_USER_PATH, index=False)
        df_tweet.to_csv(CLEAN_TWEET_PATH, index=False)
