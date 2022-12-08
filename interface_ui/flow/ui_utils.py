import pandas as pd
import numpy as np
import requests
import urllib.parse
import os
from sklearn.neighbors import NearestNeighbors

def get_coordinates (address:object):
    """Return the coordinates (latitude and longitude)
    based on an address by leveraging the GOOGLE API"""

    geocode_url='https://maps.googleapis.com/maps/api/geocode/json'
    params=dict(
        address=[address],
        key=[os.environ.get("GOOGLE_API_KEY")]
        )
    geo_response=requests.get(url=geocode_url,params=params)
    geodata = geo_response.json()
    try:
        latlong = [geodata['results'][0]['geometry']['location']['lat'],
               geodata['results'][0]['geometry']['location']['lng']]
    except IndexError:
        latlong = None
    return latlong

def get_stations(only_coordinates=False):
    """Return the stations dataframe
    OPTIONAL: it can be a simple df - with only stations
    or a complete df - with stations id, name and dpcapacity
    TO BE CORRECTED: load to cloud and source address"""

    address='/Users/mariofernandez/code/G-Dolle/DIVVY_BIKE/raw_data/data/stations.csv'
    stations=pd.read_csv(address)
    if only_coordinates:
        stations.drop(columns=['id','name','dpcapacity'], inplace=True)
    stations.rename(columns={'latitude':'lat','longitude':'lon'},
                    inplace=True)
    stations.lat=stations.lat.apply(
        lambda x: float(x.split()[0].replace(',','.')))
    stations.lon=stations.lon.apply(
        lambda x: float(x.split()[0].replace(',','.')))
    return stations

def get_nearest_n_stations(lat:float,
                           lon:float,
                           top_n=1):
    """Return the top n stations closest to the user lat, lon"""
    stations=get_stations(only_coordinates=False)
    NN=NearestNeighbors(n_neighbors=top_n,metric='haversine')
    user_loc=pd.DataFrame(dict(lat=[lat],lon=[lon]))
    NN.fit(stations[['lat', 'lon']])
    result=NN.kneighbors(user_loc)
    index=list(result[1][0])
    return stations.iloc[index]

def chicago_weather_forecast():
    '''Return a 5-day weather forecast for the city of Chicago'''

    BASE_URI="https://weather.lewagon.com"
    url=urllib.parse.urljoin(BASE_URI, "/data/2.5/forecast")
    forecasts=requests.get(url, params={'lat': 41.87, 'lon': -87.62, 'units': 'metric'}).json()['list']
    return forecasts[::8]

def convert_chicago_forecast_todf(forecasts:list):
    """Return a pre-preprocessed dataframe """
    weather_dict=dict(dt=[],dt_iso=[],timezone=[],city_name=[],lat=[],lon=[],temp=[]
                  ,visibility=[],dew_point=[],feels_like=[],temp_min=[],temp_max=[],
                  pressure=[],sea_level=[],grnd_level=[],humidity=[],wind_speed=[],
                  wind_deg=[],wind_gust=[],rain_1h=[],rain_3h=[],snow_1h=[],snow_3h=[],
                  clouds_all=[],weather_id=[],weather_main=[],weather_description=[],
                  weather_icon=[])


def get_right_forecast(departure_date,departure_time):
    """Return """
