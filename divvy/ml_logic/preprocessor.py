import math
import numpy as np
import pandas as pd
import pygeohash as gh
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer, StandardScaler
from ml_logic.data_import import get_station_data
import pygeohash as gh

def transform_time_features(X: pd.DataFrame) -> np.ndarray:

    assert isinstance(X, pd.DataFrame)
    hourly_data = pd.to_datetime(X["hourly_data"],
                            format="%Y-%m-%d %H:%M:%S UTC",
                            utc=True)
    hourly_data = hourly_data.dt.tz_convert("America/Chicago").dt
    dow = hourly_data.weekday
    hour = hourly_data.hour
    month = hourly_data.month
    #year = hourly_data.year
    hour_sin = np.sin(2 * math.pi / 24 * hour)
    hour_cos = np.cos(2 * math.pi / 24 * hour)

    result = np.stack([hour_sin, hour_cos, dow, month], axis=1)
    return result


def preprocess_features(X: pd.DataFrame) -> np.ndarray:

    def create_sklearn_preprocessor() -> ColumnTransformer:

        time_categories = {
                    0: np.arange(0, 7, 1),  # days of the week
                    1: np.arange(1, 13, 1)  # months of the year
                    # will need to add one cat for the year when generalizing
                }

        time_pipe = make_pipeline(
                FunctionTransformer(transform_time_features),
                make_column_transformer(
                    (OneHotEncoder(
                        categories=time_categories,
                        sparse=False,
                        handle_unknown="ignore"), [2,3]), # correspond to columns ["day of week", "month"], not the others columns
                    #(FunctionTransformer(lambda year: (year-year_min)/(year_max-year_min)), [4]), # min-max scale the columns 4 ["year"]
                    remainder="passthrough" # keep hour_sin and hour_cos
                    )
                )

        weather_pipe = make_pipeline(StandardScaler())
        weather_features = ["temp","pressure","humidity","wind_speed","wind_deg","clouds_all"]

        # def compute_geohash_stations(precision: int = 4) -> np.ndarray:
        #             """
        #             Add a geohash (ex: "dr5rx") of len "precision" = 5 by default
        #             corresponding to each (lon,lat) tuple, for pick-up, and drop-off
        #             """
        #             df_stations=get_station_data()
        #             assert isinstance(df_stations, pd.DataFrame)

        #             df_stations["geohash"] = df_stations.apply(lambda x: gh.encode(
        #                 x.lat, x.lon, precision=precision),
        #                                             axis=1)
        #             df_stations_reduced=df_stations[["name","legacy_id",'geohash']]
        #             df_stations_reduced.rename(columns={"name":"start_station_name",
        #                                         "legacy_id":"station_id"}, inplace=True)

        #             return df_stations_reduced

        # geohash_categories = {
        #     0:'dp3w',
        #     1:'dp3t',
        #     2:'dp3x',
        #     3:'dp3v',
        #     4:'dp3s'
        #     # 5:'dp3u'
        # }

        # geohash_pipe = OneHotEncoder(
        #     # categories=geohash_categories,
        #     sparse=False,
        #     handle_unknown="ignore")#),
        # # remainder="passthrough"

        cat_transformer = OneHotEncoder(sparse=False, handle_unknown="ignore")

        final_preprocessor = ColumnTransformer(
                    [
                        ("time_preproc", time_pipe, ["hourly_data"]),
                        ("weather_scaler",weather_pipe, weather_features),
                        ("geohash encoding", cat_transformer,["geohash"])
                    ],
                    n_jobs=-1,
                )
        return final_preprocessor


    preprocessor = create_sklearn_preprocessor()

    X = X.drop(columns=["dt_iso"])

    X_processed = preprocessor.fit_transform(X)

    X_processed_df = pd.DataFrame(X_processed)

    return preprocessor, X_processed_df


def final_preproc(X_processed_df,df_stations_reduced):

        # Calling Geohash function and creating Stations Dataframe
        df_stations_reduced=compute_geohash_stations(precision=4)

        # Merge divvy data & station data
        X_complete=X.merge(df_stations_reduced,how='left',on=['start_station_name'])

        return X_complete


def target_process(df):

    df.replace(np.inf, 1000, inplace=True)

    return df
