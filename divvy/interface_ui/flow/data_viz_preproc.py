import os
import pandas as pd

from divvy.ml_logic.data_import import get_divvy_data, get_weather_data
from divvy.ml_logic.cleaning import compute_geohash_stations,weather_cleaning, cleaning_divvy_gen,cleaning_divvy_gen_agg, merge_divvy_weather, features_target
from divvy.ml_logic.preprocessor import transform_time_features, preprocess_features, target_process


raw_weather_df = get_weather_data()
clean_weather_df = weather_cleaning(raw_weather_df)

divvy_q1_2021 = get_divvy_data(2021,"Q1")

divvy_q2_2021 = get_divvy_data(2021,"Q2")
divvy_q3_2021 = get_divvy_data(2021,"Q3")
divvy_q4_2021 = get_divvy_data(2021,"Q4")


rides_df = pd.concat([divvy_q1_2021,divvy_q2_2021, divvy_q3_2021,divvy_q4_2021])

rides_df = rides_df[rides_df["start_station_name"].isnull()==False]
rides_df['started_at']=pd.to_datetime(rides_df['started_at'])
rides_df['hourly_data_started'] = rides_df.started_at.dt.round('60min')

rides_df = rides_df[["start_station_name","ride_id","hourly_data_started"]]
rides_df.rename(columns={"start_station_name":"station_name"}, inplace=True)


precision_level= int(os.environ.get("PRECISION_LEVEL"))
geohash_station_df = compute_geohash_stations(precision = precision_level)

rides_df = rides_df.merge(geohash_station_df, on="station_name", how="left")

rides_df["date"]= pd.to_datetime(rides_df["hourly_data_started"]).dt.date
rides_df["nb_rides"]=1

rides_df_daily_geohash = rides_df.groupby(by=["geohash","date"])["nb_rides"].sum().reset_index()
rides_df_daily = rides_df.groupby(by=["date"])["nb_rides"].sum().reset_index()

clean_weather_df["date"]= pd.to_datetime(clean_weather_df["hourly_data"]).dt.date
avg_weather_df = clean_weather_df.groupby(by=["date"])["temp",
                                                    "pressure",
                                                    'humidity',
                                                    'wind_speed',
                                                    'wind_deg',
                                                    "clouds_all"].mean().reset_index()

rides_df_daily_geohash.to_csv("raw_data/rides_df_daily_geohash_2021.csv", index=False)

rides_df_daily.to_csv("raw_data/rides_df_daily_2021.csv", index=False)
avg_weather_df.to_csv("raw_data/avg_temp.csv", index=False)
