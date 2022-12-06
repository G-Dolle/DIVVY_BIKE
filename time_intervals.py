import pandas as pd
import numpy as np
import os

path0 = os.path.dirname(__file__)
path = os.path.join(path0, 'raw_data', 'Divvy_Trips_2021_Q1.csv')

df=pd.read_csv(path)
df.dtypes
print(df.head())
