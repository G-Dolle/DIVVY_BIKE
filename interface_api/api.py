from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interface_ui.flow.flow import transform_user_inputs,get_station_availability
from interface_ui.flow.ui_utils import process_weather_inputs
import pandas as pd
import pickle as pkl
from datetime import datetime

app = FastAPI()
app.state.model_dep=pkl.load(open('models/elasticnet_departures.pickle','rb'))
app.state.model_arr=pkl.load(open('models/elasticnet_arrivals.pickle','rb'))
app.state.prep_dep=pkl.load(open('preprocessors/preprocessor_dep.pickle','rb'))
app.state.prep_dep=pkl.load(open('preprocessors/preprocessor_arr.pickle','rb'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.get("/predict")
def predict(dep_datetime: datetime, #2022-12-13 12:10:20
            departure_address: object,  #3424 S giles
            num_nearest_stations: int,  #3
            ):
    """
    based on user inputs (dep_datetime, departure address and
    number of nearest stations) triggers the prediction of
    stations available
    """

    #converting datetime into two variables: date and time
    dep_datetime=str(dep_datetime)
    dep_date,dep_time=dep_datetime.split (sep=' ')
    departure_date= datetime.strptime(dep_date, '%Y-%m-%d').date()
    departure_time=datetime.strptime(dep_time, '%H:%M:%S').time()

    #Transform user inputs (address and near stations) into model inputs
    userlatlon, nclose_stations=transform_user_inputs(departure_address,
                                       num_nearest_stations)
    user_lat=userlatlon[0]
    user_lon=userlatlon[1]

    #Obtain weather forecasts and transform it for Chicago
    weather_inputs=process_weather_inputs(departure_date,
                                          departure_time)
    #Preprocess user inputs
    X_dep_processed=app.state.prep_dep.transform(weather_inputs)
    X_arr_processed=app.state.prep_dep.transform(weather_inputs)

    #Predict departures and arrivals
    departures=app.state.model_dep.predict(X_dep_processed)
    arrivals=app.state.model_dep.predict(X_arr_processed)

    stations=get_station_availability(nclose_stations,
                                      arrivals,
                                      departures)

    stations_dict=stations.to_dict('list')

    map_lat=stations.lat.mean()
    map_lon=stations.lon.mean()

    return dict(user_lat=user_lat,user_lon=user_lon,map_lat=map_lat,map_lon=map_lon,station=stations_dict)


@app.get("/")
def root():
    return {'greeting':'Hello'}
