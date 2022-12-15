import streamlit as st
import time
import numpy as np
from folium import Map, plugins
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime
from streamlit_folium import folium_static
from divvy.ml_logic.data_import import get_station_data
import seaborn as sns

st.set_page_config(page_title="Factors influencing bikes traffic",  layout="centered")

st.sidebar.header("Analysis")

st.markdown("# What drives bikes traffic?")

st.markdown("## Weather")

st.markdown("The better the weather, the nicer it is to ride a bike across the city. Not surprisingly, bikes traffic and temperature follow similar trends.")

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
    ax1.set_ylabel('Total number of rides per day', color='g')
    ax2.set_ylabel(f'{weather_metric}', color='b')

    return fig

from PIL import Image
image = Image.open('raw_data/output.png')

st.image(image, caption='',width=500)

#scatter = plt.scatterplot(data = rides_df_daily, x="temp",y="nb_rides")


#start_time = "2021-07-01"
#end_time = "2021-12-31"
#timevariable="date"
#geohash = "dp3wm"
#weather_metric="temp"

#weather_metric_choice= ['temp', 'pressure', 'humidity', 'wind_speed', 'wind_deg','clouds_all']

st.markdown("### Explore it further")

with st.form('Please pick a starting and an end date'):
    start_date_all=st.date_input('Start date',
                                 value=datetime.date(2021, 7, 1))
    end_date_all=st.date_input('End date',
                                 value=datetime.date(2021, 12, 31))

    #wmc=st.selectbox('Select the weather metric', weather_metric_choice)


    st.form_submit_button("Let's go!")

start_time = start_date_all
end_time = end_date_all
timevariable="date"
weather_metric = "temp"

fig=plot_rides_all(start_time,end_time,
                       rides_df_daily,avg_weather_df,
                       timevariable,
                       weather_metric)

st.pyplot(fig)


st.markdown("## Temporality")

st.markdown("Bikes traffic usually differs during weekends from weekdays.")
st.markdown("Within a weekday it is usually higher during commuting time, while higher on saturdays evenings during weekends.")

st.markdown("## Spatial disparities")

st.markdown("Bike stations' density differs across Chicago. Some areas are likely to feature more bikes' departures or arrivals because of this, but also because of idiosyncrasies such as a concentration of business premises, bars and restaurants, which yield specific patterns for bikes traffic")

station_df = get_station_data()

capacity_df = station_df[['capacity']]
capacity_df=capacity_df.drop_duplicates().reset_index(drop=True)
capacity_df = capacity_df.sort_values(by="capacity",ascending=True)
capacity_df = capacity_df[capacity_df["capacity"]>0]
station_df_red = station_df[["lat","lon"]]


st.markdown("### Stations location across Chicago")

st.map(station_df_red)

st.markdown("### Density of stations")

m = Map([41.8781, -87.6298], zoom_start=8)

# convert to (n, 2) nd-array format for heatmap
stationArr = station_df_red.values

# plot heatmap
m.add_child(plugins.HeatMap(stationArr, radius=11))


folium_static(m, width=700, height=600)
