from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from DIVVY_BIKE.ml_logic.preprocessor import preprocess_features
#from DIVVY_BIKE.ml_logic.registry import load_model
import pandas as pd

app = FastAPI()
app.state.model=load_model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.get("/predict")
def predict(pickup_datetime: datetime,  # 2013-07-06 17:18:00
            pickup_longitude: float,    # -73.950655
            pickup_latitude: float,     # 40.783282
            ):
    """
    type hinting to indicate the data types expected
    for the parameters of the function
    FastAPI uses it to hand errors on incompatible parameters
    """

    X_pred = pd.DataFrame(dict(
            pickup_datetime=[pickup_datetime],
            pickup_longitude=[pickup_longitude],
            pickup_latitude=[pickup_latitude],
        ))

    X_processed = preprocess_features(X_pred)
    y_pred = app.state.model.predict(X_processed)
    return dict(fare=float(y_pred))


@app.get("/")
def root():
    return {'greeting':'Hello'}
