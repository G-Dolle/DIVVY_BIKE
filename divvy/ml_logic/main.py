import os
import pandas as pd
import numpy as np
import math

from divvy.ml_logic.data_import import get_weather_data, get_divvy_data
from divvy.ml_logic.cleaning import compute_geohash_stations,weather_cleaning, cleaning_divvy_gen,cleaning_divvy_gen_agg, merge_divvy_weather, features_target
from divvy.ml_logic.preprocessor import transform_time_features, preprocess_features, target_process
from divvy.ml_logic.model import initialize_model_departure, initialize_model_arrival,train_model, save_model, load_model, load_preprocessor, predict

def preprocess(target_chosen):

    # Import data

    quarter= os.environ.get("DIVVY_QUARTER")
    year= os.environ.get("DIVVY_YEAR")

    raw_divvy_df = get_divvy_data(year,quarter)
    raw_weather_df = get_weather_data()

    print("Raw data imported")

    # Clean data & merge data

    clean_divvy_df = cleaning_divvy_gen_agg(raw_divvy_df)
    clean_weather_df = weather_cleaning(raw_weather_df)

    merged_df = merge_divvy_weather(clean_divvy_df, clean_weather_df)

    print("Data cleaned and merged")

    # Create features and target dataframes

    X, y = features_target(merged_df, target_chosen)

    print("features and target dataframes created")

    # Extracting geohash retained in the training set for prediction

    #geohash_df = get_retained_geohash(X)

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

    clean_divvy_df = cleaning_divvy_gen_agg(raw_divvy_df)
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

if __name__ == '__main__':
    # get the preprocessed data of arrival
    target_chosen = "nb_arrivals"
    X_processed_df_arrival, y_processed_df_arrival, preprocessor_arrival = preprocess(target_chosen)
    X_test_processed_arrival, y_test_processed_arrival=preprocess_test(preprocessor_arrival, target_chosen)
    # initialize model
    model_arrival = initialize_model_arrival()
    # train model
    model_arrival = train_model(model_arrival, X_processed_df_arrival, y_processed_df_arrival)
    # save model
    save_model('arrival', model_arrival, type="model")
    # save preprocessor
    save_model('arrival', preprocessor_arrival, type="preprocessor")
    # predict
    model_arrival = load_model(kind="arrival")
    preprocessor_arrival = load_preprocessor(kind="arrival")
    new_X = preprocessor_arrival(input_X)
    y_pred_arrival = predict(model_arrival, new_X)

    # get the preprocessed data of departure
    target_chosen = "nb_departures"
    X_processed_df_departure, y_processed_df_departure, preprocessor_departure = preprocess(target_chosen)
    X_test_processed_departure, y_test_processed_departure=preprocess_test(preprocessor_departure, target_chosen)
    # initialize model
    model_departure = initialize_model_departure()
    # train model
    model_departure = train_model(model_departure, X_processed_df_departure, y_processed_df_departure)    
    # save model
    save_model('departure', model_departure, type="model")
    # save preprocessor
    save_model('departure', preprocessor_departure, type="preprocessor")
    # predict
    model_departure = load_model(kind="departure")
    preprocessor_departure = load_preprocessor(kind="departure")
    new_X = preprocessor_departure(input_X)
    y_pred_departure = predict(model_departure, new_X)
