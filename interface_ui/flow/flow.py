from interface_ui.flow.ui_utils import get_coordinates
from interface_ui.flow.ui_utils import get_nearest_n_stations
import pandas as pd

def transform_user_inputs(departure_address:object,
                          num_nearest_stations:int):
    """Return nearest stations by transforming user inputs as follows:
    depature_address --> departure latitude and longitude
    num_nearest_stations--> top n stations"""
    latlon=get_coordinates(departure_address)
    departure_latitude=latlon[0]
    departure_longitude=latlon[1]
    nclose_stations=get_nearest_n_stations(departure_latitude,
                                       departure_longitude,
                                       num_nearest_stations)
    return nclose_stations

def get_station_availability (stations:pd.DataFrame):
    """Return whether there will be bikes available
    for a given station"""
    stations['availability']=1
    return stations
