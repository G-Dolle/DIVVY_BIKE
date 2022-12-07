import pandas as pd
import numpy as np
import requests
import urllib.parse
import os

BASE_URI = "https://weather.lewagon.com"



def get_coordinates (address):
    """
    obtain the coordinates (latitude and longitude)
    based on an address by leveraging the GOOGLE API
    """
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

def chicago_weather_forecast():
    '''Return a 5-day weather forecast for the city of Chicago'''
    BASE_URI = "https://weather.lewagon.com"
    url = urllib.parse.urljoin(BASE_URI, "/data/2.5/forecast")
    forecasts = requests.get(url, params={'lat': 41.87, 'lon': -87.62, 'units': 'metric'}).json()['list']
    return forecasts[::8]

def get_stations():
    """get the stations dataframe
    TO BE CORRECTED: load to cloud and source address"""
    address='/Users/mariofernandez/code/G-Dolle/DIVVY_BIKE/raw_data/data/stations.csv'
    stations=pd.read_csv(address)
    stations.drop(columns=['id','name','dpcapacity'], inplace=True)
    stations.rename(columns={'latitude':'lat','longitude':'lon'},
                    inplace=True)

    stations.lat=stations.lat.apply(
        lambda x: float(x.split()[0].replace(',','.')))
    stations.lon=stations.lon.apply(
        lambda x: float(x.split()[0].replace(',','.')))
    return stations
