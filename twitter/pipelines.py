from pyspark.sql import SparkSession, DataFrame
from typing import List, Optional
import os
from .config import GG_LUCKY_PATH, SPARK_MASTER, HADOOP_CONNECTOR_PATH, ELASTIC_MASTER, ELASTIC_HTTP_AUTH, \
                    MODEL_CKPT, ROOT, PROFILE_PATH
RAW_DATA_PATH = os.path.join(ROOT, PROFILE_PATH + "l")

from .tasks import UserClassification
from .processing import DataCleaner, DataPreprocessor
from .scraping import scrape

from elasticsearch import Elasticsearch
from elasticsearch import helpers

class Pipeline:
    def __init__(self):
        self.spark = self.connect_spark()
        self.es = self.connect_elastic()
    
    @staticmethod
    def connect_spark():
        #config the connector jar file
        spark = (SparkSession.builder.appName("SimpleSparkJob").master(SPARK_MASTER)
                .config("spark.jars", HADOOP_CONNECTOR_PATH)
                .config("spark.executor.memory", "1G")  #excutor excute only 2G
                .config("spark.driver.memory","1G") 
                .config("spark.executor.cores","1") # Cluster use only 3 cores to excute as it has 3 server
                .config("spark.python.worker.memory","1G") # each worker use 1G to excute
                .config("spark.driver.maxResultSize","1G") #Maximum size of result is 3G
                .config("spark.kryoserializer.buffer.max","1024M")
                .getOrCreate())
        
        # version migration
        spark.conf.set("spark.sql.legacy.timeParserPolicy","LEGACY")

        #config the credential to identify the google cloud hadoop file 
        spark.conf.set("google.cloud.auth.service.account.json.keyfile", GG_LUCKY_PATH)
        spark._jsc.hadoopConfiguration().set('fs.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem')
        spark._jsc.hadoopConfiguration().set('fs.gs.auth.service.account.enable', 'true')

        return spark

    @staticmethod
    def connect_elastic():
        es = Elasticsearch([ELASTIC_MASTER], 
                           http_auth=(ELASTIC_HTTP_AUTH["id"], 
                                      ELASTIC_HTTP_AUTH["password"]))
        return es
        

class TwitterPipeline(Pipeline):
    def __init__(
        self,
        raw_data: Optional[str] = RAW_DATA_PATH,
        model: Optional[str] = MODEL_CKPT,
        task_neglect_cols: List = ['profileImageUrl','profileBannerUrl','descriptionLinks','_type', 'verified',
                                    'id_str','url','created', 'rawDescription', 'protected', 'blueType', 'displayname', 'country'],
        tweet_join_cols: List = ["user_id", "replyCount", "retweetCount", 
                                 "likeCount", "quoteCount", "viewCount", "lang"]
    ):
        super().__init__()

        self.cleaner = DataCleaner(self.spark, raw_data)
        self.preprocessor = DataPreprocessor(task_neglect_cols, tweet_join_cols)
        self.task = UserClassification(model, task_neglect_cols)

    @staticmethod
    def scrape_data(load_uids: bool = True):
        scrape(load_uids = load_uids)
    
    def run(self, report_name: str = "group15-spark-ml-experimental"):
        user_df, tweet_df = self.cleaner()
        task_df = self.preprocessor(tweet_df, user_df)
        report_df = self.task.model_infer(task_df)

        self.report(report_df, report_name)

    def report(self, df: DataFrame, index_name):
        actions = []
        for row in df.rdd.toLocalIterator():
            action = {
                "_index": index_name,
                "_source": {
                    col: row[col] for col in df.columns
                }
            }
            actions.append(action)
        helpers.bulk(self.es, actions)