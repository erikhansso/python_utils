import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randn
import pandas as pd
from pandas import Series, DataFrame


# The csv file for forex is 1-m data, 24 h a day, but SKIPPING WEEKENDS
# Take this into account when doing time deltas
headers = ['Ticker', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Vol']

csv_input_filepath = "pathtocsvfile"
csv_output_filepath = "desiredoutputpath"
# Gotta specify dtypes cause pandas fucks it up and trims 0's from the timestamp
dataframe = pd.read_csv(csv_input_filepath, delimiter=",", names=headers,
                        dtype={'Date': str, 'Time': str, 'Open': float, 'High': float, 'Low': float, 'Close': float})

dataframe['Time'] = dataframe['Time'].astype(str).str[:4]
dataframe['DateTime'] = dataframe['Date'].astype(str).str.cat(dataframe['Time'].astype(str), sep=" ")
dataframe['DateTime'] = pd.to_datetime(dataframe['DateTime'], errors="coerce", format='%Y%m%d %H%M')

trimmed_df = DataFrame(dataframe, columns=['DateTime', 'Open', 'High', 'Low', 'Close'])

trimmed_df.to_csv(csv_output_filepath, index=False)

# Examples of calculating time deltas:
#
# delta = trimmed_df['DateTime'][20000] - trimmed_df['DateTime'][1]
#
# print(delta)
#
# print(delta.total_seconds())
#
# print(delta.days)
#
# minutes = divmod(delta.total_seconds(), 60)[0]
#
# print("minutes: ", minutes)

