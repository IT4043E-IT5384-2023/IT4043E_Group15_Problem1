from typing import List

from pyspark.sql import DataFrame
import pyspark.sql.functions as F

class DataPreprocessor:
    def __init__(
        self,
        neglect_cols: List,
        join_cols: List,
    ):
        self.neglect_cols = neglect_cols
        self.join_cols = join_cols

    def __call__(
        self,
        cleaned_tweet_df: DataFrame,
        cleaned_user_df: DataFrame,
        fillna_num_tweet: int = 0,
        fillna_cat_tweet: str = "Unk",
        left_join_on_cols: List = ["user_id"],
    ) -> DataFrame:
        return self.integrate_data(self.preprocess_users(cleaned_user_df), self.preprocess_tweets(cleaned_tweet_df), 
                                   fillna_num_tweet, fillna_cat_tweet, left_join_on_cols)

    def preprocess_tweets(
        self,
        tweet_df: DataFrame,
    ) -> DataFrame:
        # drop unecessary fields for ML tasks
        tweet_df = tweet_df.select(*self.join_cols)
        
        # drop any-NULL rows
        tweet_df = tweet_df.na.drop()
        
        # agg. by user
        tweet_df = tweet_df.groupBy("user_id").agg(
            F.mean("replyCount").alias("replyCount"),
            F.mean("retweetCount").alias("retweetCount"),
            F.mean("likeCount").alias("likeCount"),
            F.mean("quoteCount").alias("quoteCount"),
            F.mean("viewCount").alias("viewCount"),
            F.mode("lang").alias("lang")
        )
        
        return tweet_df

    def preprocess_users(
        self,
        user_df: DataFrame,
    ) -> DataFrame:
        # drop rows with NaN values in columns other than "location"
        process_cols = [col_name for col_name in user_df.columns if col_name not in (["location"] + self.neglect_cols)]
        user_df = user_df.na.drop(subset=process_cols)
        
        return user_df
    
    def integrate_data(
        self,
        user_df: DataFrame,
        tweet_df: DataFrame,
        fillna_num: int,
        fillna_cat: str,
        left_join_on_cols: List
    ) -> DataFrame:
        # perform a left join on specified columns
        data_spark = user_df.join(tweet_df, on=left_join_on_cols, how='left')

        # replace NaN values in columns for tweets
        num_cols = [col_name for col_name in tweet_df.columns if col_name != "location" and col_name != "lang"]
        cat_cols = ["lang"]
        data_spark = data_spark.fillna(fillna_num, subset=num_cols)
        data_spark = data_spark.fillna(fillna_cat, subset=cat_cols)
                                
        return data_spark