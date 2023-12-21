import sklearn
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Union

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from ..config import LABEL_MAP

def load_data(data: Union[pd.DataFrame, str]):
    if isinstance(data, str):
        data = pd.read_csv(data)
    data = data.drop(columns=["user_id", "username"], axis=1)
    
    # split data
    labeled, unlabeled = data[data["location"].notnull()], data[data["location"].isnull()]  
    Xl, yl = labeled.drop(columns=["location"], axis=1), labeled["location"]
    Xu, yu = unlabeled.drop(columns=["location"], axis=1), unlabeled["location"]

    return Xl, yl, Xu, yu

def encode_data(
    X: pd.DataFrame, 
    y: pd.Series
) -> Tuple[np.ndarray, np.ndarray]:
    # extract type-specific columns
    cat_attrbs = X.select_dtypes(include="object").columns.tolist()
    num_attrbs = X.select_dtypes(exclude="object").columns.tolist()

    # pipeline
    fn = ColumnTransformer([
        ("std_scaler", StandardScaler(), num_attrbs),
        ("lbl_encoder", OrdinalEncoder(), cat_attrbs),
    ], remainder="passthrough")
    
    pipe = Pipeline([
        ("preprocess_fn", fn),
    ])

    # encode data
    X = pipe.fit_transform(X)
    y = y.map(LABEL_MAP).to_numpy()
    
    return X, y

def interpret_label(y: np.ndarray) -> np.ndarray:
    inv_map = {v: k for k, v in LABEL_MAP.items()}
    return np.vectorize(inv_map.get)(y)