import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta, datetime
import os

from functions import return_date, change_date, return_time_diff, fix_missing_date, find_trigger_time, adjust_timestamp

# Get the current working directory and append "data/"
data_dir = os.path.join(os.getcwd(), "data/")

# get list of the .LOG files using list comprehension
files = [file for file in os.listdir(data_dir) if file.endswith(".LOG")]

# Specify the path to the directory containing the data files
path = "data/"

# Create an empty list to store the dataframes
dfs = []

# Loop through the files in the directory
for file in os.listdir(path):
    # Check if the file is a LOG file
    if file.endswith(".LOG"):
        # Read the CSV file into a dataframe
        new_df = pd.read_csv(os.path.join(path, file), 
                             delimiter=r"[,\s]+", 
                             comment="#", 
                             names=["date", "millis", "sensor_id", "spot_meas"], 
                             engine="python")
        # Append the dataframe to the list of dataframes
        dfs.append(new_df)

# Concatenate all the dataframes into a single dataframe
df = pd.concat(dfs, ignore_index=True)

#Change dates from String to datetime object
df['date'] = df.apply(change_date, axis=1)

#Get list of sensor ids
ids = pd.unique(df["sensor_id"])

#initialize empty list for dataframes
dfs = []
# define a Trigger time to set for all Sensors
trigger_time = datetime.strptime("2023-03-02 15:51:59",'%Y-%m-%d %H:%M:%S')

#loop over the sensor ids
for i in ids:
    # if they have only one unique value in "dates" they miss a proper timestamp
    if len(df[df["sensor_id" ] == i]["date"].unique()) == 1:
        print("Triggered else for ID: "+ i)
        mask = df["sensor_id"] == i
        # use fix missing date function from functions.py to add dates to the df
        df.loc[mask, "date"] = df.loc[mask].apply(fix_missing_date, axis=1)  
    # adjust the timestamp to the defined trigger time   
    adjust_timestamp(trigger_time,i)
    dfs.append(df[df["sensor_id" ] == i].pivot(index="date", columns="sensor_id", values="spot_meas"))

fig, ax = plt.subplots(nrows=1
                         ,ncols=1
                         ,figsize=(6.4,4.8)
                         ,dpi = 150
                        )
#fig.suptitle('Data From 1850 to 2015', fontsize=16)
fig.tight_layout()
#ax.set_title("March")
for i_df in dfs:
    i_df.plot(ax=ax)

plt.savefig("plots/1st_plot.pdf")
plt.close()