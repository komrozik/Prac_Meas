import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
from datetime import datetime
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

df = pd.read_csv("preparation_tasks/data/tsticks.log"
                 ,delimiter = ", "
                 , comment = "#"
                ,names = ["module","HEX ID","timestamp","sensor1","sensor2","sensor3","sensor4","sensor5","sensor6","sensor7","sensor8"]
                )


# timestamps in Zeitdifferenzen umwandeln

def return_date(string):
    string = string.replace("T", " " )
    string = string.replace("Z", "" )
    date = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
    return date

def return_time_diff(row):
    date1 = "2023-01-13T16:30:16Z" #Initialization time
    date2 = "2023-01-17T15:01:19Z" #first timestamp
    first_time = return_date(date2)
    later_time = return_date(row["timestamp"])
    difference = later_time - first_time
    seconds_in_day = 24 * 60 * 60
    min_sec = divmod(difference.days * seconds_in_day + difference.seconds, 60)
    return min_sec[0]*60+min_sec[1]

df['time_diff'] = df.apply(return_time_diff, axis=1)

df_50163d = df[df["HEX ID"] == "50163d"]
df_554f2d = df[df["HEX ID"] == "554f2d"]


Z = np.array([df_50163d["sensor8"].to_numpy()
     ,df_50163d["sensor7"].to_numpy()
     ,df_50163d["sensor6"].to_numpy()
     ,df_50163d["sensor5"].to_numpy()
     ,df_50163d["sensor4"].to_numpy()
     ,df_50163d["sensor3"].to_numpy()
     ,df_50163d["sensor2"].to_numpy()
     ,df_50163d["sensor1"].to_numpy()
    ])

x = df_50163d["time_diff"]
y = np.arange(8)
X, Y = np.meshgrid(x, y)

Z2 = np.array([df_554f2d["sensor8"].to_numpy()
     ,df_554f2d["sensor7"].to_numpy()
     ,df_554f2d["sensor6"].to_numpy()
     ,df_554f2d["sensor5"].to_numpy()
     ,df_554f2d["sensor4"].to_numpy()
     ,df_554f2d["sensor3"].to_numpy()
     ,df_554f2d["sensor2"].to_numpy()
     ,df_554f2d["sensor1"].to_numpy()
    ])

x2 = df_554f2d["time_diff"]
y2 = np.arange(8)
X2, Y2 = np.meshgrid(x2, y2)

fig, ax = plt.subplots(1,2,figsize=(2*7.2,4.4),constrained_layout = True)
CS = ax[0].contourf(X/(60**2),Y,Z,10, cmap = "coolwarm")

ax[0].set_title('50163d Data')
ax[0].set_xlabel('Time [h]')
ax[0].set_ylabel('Sensor')
labels = [item.get_text() for item in ax[0].get_yticklabels()]
labels = ["Sensor 8"
          ,"Sensor 7"
          ,"Sensor 6"
          ,"Sensor 5"
          ,"Sensor 4"
          ,"Sensor 3"
          ,"Sensor 2"
          ,"Sensor 1"]
ax[0].set_yticklabels(labels)



CS2 = ax[1].contourf(X2/(60**2),Y2,Z2,10, cmap="coolwarm")

ax[1].set_title('50163d Data')
ax[1].set_xlabel('Time [h]')
ax[1].set_ylabel('Sensor')
labels = [item.get_text() for item in ax[1].get_yticklabels()]
labels = ["Sensor 8"
          ,"Sensor 7"
          ,"Sensor 6"
          ,"Sensor 5"
          ,"Sensor 4"
          ,"Sensor 3"
          ,"Sensor 2"
          ,"Sensor 1"]
ax[1].set_yticklabels(labels)

cbar=fig.colorbar(CS2)
cbar.ax.set_ylabel('Temperature')

plt.savefig("plot1.pdf")
plt.close()


#--------------------------

#Teil b

path = "preparation_tasks/data/tsensors_multiple_files/"
df = pd.DataFrame()
for i in np.arange(1,8):
    new_df = pd.read_csv(path+"group0"+str(i)+".log"
                     ,delimiter = ", "
                     , comment = "#"
                    ,names = ["timestamp","group","spot_meas","avg_meas"]
                    ,engine = "python"
                    )
    df = pd.concat([df,new_df],ignore_index=True)
    
df['time_diff'] = df.apply(return_time_diff, axis=1)
df['time_diff'] = df['time_diff']+17533961 #remove offset due to wrong start time

fig, ax = plt.subplots(1,1,figsize=(2*7.2,4.4),constrained_layout = True)
for i in np.arange(1,8):
    plt.plot(df[df["group"]== i]["time_diff"]
            ,df[df["group"]== i]["avg_meas"]
            ,label = f"Group {i}")
plt.legend()

plt.savefig("plot2.pdf")
plt.close()




Z = np.array([df[df["group"]== 1]["avg_meas"].to_numpy()[0:2914]
     ,df[df["group"]== 2]["avg_meas"].to_numpy()[0:2914]
     ,df[df["group"]== 3]["avg_meas"].to_numpy()[0:2914]
     ,df[df["group"]== 4]["avg_meas"].to_numpy()[0:2914]
     ,df[df["group"]== 5]["avg_meas"].to_numpy()[0:2914]
     ,df[df["group"]== 6]["avg_meas"].to_numpy()[0:2914]
     ,df[df["group"]== 7]["avg_meas"].to_numpy()[0:2914]
    ])

x = df[df["group"]== 1]["time_diff"]
y = np.arange(1,8)
X, Y = np.meshgrid(x, y)

fig, ax = plt.subplots(1,1,figsize=(2*7.2,4.4),constrained_layout = True)
CS = ax.contourf(Z,10, cmap="coolwarm")

ax.set_title('Part b Data')
ax.set_xlabel('Time')
ax.set_ylabel('Sensor')
labels = [item.get_text() for item in ax.get_yticklabels()]
labels = ["Sensor1"
          ,"Sensor2"
          ,"Sensor3"
          ,"Sensor4"
          ,"Sensor5"
          ,"Sensor6"
          ,"Sensor7"]
ax.set_yticklabels(labels);

cbar = fig.colorbar(CS)
cbar.ax.set_ylabel('Temperature')

plt.savefig("plot3.pdf")
plt.close()