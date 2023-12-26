from typing import Tuple, List, Union, Optional, Dict
from itertools import chain

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import DataFrame
from pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier, RandomForestClassificationModel
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from ..config import LANG_MAP, LABEL_MAP

class UserClassification:
    def __init__(
        self,
        model: Union[str, RandomForestClassificationModel],
        neglect_cols: List
    ):
        self.neglect_cols = neglect_cols

        if isinstance(model, str):
            model = self.load_model(model)
        self.model = model
    
    @staticmethod
    def load_model(modelpath: str):
        rf_clf = RandomForestClassificationModel.load(modelpath)
        return rf_clf
    
    def _extract_data(self, data: DataFrame) -> Tuple[DataFrame, DataFrame]:
        # split data into labeled and unlabeled
        labeled = data.filter(F.col("location").isNotNull())
        unlabeled = data.filter(F.col("location").isNull())

        return labeled, unlabeled

    def _transform_data(self, data: DataFrame) -> DataFrame:
        # encode categorical features
        bin_len = 6
        label_map = F.create_map([F.lit(x) for x in chain(*LABEL_MAP.items())])
        lang_map = F.create_map([F.lit(x) for x in chain(*LANG_MAP.items())])
        data = data \
                .withColumn("location", label_map[F.col("location")]) \
                .withColumn("blue_tmp", F.when(F.col("blue") == True, 1).otherwise(0)) \
                .withColumn("lang_tmp", lang_map[F.col("lang")])
        
        data = data.withColumn("lang_tmp", 
                                         F.lpad(F.bin(data["lang_tmp"]), bin_len, '0')) # binary encoding
        split_lang = F.split(data['lang_tmp'], "")
        for i in range(bin_len):
            data = data.withColumn(f'lang_{i}', 
                                             split_lang.getItem(i).cast(T.IntegerType()))
        data = data.drop("lang_tmp")
        
        # enumerate types of features
        num_cols = [name for name, datatype in data.dtypes 
                    if (not datatype.startswith('string')) and (not name.startswith('lang')) 
                    and (not name.startswith('blue')) and name not in (["location", "user_id"] + self.neglect_cols)]
        cat_cols = ["blue_tmp"] + [name for name, datatype in data.dtypes 
                                   if name.startswith('lang') and name not in (self.neglect_cols + ["lang"])]
        
        # define processing ops
        num_assembler = VectorAssembler(inputCols=num_cols, outputCol="num_feats")
        scaler = StandardScaler(inputCol="num_feats", outputCol="num_feats_scaled", withStd=True, withMean=True)
        
        cat_assembler = VectorAssembler(inputCols=cat_cols, outputCol="cat_feats", 
                                        handleInvalid ="keep")
        
        all_assembler = VectorAssembler(inputCols= ["num_feats_scaled", "cat_feats"], outputCol="all_feats_scaled", 
                                        handleInvalid ="keep")

        # assemble a pipeline
        pipeline = Pipeline(stages=[num_assembler, scaler, cat_assembler, all_assembler])

        # fit transform on pipeline
        encode_data = pipeline.fit(data).transform(data)

        # select features + targets
        selected_cols = ["all_feats_scaled"] + data.columns
        encode_data = encode_data.select(*selected_cols)

        return encode_data
    
    def model_fit(self, data: DataFrame):
        labeled, _ = self._extract_data(data)
        labeled_prep = self._transform_data(labeled)
        self.model = self.model.fit(labeled_prep)
    
    def model_eval(
        self,
        metrics: List,
        data: DataFrame
    ) -> Dict[str, float]:
        labeled, _ = self._extract_data(data)
        labeled_prep = self._transform_data(labeled)

        # set up cross-validation
        scoreboard = {}
        for metric in metrics:
            print(f"Validating model using {metric}")
            paramGrid = ParamGridBuilder().build()
            cross_validator = CrossValidator(
                estimator=self.model.copy(),
                estimatorParamMaps=paramGrid, 
                evaluator=MulticlassClassificationEvaluator(labelCol="location", metricName=metric), 
                numFolds=2
            )

            # cross-validate on labeled data
            model = cross_validator.fit(labeled_prep)

            # avg. score from the cross-validated model
            scoreboard[metric] = model.avgMetrics[0]
        
        self.scores_ = scoreboard
        return scoreboard
    
    def model_infer(self, data: DataFrame) -> DataFrame:
        labeled, unlabeled = self._extract_data(data)
        
        unlabeled_prep = self._transform_data(unlabeled)
        unlabeled_pred = self.model.transform(unlabeled_prep)
        unlabeled_pred = self._inv_transform(unlabeled_pred, show_col=labeled.columns)
        
        return labeled.select(*unlabeled_pred.columns).union(unlabeled_pred)
    
    def _inv_transform(self, data: DataFrame, show_col: List) -> DataFrame:
        INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}
        inv_label_map = F.create_map([F.lit(x) for x in chain(*INV_LABEL_MAP.items())])

        
        show_df = data \
                    .withColumn("prediction", inv_label_map[F.col("prediction")]) \
                    .select(*show_col, "prediction") \
                    .drop("location") \
                    .withColumnRenamed("prediction", "location") \
                    .withColumn("blue", F.when(F.col("blue") == 1, True).otherwise(False))
    
        return show_df
        