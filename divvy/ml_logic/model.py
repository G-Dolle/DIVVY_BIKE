import os
import pandas as pd
import time
import glob
import pickle as pkl

from sklearn.linear_model import RidgeCV
from sklearn.ensemble import StackingRegressor
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor

def initialize_model():
    """Initialize ML Stacking Regressor model"""
    ridgecv_pipe=make_pipeline(RidgeCV())
    xgb_pipe=make_pipeline(XGBRegressor(learning_rate=0.1,
                                        max_depth=6,
                                        min_child_weight=11,
                                        n_estimators=100,
                                        n_jobs=1,
                                        objective='reg:squarederror',
                                        subsample=0.1,
                                        verbosity=0))
    estimators=[("RCV",ridgecv_pipe)]
    model= StackingRegressor(estimators=estimators,
                             final_estimator=xgb_pipe)
    return model

def train_model (model: StackingRegressor,
                 X: pd.DataFrame,
                 y: pd.DataFrame):
    """
    Fit model and return fitted_model
    """
    model.fit(X,y)
    return model


def predict(model: StackingRegressor,
                   X: pd.DataFrame):
    """"""
    y_pred= model.predict(X)
    return y_pred

def score(model: StackingRegressor,
                   X: pd.DataFrame,
                   y: pd.DataFrame):
    score=model.score(X,y)
    return score

def save_model(model: StackingRegressor = None,
               target: object) -> None:
    """
    Save model version (defined by timestamp) in divvy/models folder
    """
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    print("\nSave model to local disk...")
    LOCAL_PATH = os.path.expanduser(os.environ.get("LOCAL_PATH"))
    # save model
    if model is not None:
        model_path = os.path.join(LOCAL_PATH, "models" + target + timestamp + ".pickle")
        print(f"- model path: {model_path}")
        with open(model_path, "wb") as file:
            pkl.dump(model, file)

    print("\n✅ data saved locally")
    return None


def load_model(save_copy_locally=False) -> Model:
    """
    load the latest saved model, return None if no model found
    """
    print("\nLoad model from local disk...")
    LOCAL_PATH = os.path.expanduser(os.environ.get("LOCAL_PATH"))
    # get latest model version
    model_directory = os.path.join(LOCAL_PATH, "models")
    results = glob.glob(f"{model_directory}/*")
    if not results:
        return None

    model_path = sorted(results)[-1]
    print(f"- path: {model_path}")

    with open(model_path, "rb") as file:
        loaded_model=pkl.load(file)

    print("\n✅ model loaded from disk")

    return loaded_model


def availability (arrivals:float,
           departures:float):
    if arrivals/departures<0.6:
        return 0
    else:
        return 1
