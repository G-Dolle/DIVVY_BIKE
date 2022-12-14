import os
import pandas as pd
import time
import glob
import pickle as pkl

from sklearn.linear_model import RidgeCV
from sklearn.ensemble import StackingRegressor
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import LinearSVR
from sklearn.compose import ColumnTransformer

def initialize_model_arrival():
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

def initialize_model_departure():
    """Initialize ML Stacking Regressor model"""
    model = StackingRegressor(
        estimators = [("svr", LinearSVR(C=25.0, dual=True, epsilon=1.0, loss='squared_epsilon_insensitive', tol=0.0001)),
                    ("xbg", XGBRegressor(learning_rate=0.01, max_depth=3, min_child_weight=19, n_estimators=100, n_jobs=1, objective='reg:squarederror', subsample=0.8, verbosity=0))],
        final_estimator = DecisionTreeRegressor(max_depth=3, min_samples_leaf=12, min_samples_split=18))
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


def save_model(target: object, model: StackingRegressor = None,type="model") -> None:
    """
    Save model version (defined by timestamp) in divvy/models folder
    """
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    print(f"\nSave {type} to local disk...",  os.environ.get(f"LOCAL_PATH_{type.upper()}"))
    LOCAL_PATH = os.path.expanduser(os.environ.get(f"LOCAL_PATH_{type.upper()}"))
    # save model
    if model is not None:
        model_path = os.path.join(LOCAL_PATH, type + "_" + target + "_" + timestamp + ".pickle")
        print(f"- model path: {model_path}")
        with open(model_path, "wb") as file:
            pkl.dump(model, file)

    print("\n✅ data saved locally")
    return None


def load_model(save_copy_locally=False,kind="arrival") -> StackingRegressor:
    """
    load the latest saved model, return None if no model found
    """
    print("\nLoad model from local disk...")
    LOCAL_PATH = os.path.expanduser(os.environ.get("LOCAL_PATH_MODEL"))
    # get latest model version
    model_directory = os.path.join(LOCAL_PATH)
    results = glob.glob(f"{model_directory}/*")
    if not results:
        return None

    results = [x for x in results if kind in x.lower()]

    model_path = sorted(results)[-1]
    print(f"- path: {model_path}")

    with open(model_path, "rb") as file:
        loaded_model=pkl.load(file)

    print("\n✅ model loaded from disk")

    return loaded_model


def load_preprocessor(save_copy_locally=False,kind="arrival") -> ColumnTransformer:
    """
    load the latest saved preprocessor, return None if no preprocessor found
    """
    print("\nLoad preprocessor from local disk...")
    LOCAL_PATH = os.path.expanduser(os.environ.get("LOCAL_PATH_PREPROCESSOR"))
    # get latest model version
    preprocessor_directory = os.path.join(LOCAL_PATH)
    results = glob.glob(f"{preprocessor_directory}/*")
    if not results:
        return None

    results = [x for x in results if kind in x.lower()]

    preprocessor_path = sorted(results)[-1]
    print(f"- path: {preprocessor_path}")

    with open(preprocessor_path, "rb") as file:
        loaded_preprocessor=pkl.load(file)

    print("\n✅ preprocessor loaded from disk")

    return loaded_preprocessor


def availability (arrivals:float,
           departures:float):
    if arrivals/departures<0.6:
        return 0
    else:
        return 1
