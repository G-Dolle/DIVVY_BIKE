import os
import pandas as pd
import numpy as np
from sklearn.linear_model import ElasticNet
import pickle as pkl

def initialize_model():
    model_en=ElasticNet(alpha=0.01,l1_ratio=0.1)
    return model_en

def train_model(model: ElasticNet,
                X: pd.DataFrame,
                y: pd.DataFrame):
    model.fit(X,y)
    saved_model = pkl.dumps(model)
    return saved_model, model

def load_model (pkl:bytes):
    model=pkl.loads(pkl)
    return model

def predict(model: ElasticNet,
                   X: pd.DataFrame):
    y_pred= model.predict(X)
    return y_pred

def score(model: ElasticNet,
                   X: pd.DataFrame,
                   y: pd.DataFrame):
    score=model.score(X,y)
    return score

def availability (arrivals: float,
           departures: float):
    if arrivals/departures<0.6:
        return 0
    else:
        return 1
