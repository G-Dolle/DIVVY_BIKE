
import pandas as pd
import numpy as np
import datetime as dt
from ml_logic.data_import import get_station_data

def weather_cleaning(df):
    '''
    This function cleans the weather data by removing characters from the dt_iso variable
    to allow the creation of a datetime variable

    It also removes the duplicates and selects the relevant features

    '''

    features = ["dt_iso","temp","pressure","humidity","wind_speed","wind_deg","clouds_all"]

    df_clean_tmp=df[features]

    df_clean_tmp = df_clean_tmp.drop_duplicates()

    df_clean_tmp["dt_iso"] = df_clean_tmp["dt_iso"].apply(lambda x: x.replace("+0000 UTC", ""))

    df_clean_tmp["dt_iso"] = pd.to_datetime(df_clean_tmp["dt_iso"])
    df_clean_tmp['hourly_data']=df_clean_tmp['dt_iso']

    return df_clean_tmp

def cleaning_divvy_gen(df):

    df['started_at']=pd.to_datetime(df['started_at'])
    df['ended_at']=pd.to_datetime(df['ended_at'])
    df['hourly_data_started'] = df.started_at.dt.round('60min')
    df['hourly_data_ended'] = df.ended_at.dt.round('60min')

    df_departures=df[[
                    "start_station_name",
                    "start_station_id",
                    "hourly_data_started"]]

    df_departures=df_departures.rename(columns={'hourly_data_started':'hourly_data',
                                                "start_station_name":"station_name",
                                                "start_station_id": "station_id"})

    df_departures["nb_departures"]=1

    df_dep_agg=df_departures.groupby(by=["station_name",
                                        "station_id",
                                        'hourly_data']).count().reset_index()


    df_arrivals=df[["end_station_name",
                 "end_station_id",
                 "hourly_data_ended"]]

    df_arrivals=df_arrivals.rename(columns={'hourly_data_ended':'hourly_data',
                                            "end_station_name":"station_name",
                                            "end_station_id": "station_id"})
    df_arrivals["nb_arrivals"]=1

    df_arr_agg=df_arrivals.groupby(by=["station_name",
                                            "station_id",
                                            'hourly_data']).count().reset_index()

    merge_ratio=pd.merge(
    df_dep_agg,
    df_arr_agg,
    how="outer",
    on=['hourly_data',"station_name","station_id"])


    merge_ratio["nb_departures"] = merge_ratio["nb_departures"].replace(np.nan, 0)
    merge_ratio["nb_arrivals"] = merge_ratio["nb_arrivals"].replace(np.nan, 0)

    merge_ratio['ratio']=merge_ratio['nb_departures']/merge_ratio['nb_arrivals']

    return merge_ratio


def merge_divvy_weather(df_bikes , df_weather):

    '''
    This function merges the Divvy data aggregated at the station and hourly level
    with the hourly weather cleaned data
    '''

    merged_df = df_bikes.merge(df_weather,
    how="left",
    on='hourly_data')

    return merged_df

def features_target(df, target):
    '''
    This function creates the features and target dataframes, the latter
    being created by identifying the target (nb_departures, nb_arrivals, ratio of the two)
    as an argument
    '''

    features_df = df.drop(columns=["ratio","nb_departures","nb_arrivals"])
    target_df =  df[target]

    return features_df, target_df
