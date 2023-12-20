from .models import Model
from .transforms import encode_data
from ..config import PROCESS_DATA_PATH

import pandas as pd

def infer(): # <-- data is cleaned & processed
    records = pd.read_csv(PROCESS_DATA_PATH)

    model = Model() # default estimator

    # encode records for ml
    X, _, label_encoder = encode_data(records)

    # model infers
    y_pred = model.infer(X)
    
    return label_encoder.inverse_transform(y_pred)
