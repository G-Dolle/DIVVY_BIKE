import streamlit as st
import pandas as pd
import requests
import datetime
import folium
from streamlit_folium import folium_static


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

#Executing the API
url='http://localhost:8000/predict'
params=dict(
            dep_datetime=[dep_datetime],
            departure_address=[departure_address],
            num_nearest_stations=[num_nearest_stations],
        )

response=requests.get(url=url, params=params)
outcome=response.json()

#Extracting info from API response to streamlit
lat_st=outcome['map_lat']
lon_st=outcome['map_lon']
lat_user=outcome['user_lat']
lon_user=outcome['user_lon']

stations=pd.DataFrame.from_dict(outcome['station'])

#Initialize folium map with Chicago coordinates
m=folium.Map(location=[lat_st,lon_st], zoom_start=15)

folium.Marker(location=[lat_user,lon_user],
              popup="you're here",
              icon=folium.Icon(color='blue'),
              tooltip="you're here"
              ).add_to(m)

#Adding markers
for index, row in stations.iterrows():
    if row['availability']==1:
        color_row='green'
        tooltip_row='bikes available'
    else:
        color_row='red'
        tooltip_row='no bikes available'
    folium.Marker(location=[row['lat'], row['lon']],
                  popup=row['name'],
                  icon=folium.Icon(color=color_row),
                  tooltip=tooltip_row
                  ).add_to(m)

folium_static(m)
