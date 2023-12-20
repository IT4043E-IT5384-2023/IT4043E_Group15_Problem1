import sklearn
import pandas as pd
import numpy as np
from typing import Dict, Tuple

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from ..config import PROCESS_DATA_PATH, MODEL_DIR

def encode_data(data: pd.DataFrame):
    # eliminate Arctic
    data = data[data["location"] != "Arctic"]
    data["blue"] = data["blue"].astype("object")
    data = data.drop(columns=["user_id", "username"], axis=1)

    # extract type-specific columns
    cat_attrbs = data.select_dtypes(include="object").columns.tolist()[1:]
    num_attrbs = data.select_dtypes(exclude="object").columns.tolist()

    print(len(cat_attrbs), len(num_attrbs))
    print(cat_attrbs, num_attrbs)

    # transform features
    fn = ColumnTransformer([
        ("std_scaler", StandardScaler(), num_attrbs),
        ("lbl_encoder", OrdinalEncoder(), cat_attrbs),
    ], remainder="drop")
    
    pipe = Pipeline([
        ("preprocess_fn", fn),
    ])

    X = pipe.fit_transform(data.drop(columns=["location"], axis=1))
    
    # transform labels
    lb_encoder = LabelEncoder()
    y = lb_encoder.fit_transform(data["location"])
    
    return X, y, lb_encoder