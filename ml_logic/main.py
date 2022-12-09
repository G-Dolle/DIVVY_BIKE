import os
import pandas as pd
import numpy as np
import math

from ml_logic.data_import import get_weather_data, get_divvy_data
from ml_logic.cleaning import weather_cleaning, cleaning_divvy_gen, merge_divvy_weather, features_target
from ml_logic.preprocessor import transform_time_features, preprocess_features, target_process




def preprocess(target_chosen):

    # Import data

    quarter= os.environ.get("DIVVY_QUARTER")
    year= os.environ.get("DIVVY_YEAR")

    raw_divvy_df = get_divvy_data(year,quarter)
    raw_weather_df = get_weather_data()

    print("Raw data imported")

    # Clean data & merge data

    clean_divvy_df = cleaning_divvy_gen(raw_divvy_df)
    clean_weather_df = weather_cleaning(raw_weather_df)

    merged_df = merge_divvy_weather(clean_divvy_df, clean_weather_df)

    print("Data cleaned and merged")

    # Create features and target dataframes

    X, y = features_target(merged_df, target_chosen)

    print("features and target dataframes created")

    # preprocess features
    preprocessor, X_processed_df = preprocess_features(X)

    print("features preprocessed")

    # preprocess target

    if target_chosen == "ratio":
        y_processed_df = target_process(y)
        print("ratio picked as target, and preprocessed")
    else:
        y_processed_df = y

        print(f"{target_chosen} picked as target")

    print("Preprocessing of Training set is done")

    return X_processed_df, y_processed_df, preprocessor


# preprocessing a test set

def preprocess_test(preprocessor, target_chosen):

    # Import data
    quarter= os.environ.get("DIVVY_QUARTER_TEST")
    year= os.environ.get("DIVVY_YEAR_TEST")

    raw_divvy_df = get_divvy_data(year,quarter)
    raw_weather_df = get_weather_data()

    print("Test Raw data imported")

    # Clean data & merge data

    station_name = os.environ.get("DIVVY_STATION_NAME")

    clean_divvy_df = cleaning_divvy(raw_divvy_df,station_name)
    clean_weather_df = weather_cleaning(raw_weather_df)

    merged_df = merge_divvy_weather(clean_divvy_df, clean_weather_df)

    print("Test Data cleaned and merged")

    # Create features and target dataframes

    X_test, y_test = features_target(merged_df, target_chosen)

    print("Test features and target dataframes created")

    # transform the features test set

    X_test_processed = preprocessor.transform(X_test)

    # preprocess target

    if target_chosen == "ratio":
        y_test_processed = target_process(y_test)
        print("ratio picked as target, and preprocessed")
    else:
        y_test_processed = y_test

        print(f"{target_chosen} picked as target")

    print("Preprocessing of test set is done")

    return X_test_processed, y_test_processed

# train model

# Save model

# Evaluate model

# predict


if __name__ == '__main__':
    target_chosen = os.environ.get("TARGET_CHOSEN")
    X_processed_df, y_processed_df, preprocessor = preprocess(target_chosen)
    X_test_processed, y_test_processed=preprocess_test(preprocessor, target_chosen)
