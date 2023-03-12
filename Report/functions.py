# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
from datetime import datetime
# from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def return_date(string):
    date_format = '%Y-%m-%d %H:%M:%S'
    date_str = string.replace('T', ' ').replace('Z', '')
    return datetime.strptime(date_str, date_format)

def change_date(row):
    date_format = '%Y-%m-%d %H:%M:%S'
    date_str = row['date'].replace('T', ' ').replace('Z', '')
    date = datetime.strptime(date_str, date_format)
    return date

def return_time_diff(row):
    date1 = "2023-01-13T16:30:16Z" #Initialization time
    date2 = "2023-01-17T15:01:19Z" #first timestamp
    first_time = return_date(date2)
    later_time = row["time"]
    diff_td = later_time - first_time
    diff_seconds = diff_td.total_seconds()
    return  int(diff_seconds)

def fix_missing_date(row):
    init_date = return_date("2023-03-02T15:47:54Z")
    date = init_date + timedelta(0,int(row["millis"]/1000))
    return date

def find_trigger_time(df):
    trigg = df[df["spot_meas"].diff() < -2.3].iloc[0]["date"]
    return trigg

def adjust_timestamp(trig_time,ID,df):
    mask = df["sensor_id"] == ID
    df_trig_time = find_trigger_time(df[df["sensor_id"] == ID])
    diff_time = trig_time - df_trig_time
    df.loc[mask, "date"] = df.loc[mask, "date"] + diff_time