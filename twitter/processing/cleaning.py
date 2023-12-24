from typing import Any, Union, Tuple
import json
from itertools import chain

from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from pyspark.sql import SparkSession

from ..config import LOCATION_PATH
from .utils import country_to_continent

class DataCleaner:
    def __init__(
        self,
        data: Union[str, DataFrame],
    ):
        if isinstance(data, str):
            data = self.load_raw_data(data)
        self.data = data
    
    @staticmethod
    def load_raw_data(spark: SparkSession, datapath: str) -> DataFrame:
        profile_df = spark.read.json(datapath)
        return profile_df

    def __call__(self) -> Tuple[DataFrame, DataFrame]:
        user_df = self.clean_users()
        tweet_df = self.clean_tweets()

        return user_df, tweet_df

    def _extract_users(self) -> DataFrame:
        user_df = self.data.select(F.col("user.*"))
        return user_df

    def _label_users(self, user_df: DataFrame) -> DataFrame:
        with open(LOCATION_PATH, "r") as f:
            location_dict = json.load(f)
        for k, v in location_dict.items():
            if isinstance(v , str):
                if v == "None":
                    v = None
                else:
                    v = v.strip()
            location_dict[k] = v        
        for unk_geo in ["nan", ""]:
            location_dict[unk_geo] = None
            
        country_encode_fn = F.create_map([F.lit(x) for x in chain(*location_dict.items())])
        user_df = user_df.withColumn("country", country_encode_fn[F.col("location")])
            
        for k, v in location_dict.items():
            if v is not None:
                location_dict[k] = country_to_continent(v)
            else:
                location_dict[k] = None
            
        label_encode_fn = F.create_map([F.lit(x) for x in chain(*location_dict.items())])
        user_df = user_df.withColumn("location", label_encode_fn[F.col("location")])
        
        return user_df

    def clean_users(self) -> DataFrame:
        # extract users from crawled data
        user_df = self._extract_users(self.data)
        
        # consistent & unique
        user_df = user_df \
                    .withColumnRenamed("id", "user_id") \
                    .dropDuplicates(['user_id'])
        user_df = user_df.na.drop(subset=["user_id"])
        user_df = user_df.withColumn("created", F.to_timestamp(user_df.created, 'yyyy-MM-dd HH:mm:ss'))
        
        # handle target variable
        user_df = self._label_users(user_df)
        
        # drop all-NULL rows
        user_df = user_df.na.drop("all")

        return user_df
    
    def _extract_tweets(self) -> DataFrame:
        tweet_df = self.data \
                .select(F.col("user.id").alias("user_id"), "tweet") \
                .withColumn("tweet", F.explode("tweet")) \
                .select("user_id", F.col("tweet.*"))
    
        return tweet_df
    
    def clean_tweets(self) -> DataFrame:
        # extract tweets from crawled data
        tweet_df = self._extract_tweets(self.data) # <-- id -> user_id here
        
        # consistent & duplicate
        tweet_df = tweet_df.dropDuplicates(["id"])
        tweet_df = tweet_df.na.drop(subset=["id"])
        
        # drop all-NULL rows
        tweet_df = tweet_df.na.drop("all")

        return tweet_df
    

            