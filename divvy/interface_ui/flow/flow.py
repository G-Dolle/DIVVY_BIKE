from divvy.interface_ui.flow.ui_utils import get_coordinates
from divvy.interface_ui.flow.ui_utils import get_nearest_n_stations
from divvy.ml_logic.model import availability
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
    return latlon, nclose_stations

def get_station_availability (stations:pd.DataFrame,
                              arrivals:float,
                              departures:float):
    """Return whether there will be bikes available
    for a given station"""
    available=availability(arrivals, departures)
    stations['availability']=available
    stations_simplified_df=stations.drop(columns=['Unnamed: 0','external_id','eightd_has_key_dispenser','electric_bike_surcharge_waiver','has_kiosk','rental_methods','rental_uris','eightd_station_services','region_id','region_code','address','dockless_bikes_parking_zone_capacity','rack_model','client_station_id','target_bike_capacity','target_scooter_capacity'])
    return stations_simplified_df
