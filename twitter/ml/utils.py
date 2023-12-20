import joblib
import os
from ..config import MODEL_DIR

def save_model(model, name):
    joblib.dump(model, os.path.join(MODEL_DIR, name + ".pkl"))

def load_model(name):
    return joblib.load(os.path.join(MODEL_DIR, name + ".pkl"))