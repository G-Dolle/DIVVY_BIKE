import math
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer, StandardScaler

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

        final_preprocessor = ColumnTransformer(
                    [
                        ("time_preproc", time_pipe, ["hourly_data"]),
                        ("weather_scaler",weather_pipe, weather_features),
                        #("geohash", geohash_pipe, lonlat_features),
                    ],
                    n_jobs=-1,
                )
        return final_preprocessor

    preprocessor = create_sklearn_preprocessor()

    X_processed = preprocessor.fit_transform(X)

    X_processed_df = pd.DataFrame(X_processed)

    return preprocessor, X_processed_df

def target_process(df):

    df.replace(np.inf, 1000, inplace=True)

    return df
