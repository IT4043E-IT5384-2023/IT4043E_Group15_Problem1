import sklearn
import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import cross_val_score
from sklearn.base import clone

from ..config import MODEL_DIR

def save_model(model, name):
    joblib.dump(model, os.path.join(MODEL_DIR, name + ".pkl"))

def load_model(name):
    return joblib.load(os.path.join(MODEL_DIR, name + ".pkl"))

class Model:
    def __init__(
        self,
        model = None,
        ckpt: str = os.path.join(MODEL_DIR, "rf-n_estimators_95-max_depth_11.pkl")
    ):
        if ckpt is not None:
            model = self.load_model(ckpt)
        assert model is not None, "Either model or checkpoint cannot be None!"
        
        self.model = model        
    
    def infer(
        self, 
        X: np.ndarray
    ) -> np.ndarray:
        return self.model.predict(X)

    def train(
        self, 
        X: np.ndarray,
        y: np.ndarray
    ):
        self.model.fit(X, y)

    def increment(
        self,
        X: np.ndarray,
        y: np.ndarray
    ):
        pass

    def eval(
        self,
        X: np.ndarray,
        y: np.ndarray,
        scoring: str = "roc_auc_ovo"
    ) -> float:
        return cross_val_score(clone(self.model), X, y, 
                               scoring=scoring, cv=2, n_jobs=-1).mean()
    
    @staticmethod
    def load_model(ckpt: str):
        return joblib.load(ckpt)
    
    def save_model(self, id_):
        joblib.dump(self.model, os.path.join(MODEL_DIR, id_ + ".pkl"))
        