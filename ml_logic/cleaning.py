
import pandas as pd
import numpy as np

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

def station_stats(df,station_id):
    '''
    This function computes the number of arrivals and departures for a given
    station, identified by its station_id value. It finally computes
    the ratio of departures over arrivals
    '''

    station_id = str(station_id)

    df['started_at']=pd.to_datetime(df['started_at'])
    df['ended_at']=pd.to_datetime(df['ended_at'])
    df['hourly_data'] = df.started_at.dt.round('60min')


    # Departures per station
    df_departures=df[df['start_station_id']==station_id]
    df_departures=df_departures[['started_at','hourly_data_started']]
    df_departures=df_departures.rename(columns={'hourly_data_started':'hourly_data'})
    df_departures=df_departures.groupby(by='hourly_data').count()


    # Arrivals per station
    df_arrivals=df[df['start_station_id']=='station_id']
    df_arrivals=df_arrivals[['ended_at','hourly_data_ended']]
    df_arrivals=df_arrivals.rename(columns={'hourly_data_ended':'hourly_data'})
    df_arrivals=df_arrivals.groupby(by='hourly_data').count()

    # Merge departures and arrivals to get a ratio
    final_df=pd.merge(
    df_departures,
    df_arrivals,
    how="outer",
    on='hourly_data')

    final_df.rename(columns={"ended_at":"nb_arrivals","started_at":"nb_departures"}, inplace=True)

    # Replacing missing values by zero in case of no arrivals, no departures during a given hour
    final_df["nb_departures"] = final_df["nb_departures"].replace(np.nan, 0)
    final_df["nb_arrivals"] = final_df["nb_arrivals"].replace(np.nan, 0)

    final_df['ratio']=final_df['started_at']/final_df['ended_at']

    # Return the merged dataset
    return final_df


def cleaning_divvy(df,station_name):

    df['started_at']=pd.to_datetime(df['started_at'])
    df['ended_at']=pd.to_datetime(df['ended_at'])
    df['hourly_data'] = df.started_at.dt.round('60min')

    # Focusing on departures
    departures_df = df.drop(columns=["end_station_name","end_station_id","end_lat","end_lng","ended_at","start_lat","start_lng",
                                    "member_casual"])

    departures_df_reduced=departures_df.loc[departures_df["start_station_name"]==station_name]
    departures_df_reduced["nb_departures"]=0
    departures_df_final = pd.DataFrame(departures_df_reduced.groupby(['hourly_data',
                                                      "start_station_name",
                                                                      "start_station_id"],
                                                     as_index=False)["nb_departures"].count())

    # Focusing on arrivals
    arrivals_df = df.drop(columns=["start_station_name","start_station_id","end_lat","end_lng","started_at","start_lat","start_lng",
                                 "member_casual"])

    arrivals_df["nb_arrivals"]=0
    arrivals_df_reduced=arrivals_df.loc[arrivals_df["end_station_name"]==station_name]
    arrivals_df_final = pd.DataFrame(arrivals_df_reduced.groupby(['hourly_data',"end_station_name",
                                                                      "end_station_id"], as_index=False)['nb_arrivals'].count())

    arrivals_df_final= arrivals_df_final.drop(columns=["end_station_name","end_station_id"])

    final_df = arrivals_df_final.merge(departures_df_final, how="outer", on="hourly_data")
    final_df.rename(columns={"start_station_name":"station_name","start_station_id":"station_id"}, inplace=True)

    # Replacing missing values by zero in case of no arrivals, no departures during a given hour

    final_df["nb_departures"] = final_df["nb_departures"].replace(np.nan, 0)
    final_df["nb_arrivals"] = final_df["nb_arrivals"].replace(np.nan, 0)

    # Computing the ratio of arrivals over departures
    final_df['ratio']=final_df['nb_departures']/final_df['nb_arrivals']

    return final_df


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
