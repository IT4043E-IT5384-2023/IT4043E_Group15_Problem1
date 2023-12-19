import pandas as pd
from typing import List

def preprocess_users(
    df_user: pd.DataFrame,
    drop_cols: List = ["verified"],
) -> pd.DataFrame:
    df_user = df_user[df_user["location"].notnull()]
    df_user = df_user.drop(columns=drop_cols, axis=1)
    df_user["blue"] = df_user["blue"].astype("int64")
    
    # for merging
    df_user.rename(columns={"id": "user_id"}, inplace=True)
    
    return df_user

def preprocess_tweets(
    df_tweet: pd.DataFrame
) -> pd.DataFrame:
    df_tweet = df_tweet.drop(columns=["id"], axis=1)
    df_tweet = df_tweet.dropna()
    df_tweet = df_tweet.groupby(["user_id"]).mean().reset_index()

    return df_tweet

def merge_data(
    df_user: pd.DataFrame, 
    df_tweet: pd.DataFrame,
    fill_none_tweet: int = 0,
    left_join_on_cols: List = ['user_id']
):
    data = pd.merge(df_user, df_tweet, 
                    how='left', on=left_join_on_cols)
    data.fillna(fill_none_tweet, inplace=True)
    return data
