import os
import pandas as pd


def get_weather_data():

    path = os.environ.get("LOCAL_DATA_PATH_WEATHER")

    weather_df = pd.read_csv(path)

    return weather_df

def get_divvy_data(year,quarter):

    year = str(year)
    quarter = str(quarter)

    file=year+ "/Divvy_Trips_" + year+"_"+quarter+".csv"

    path = os.environ.get("LOCAL_DATA_PATH_DIVVY")

    file_path = path+"/"+file

    path = os.path.join(os.path.expanduser(file_path))

    trips_df = pd.read_csv(path)

    return trips_df
