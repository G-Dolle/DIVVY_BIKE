import streamlit as st
import pandas as pd
import requests
import numpy as np
import datetime
import folium
from streamlit_folium import folium_static
from flow.flow import transform_user_inputs,get_station_availability

#Title of the app
st.title('THIS APP HELPS YOU FIND A \U0001F6B2 FOR YOUR RIDE \U0001F6B4')
st.header('Enter your departure time and location')

#Obtain the user inputs
with st.form('Please provide the below inputs'):
    departure_date=st.date_input('departure date',
                                 value=datetime.datetime(2022, 12, 16, 12, 10, 20))
    departure_time=st.time_input('departure time',
                                 value=datetime.datetime(2022, 12, 16, 12, 10, 20))
    dep_datetime=f'{departure_date} {departure_time}'
    departure_address=st.text_input('Departure address',
                                    value='3424 S giles')
    num_nearest_stations=st.number_input('nearest stations',
                                         min_value=1,
                                         max_value=5,
                                         step=1,
                                         value=1)
    st.form_submit_button('Find nearest station(s) with bikes available')

#Transform user inputs (address and near stations) into model inputs
nclose_stations=transform_user_inputs(departure_address,
                                       num_nearest_stations)

#Obtain weather forecasts for Chicago

stations=get_station_availability(nclose_stations)
lat_st=stations.lat.mean()
lon_st=stations.lon.mean()

#Initialize folium map with Chicago coordinates
m=folium.Map(location=[lat_st,lon_st], zoom_start=17)

#Adding markers
for index, row in stations.iterrows():
    if row['availability']==1:
        color='green'
        tooltip='available  :ok_hand::skin-tone-3:'
    else:
        color='red'
        tooltip='no bikes available :white_frowning_face:'
    folium.Marker(location=[stations.lat, stations.lon],
                  popup=stations.name,
                  icon=folium.Icon(color=color, tooltip=tooltip),
                  ).add_to(m)

folium_static(m)

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
