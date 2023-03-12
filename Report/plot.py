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

fig, ax = plt.subplots(nrows=1
                         ,ncols=1
                         ,figsize=(6.4,4.8)
                         ,dpi = 150
                        )
fig.tight_layout()

#loop over the sensor ids
for i in ids:
    # if they have only one unique value in "dates" they miss a proper timestamp
    if len(df[df["sensor_id" ] == i]["date"].unique()) == 1:
        print("Triggered else for ID: "+ i)
        mask = df["sensor_id"] == i
        # use fix missing date function from functions.py to add dates to the df
        df.loc[mask, "date"] = df.loc[mask].apply(fix_missing_date, axis=1) 
    else:
        plt.plot(df[df["sensor_id"]== i]["date"],df[df["sensor_id"] == i]["spot_meas"],label = i) 
    # adjust the timestamp to the defined trigger time   
    adjust_timestamp(trigger_time,i,df)
    dfs.append(df[df["sensor_id" ] == i].pivot(index="date", columns="sensor_id", values="spot_meas"))

plt.legend(loc = "best")
plt.savefig("plots/plot1.pdf")
plt.close()

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

plt.savefig("plots/plot2.pdf")
plt.close()

# Read the first Calibration log file into a Pandas DataFrame with the following settings:
cal_df = pd.read_csv(os.path.join("data/cal/", "tsensor_calibration_time_constant_new.log"), 
                     delimiter=r"[,\s]+",  # Delimiter can be either comma or whitespace
                     comment="#",  # Ignore lines starting with #
                     names=["date", "spot_meas"],  # Set column names
                     engine="python")  # Use the Python engine to read the CSV file

# Read the second Calibration log file into another DataFrame with the same settings:
cal_df2 = pd.read_csv(os.path.join("data/cal/", "tsensor_calibration2.log"), 
                      delimiter=r"[,\s]+", 
                      comment="#", 
                      names=["date", "spot_meas"], 
                      engine="python")

# Prepend the date string "2023-03-02 " to the "date" column in both DataFrames:
cal_df["date"] = "2023-03-02 " + cal_df["date"]
cal_df2["date"] = "2023-03-02 " + cal_df2["date"]

# Apply the "change_date" function to the "date" column in both DataFrames:
cal_df['date'] = cal_df.apply(change_date, axis=1)
cal_df2['date'] = cal_df2.apply(change_date, axis=1)

# Concatenate both DataFrames into a single DataFrame:
cal_df = pd.concat([cal_df, cal_df2], ignore_index=True)

# Set the "date" column as the index of the DataFrame:
cal_df.set_index('date', inplace=True)



fig, ax = plt.subplots(nrows=1
                         ,ncols=1
                         ,figsize=(6.4,4.8)
                         ,dpi = 150
                        )

fig.tight_layout()
ax.set_title('Spot Measurements of the different Sensors')
for i_df in dfs:
    i_df.plot(ax=ax)
 
cal_df.plot(ax=ax)

plt.savefig("plots/plot3.pdf")
plt.close()

for i, i_df in enumerate(dfs): # changed i_df to df to follow standard naming convention for dataframes
    # calculate the difference between the value at the specified time in the current dataframe and the calibration dataframe
    diff = round(i_df.loc["2023-03-02 15:55:01"][0] - cal_df.loc["2023-03-02 15:55:03"][0], 2)
    # subtract the difference from all values in the current dataframe to adjust for calibration
    dfs[i] = i_df - diff

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6.4, 4.8), dpi=150)

fig.tight_layout()
ax.set_title('Rolling mean of different sensors')
ax.scatter(x=cal_df.index, y=cal_df.values, label='Calibration')

for i_df in dfs:
    # Take the rolling mean of the df (mean of the 10 values before) and then print only every tenth value -> avg_meas
    i_df.rolling(10).mean().iloc[::10].plot(ax=ax)

ax.legend()
plt.savefig("plots/plot4.pdf")
plt.close()

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6.4, 4.8), dpi=150)

fig.tight_layout()
ax.set_title('Rolling mean of different sensors')
ax.scatter(x=cal_df.index[4::], y=cal_df.values[4::], label='Calibration')
ax.plot(cal_df.index[4::],cal_df.values[4::]+0.5,color = "red")
ax.plot(cal_df.index[4::],cal_df.values[4::]-0.5,color = "red")

for i_df in dfs:
    # Take the rolling mean of the df (mean of the 10 values before) and then print only every tenth value -> avg_meas
    i_df.rolling(10).mean().iloc[400::10].plot(ax=ax)

ax.legend()
plt.savefig("plots/plot5.pdf")



# Get the index of the rows in the dataframe where the "date" column is equal to the "trigger_time"
start_idx = df[df["date"] == trigger_time].index

# Add 50 to the start index to get the end index
end_idx = start_idx + 50

dfs2 = []

timedel = []
# Loop over the ids and corresponding start and end indices
for idx, i in enumerate(ids):
    # Get the spot_meas value at the start and end indices
    start = df.iloc[start_idx[idx]]["spot_meas"]
    end = df.iloc[end_idx[idx]]["spot_meas"]
    
    # Calculate the cut off value using the start and end values
    cut_off = start - 0.632 * (start - end)
    c = 0
    
    # Loop through the rows from the start index until the cutoff value is reached
    while df.iloc[start_idx[idx] + c]["spot_meas"] > cut_off:
        c += 1

    # Calculate the time delta from the start to the cutoff
    time_delta = (df.iloc[start_idx[idx]+c]["date"] - df.iloc[start_idx[idx]]["date"]).seconds

    # Append the time delta to a list
    timedel.append(time_delta)

print("Average Time constant: ",sum(timedel)/8)
