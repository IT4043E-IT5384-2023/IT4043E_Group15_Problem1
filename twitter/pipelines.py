from .data_processing import clean_tweets, clean_users, load_profile
from .data_processing import preprocess_users, preprocess_tweets, merge_data
from .ml import Model, encode_data, load_data, interpret_label
from .config import CLEAN_USER_PATH, CLEAN_TWEET_PATH, PROCESS_DATA_PATH, PROCESS_USER_PATH, PROCESS_TWEET_PATH
from .config import PROFILE_PATH, RESULT_DIR

from typing import List, Dict, Union, Tuple
import pandas as pd
import numpy as np
import json

def _clean_pipe(
    profiles: Union[str, pd.DataFrame] = PROFILE_PATH,
    memory_to_disk: bool = False
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if isinstance(profiles ,str):
        profiles = load_profile(profiles)
    
    df_user = clean_users(profiles)
    df_tweet = clean_tweets(profiles)

    if memory_to_disk:
        df_user.to_csv(CLEAN_USER_PATH, index=False)
        df_tweet.to_csv(CLEAN_TWEET_PATH, index=False)
    
    return df_user, df_tweet

def _preprocess_pipe(
    df_user: Union[str, pd.DataFrame] = CLEAN_USER_PATH,
    df_tweet: Union[str, pd.DataFrame] = CLEAN_TWEET_PATH,
    memory_to_disk: bool = False
) -> pd.DataFrame:
    if isinstance(df_user ,str):
        df_user = load_profile(df_user)
    if isinstance(df_tweet ,str):
        df_tweet = load_profile(df_tweet)
    
    df_tweet = preprocess_tweets(df_tweet)
    df_user = preprocess_users(df_user)
    data = merge_data(df_user, df_tweet)

    if memory_to_disk:
        data.to_csv(PROCESS_DATA_PATH, index=False)
        df_user.to_csv(PROCESS_USER_PATH, index=False)
        df_tweet.to_csv(PROCESS_TWEET_PATH, index=False)

    return data

def _transform_pipe(
    data: Union[pd.DataFrame, str] = PROCESS_DATA_PATH,
    eval_only: bool = True
):
    Xl, yl, Xu, yu = load_data(data)

    if len(Xl) > 0 and not eval_only:
        Xl, yl = encode_data(Xl, yl)

    if len(Xu) > 0:
        Xu, yu = encode_data(Xu, yu)

    return Xl, yl, Xu, yu

def assembly_pipe(
    model: Model = Model(),
    twitter_data: str = PROFILE_PATH,
    memory_to_disk: bool = False,
    infer_only: bool = True,
    scoring: str = "roc_auc_ovo"      
) -> Dict:
    df_user, df_tweet = _clean_pipe(twitter_data, memory_to_disk)
    data = _preprocess_pipe(df_user, df_tweet, memory_to_disk)
    Xl, yl, Xu, _ = _transform_pipe(data, infer_only)

    log = {}

    if not infer_only:
        model.train(Xl, yl)
        score = model.eval(Xl, yl, scoring=scoring)
        log["eval"] = {
            "score": score,
            "type": scoring
        }

    yu_pred = model.infer(Xu)
    log["inference"] = {
        "user_id": data["user_id"].tolist(),
        "user_name": data["username"].tolist(),
        "label": interpret_label(yu_pred).tolist()
    }

    with open(RESULT_DIR, "w") as f:
        json.dump(log, f, indent=4)

    return log

