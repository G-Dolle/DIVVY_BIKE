import pandas as pd
import numpy as np
import requests

def get_coordinates (address):
    """
    obtain the coordinates (latitude and longitude)
    based on an address by leveraging the GOOGLE API
    """
    geocode_url='https://maps.googleapis.com/maps/api/geocode/json'
    params=dict(
        address=[address],
        key=[GOOGLE_API_KEY]
        )
    geo_response=requests.get(url=geocode_url,params=params)
    geodata = geo_response.json()
    try:
        latlong = [geodata['results'][0]['geometry']['location']['lat'],
               geodata['results'][0]['geometry']['location']['lng']]
    except IndexError:
        latlong = None
    return latlong
