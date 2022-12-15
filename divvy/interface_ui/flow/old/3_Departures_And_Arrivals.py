import streamlit as st
import time
import numpy as np
from folium import Map, plugins
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime
from streamlit_folium import folium_static

from divvy.ml_logic.data_import import get_divvy_data, get_weather_data, get_station_data
from divvy.ml_logic.cleaning import compute_geohash_stations,weather_cleaning, cleaning_divvy_gen,cleaning_divvy_gen_agg, merge_divvy_weather, features_target
from divvy.ml_logic.preprocessor import transform_time_features, preprocess_features, target_process

st.set_page_config(page_title="Departures and Arrivals")

st.markdown("# Departures and Arrivals")
st.sidebar.header("Departures and Arrivals")

date = "2021-07-01"
hour = "10:00:00"
geohash="dp3wm"


raw_weather_df = get_weather_data()
clean_weather_df = weather_cleaning(raw_weather_df)

divvy_q1_2021 = get_divvy_data(2021,"Q1")

divvy_q2_2021 = get_divvy_data(2021,"Q2")
divvy_q3_2021 = get_divvy_data(2021,"Q3")
divvy_q4_2021 = get_divvy_data(2021,"Q4")

rides_df = pd.concat([divvy_q1_2021,divvy_q2_2021, divvy_q3_2021,divvy_q4_2021])
clean_divvy_df = cleaning_divvy_gen_agg(rides_df)
merged_df = merge_divvy_weather(clean_divvy_df, clean_weather_df)

station_df = get_station_data()
station_df= station_df[["name","lat","lon"]]
station_df.rename(columns={"name":"station_name"}, inplace=True)
merged_df = merged_df.merge(station_df, on="station_name", how="left")
