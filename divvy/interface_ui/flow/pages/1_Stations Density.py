import streamlit as st
import time
import numpy as np
from folium import Map, plugins

import pandas as pd
import datetime
from streamlit_folium import folium_static
from divvy.ml_logic.data_import import get_station_data



st.set_page_config(page_title="Bikes stations density")

st.markdown("# Bikes stations density")
st.markdown("## Heatmap")

st.sidebar.header("Stations Density")


station_df = get_station_data()

capacity_df = station_df[['capacity']]
capacity_df=capacity_df.drop_duplicates().reset_index(drop=True)
capacity_df = capacity_df.sort_values(by="capacity",ascending=True)
capacity_df = capacity_df[capacity_df["capacity"]>0]

option = st.selectbox('Select the lowest capacity', capacity_df['capacity'])


condition = station_df.capacity > option
station_df = station_df[condition]
station_df_red = station_df[["lat","lon"]]

m = Map([41.8781, -87.6298], zoom_start=8)

# convert to (n, 2) nd-array format for heatmap
stationArr = station_df_red.values

# plot heatmap
m.add_child(plugins.HeatMap(stationArr, radius=11))


folium_static(m, width=800, height=800)

st.markdown("## Map of stations")

st.map(station_df_red)
