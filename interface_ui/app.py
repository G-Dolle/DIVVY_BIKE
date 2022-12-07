import streamlit as st
import pandas as pd
import requests
import numpy as np
import datetime
from ml_logic.ui_utils import get_coordinates

st.title('THIS APP HELPS YOU FIND A \U0001F6B2 FOR YOUR RIDE \U0001F6B4')
st.header('Enter your departure time and location')

with st.form('Please provide the below inputs'):
    departure_date=st.date_input('departure date',value=datetime.datetime(2022, 12, 16, 12, 10, 20))
    departure_time=st.time_input('departure time',value=datetime.datetime(2022, 12, 16, 12, 10, 20))
    dep_datetime=f'{pickup_date} {pickup_time}'
    departure_address=st.text_input('Departure address',value='3424 S giles')
    st.form_submit_button('Find nearest station with bikes available')

latlon=get_coordinates(departure_address)
departure_latitude=latlon[0]
departure_longitude=latlon[1]

"""url='https://taxifare2-bva7jbyfma-ew.a.run.app/predict'
params=dict(
            departure_datetime=[dep_datetime],
            departure_latitude=[departure_latitude],
            departure_longitude=[departure_longitude],
        )

response=requests.get(url=url, params=params)
my_prediction=response.json()

pred=round(my_prediction['fare'],3)

st.header(f' ${pred}')"""


stations=pd.read_csv('/Users/mariofernandez/code/G-Dolle/DIVVY_BIKE/data/stations.csv')
stations.drop(columns=['id','name','dpcapacity'], inplace=True)
stations.rename(columns={'latitude':'lat','longitude':'lon'},inplace=True)

stations.lat=stations.lat.apply(lambda x: float(x.split()[0].replace(',','.')))
stations.lon=stations.lon.apply(lambda x: float(x.split()[0].replace(',','.')))

st.map(stations)
