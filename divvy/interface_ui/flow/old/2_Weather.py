import streamlit as st
import time
import numpy as np
from folium import Map, plugins
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime
from streamlit_folium import folium_static

from divvy.ml_logic.data_import import get_divvy_data, get_weather_data
from divvy.ml_logic.cleaning import compute_geohash_stations,weather_cleaning, cleaning_divvy_gen,cleaning_divvy_gen_agg, merge_divvy_weather, features_target
from divvy.ml_logic.preprocessor import transform_time_features, preprocess_features, target_process

st.set_page_config(page_title="Bikes rides and weather")

st.markdown("# Bikes rides and weather")
st.sidebar.header("Weather")



rides_df_daily=pd.read_csv("raw_data/rides_df_daily_2021.csv")
rides_df_daily["date"]= pd.to_datetime(rides_df_daily["date"])

avg_weather_df=pd.read_csv("raw_data/avg_temp.csv")
avg_weather_df["date"]= pd.to_datetime(avg_weather_df["date"])

rides_df_daily_geohash=pd.read_csv("raw_data/rides_df_daily_geohash_2021.csv")
rides_df_daily_geohash["date"]= pd.to_datetime(rides_df_daily_geohash["date"])



def timeframe_df(df,timevariable,start_time,end_time):

    condition_1 = df[timevariable] >= pd.to_datetime(start_time)
    condition_2 = df[timevariable] <= pd.to_datetime(end_time)

    df_red = df[condition_1]
    df_red = df_red[condition_2]

    return df_red

def plot_rides_geohash(start_time,end_time,df_divvy,
                       df_weather,timevariable,
                       geohash,weather_metric):

    df_divvy_red = timeframe_df(df_divvy,timevariable,start_time,end_time)
    df_weather_red = timeframe_df(df_weather,timevariable,start_time,end_time)

    df_divvy_red = df_divvy_red[df_divvy_red["geohash"]==geohash]
    df_weather_red = df_weather_red[[timevariable,weather_metric]]

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(df_divvy_red[timevariable],df_divvy_red.nb_rides, 'g-')
    ax2.plot(df_weather_red[timevariable],df_weather_red[weather_metric], 'b-')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Total nb of rides per day', color='g')
    ax2.set_ylabel(f'{weather_metric}', color='b')

    return fig


def plot_rides_all(start_time,end_time,df_divvy,
                       df_weather,timevariable,
                       weather_metric):

    df_divvy_red = timeframe_df(df_divvy,timevariable,start_time,end_time)
    df_weather_red = timeframe_df(df_weather,timevariable,start_time,end_time)

    df_weather_red = df_weather_red[[timevariable,weather_metric]]

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(df_divvy_red[timevariable],df_divvy_red.nb_rides, 'g-')
    ax2.plot(df_weather_red[timevariable],df_weather_red[weather_metric], 'b-')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Total nb of rides per day', color='g')
    ax2.set_ylabel(f'{weather_metric}', color='b')

    return fig

#start_time = "2021-07-01"
#end_time = "2021-12-31"
#timevariable="date"
#geohash = "dp3wm"
#weather_metric="temp"

weather_metric_choice= ['temp', 'pressure', 'humidity', 'wind_speed', 'wind_deg','clouds_all']

st.markdown("## City of Chicago")

with st.form('Please pick a starting and an end date'):
    start_date_all=st.date_input('Start date',
                                 value=datetime.date(2021, 7, 1))
    end_date_all=st.date_input('End date',
                                 value=datetime.date(2021, 12, 31))

    wmc=st.selectbox('Select the weather metric', weather_metric_choice)


    st.form_submit_button("Let's go!")

start_time = start_date_all
end_time = end_date_all
timevariable="date"
weather_metric = str(wmc)

fig=plot_rides_all(start_time,end_time,
                       rides_df_daily,avg_weather_df,
                       timevariable,
                       weather_metric)

st.pyplot(fig)

st.markdown("## Geohash level")

geohash_list = list(rides_df_daily_geohash.geohash.unique())

with st.form('Please pick a starting and an ending point'):
    start_date_geo=st.date_input('Start date',
                                 value=datetime.date(2021, 7, 1))
    end_date_geo=st.date_input('End date',
                                 value=datetime.date(2021, 12, 31))

    gh=st.selectbox('Select the geohash metric', geohash_list)
    wmc2=st.selectbox('Select the weather metric', weather_metric_choice)

    st.form_submit_button("Let's go!")

start_time = start_date_all
end_time = end_date_all
timevariable="date"
weather_metric = str(wmc2)
geohash = gh

fig2=plot_rides_geohash(start_time,end_time,
                       rides_df_daily_geohash,avg_weather_df,
                       timevariable,geohash,
                       weather_metric)

st.pyplot(fig2)
