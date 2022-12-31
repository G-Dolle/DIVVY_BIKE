import streamlit as st
import time
import numpy as np
from folium import Map, plugins
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime
from streamlit_folium import folium_static
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

st.set_page_config(page_title="Factors influencing bikes traffic",  layout="centered")

st.sidebar.header("Analysis")

st.markdown("# What drives bikes traffic?")

st.markdown("## Weather")

st.markdown("The better the weather, the nicer it is to ride a bike across the city. Not surprisingly, bikes traffic and temperature follow similar trends.")


def get_station_data():

    path = os.environ.get("LOCAL_DATA_PATH_STATION")

    station_df = pd.read_csv(path)

    return station_df



rides_df_daily=pd.read_csv("raw_data/rides_df_daily_2021.csv")
rides_df_daily["date"]= pd.to_datetime(rides_df_daily["date"])

avg_weather_df=pd.read_csv("raw_data/avg_temp.csv")
avg_weather_df["date"]= pd.to_datetime(avg_weather_df["date"])

rides_df_daily_geohash=pd.read_csv("raw_data/rides_df_daily_geohash_2021.csv")
rides_df_daily_geohash["date"]= pd.to_datetime(rides_df_daily_geohash["date"])

rides_df_daily = rides_df_daily.merge(avg_weather_df, on="date", how="left")


hour_w_agg_df = pd.read_csv("raw_data/hourly_avg_rides_2021.csv")

def timeframe_df(df,start_time,end_time):

    condition_1 = df["date"] >= pd.to_datetime(start_time)
    condition_2 = df["date"] <= pd.to_datetime(end_time)

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


def plot_rides_all_bis(start_time,end_time,df_divvy):

    df_divvy["nb_rides"] = df_divvy["nb_rides"]/1000

    df_divvy_red = timeframe_df(df_divvy,start_time,end_time)

    df_divvy_red = df_divvy_red.set_index('date')

    rides_trend = seasonal_decompose(df_divvy_red['nb_rides'], model='additive')
    temp_trend = seasonal_decompose(df_divvy_red['temp'], model='additive')

    fig, ax1 = plt.subplots()

    ax1 = sns.lineplot(rides_trend.trend, color=(43/255,140/255,190/255), legend=True)
    ax2 = ax1.twinx()
    sns.lineplot(temp_trend.trend, ax=ax2, color=(222/255,45/255,38/255), legend=True)

    ax1.set_xlabel('Time')
    ax1.set_ylabel("Daily number of bike rides ('000s)", color=(43/255,140/255,190/255))
    ax2.set_ylabel('Temperature (°c)', color=(222/255,45/255,38/255))

    return fig


fig0, ax1 = plt.subplots()

ax1 = sns.scatterplot(data = rides_df_daily, x="temp",y="nb_rides", color=(54/255,144/255,192/255))
ax1.set_title("Daily number of bike rides against daily temperature")
ax1.set_xlabel("Daily average temperature (°c)")
ax1.set_ylabel("Number of bike rides ('000s)")
ax1.set_xticks(range(-20,35,10))
ax1.set_yticks(range(0,40,10))

st.pyplot(fig0)

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

fig=plot_rides_all_bis(start_time,end_time,
                       rides_df_daily)

st.pyplot(fig)


st.markdown("## Temporality")

st.markdown("Bikes traffic is overall higher on weekends than on weekdays.")

rides_df_daily["dayofweek"] = rides_df_daily['date'].dt.dayofweek
rides_df_daily['category'] = (rides_df_daily['dayofweek'] >= 5)
rides_df_daily["category"].replace({False:0,True:1}, inplace=True)
test_df = rides_df_daily.groupby(by="dayofweek")["nb_rides"].mean().reset_index()

test_df["dayofweek"].replace({0:"Monday",
                              1:"Tuesday",
                              2: "Wednesday",
                              3:"Thursday",
                              4:"Friday",
                              5:"Saturday",
                              6:"Sunday"},inplace=True)


rides_df_daily["dayofweek"] = rides_df_daily['date'].dt.dayofweek
rides_df_daily['category'] = (rides_df_daily['dayofweek'] >= 5)
rides_df_daily["category"].replace({False:0,True:1}, inplace=True)
test_df = rides_df_daily.groupby(by="category")["nb_rides"].mean().reset_index()

test_df["category"].replace({0:"weekdays",1:"weekends"},inplace=True)
color =[(116/255,169/255,207/255),(5/255,112/255,176/255)]

fig2, ax1 = plt.subplots()
ax1 = sns.barplot(x=test_df["category"],y=test_df["nb_rides"], palette=color)

ax1.set_title('Average daily number of bike rides, weekdays vs weekends')
ax1.set_xlabel('')
ax1.set_ylabel("number of bike rides ('000s)")



st.pyplot(fig2)

st.markdown("Within a weekday it is usually higher during commuting time, while following a bell-shape trend on weekends.")

fig3, ax4 = plt.subplots()


ax4 = sns.lineplot(x=hour_w_agg_df.loc[hour_w_agg_df["category"]==0,"hour"],
             y=hour_w_agg_df.loc[hour_w_agg_df["category"]==0,"nb_rides"],
             color=(116/255,169/255,207/255), label="Weekdays")

ax5 = sns.lineplot(x=hour_w_agg_df.loc[hour_w_agg_df["category"]==1,"hour"],
             y=hour_w_agg_df.loc[hour_w_agg_df["category"]==1,"nb_rides"],
             color=(5/255,112/255,176/255),
             label="weekend")


ax4.set_title('Average number of bike rides per hour of the day')
ax4.set_xlabel('Hour of the day')
ax4.set_ylabel("Number of bike rides")
ax4.set_xticks(range(0,24,2))
ax4.legend()

st.pyplot(fig3)


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
