#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import the modules
import pandas as pd
from pathlib import Path
from datetime import datetime as dt


# In[7]:


# Read the csv files selected into pandas DataFrames
df_Jul13 = pd.read_csv(Path("201307-citibike-tripdata_1.csv"))
df_Mar14 = pd.read_csv(Path("201403_citibike_tripdata_1.csv"))
df_Mar20 = pd.read_csv(Path("JC-202003-citibike-tripdata.csv"))
df_Jul20 = pd.read_csv(Path("JC-202007-citibike-tripdata.csv"))
df_Jul20.info()


# In[9]:


# Concatenate DataFrames of the earlier years
df_earlierYears = pd.concat([df_Jul13, df_Mar14, df_Mar20, df_Jul20], axis=0)
df_earlierYears.tail(2)


# In[10]:


# Read the csv files for Mar 2023 into pandas DataFrames and merge into one
df_Mar23_1 = pd.read_csv(Path("202303-citibike-tripdata_1.csv"),low_memory=False)
df_Mar23_2 = pd.read_csv(Path("202303-citibike-tripdata_2.csv"),low_memory=False)
df_Mar23_3 = pd.read_csv(Path("202303-citibike-tripdata_3.csv"),low_memory=False)
df_Mar23 = pd.concat([df_Mar23_1, df_Mar23_2, df_Mar23_3], axis=0)
df_Mar23 = df_Mar23.dropna(how='any')
df_Mar23.info()


# In[11]:


# Read the csv files for July 2023 into pandas DataFrames and merge into one
df_Jul23_1 = pd.read_csv(Path("202307-citibike-tripdata_1.csv"), low_memory=False)
df_Jul23_2 = pd.read_csv(Path("202307-citibike-tripdata_2.csv"), low_memory=False)
df_Jul23_3 = pd.read_csv(Path("202307-citibike-tripdata_3.csv"),low_memory=False)
df_Jul23_4 = pd.read_csv(Path("202307-citibike-tripdata_4.csv"),low_memory=False)

df_Jul23 = pd.concat([df_Jul23_1, df_Jul23_2, df_Jul23_3, df_Jul23_4], axis=0)
df_Jul23 = df_Jul23.dropna(how='any')
df_Jul23.info()


# In[13]:


# Read the csv files selected into pandas DataFrames
df_Mar24 = pd.read_csv(Path("JC-202403-citibike-tripdata.csv"))
df_Mar24 = df_Mar24.dropna(how='any')
df_Mar24.info()


# In[15]:


# Concatenate DataFrames of 2023 and 2024
df_latestYears = pd.concat([df_Mar23, df_Jul23, df_Mar24], axis=0)
df_latestYears.tail(2)


# In[24]:


# Calculate the trip during for the dataFrame of latest years
df_latestYears['started_at'] = pd.to_datetime(df_latestYears['started_at'])
df_latestYears['ended_at'] = pd.to_datetime(df_latestYears['ended_at'])
df_latestYears['tripduration'] = (df_latestYears['ended_at']-df_latestYears['started_at']).dt.total_seconds()
df_latestYears.info()


# In[25]:


# change the datatypes of started_at, ended_at, and tripduration to match original datasets
df_latestYears = df_latestYears.astype({"tripduration": int}, errors='raise')
df_latestYears['started_at'] = pd.to_datetime(df_latestYears['started_at']).dt.strftime('%Y-%m-%d')
df_latestYears['ended_at'] = pd.to_datetime(df_latestYears['ended_at']).dt.strftime('%Y-%m-%d')

df_latestYears.info()


# In[28]:


# Rename the columns in the datasets from earlier years to match the latest dataset
Renamed_earlierYears_df = df_earlierYears.rename(columns={"starttime":"started_at",
    "stoptime":"ended_at",
    "start station name":"start_station_name",
     "start station id":"start_station_id",
    "end station name":"end_station_name",
     "end station id":"end_station_id",                                                     
    "start station latitude":"start_lat",
    "start station longitude":"start_lng",
    "end station latitude":"end_lat",
    "end station longitude":"end_lng",
    "bikeid":"ride_id", # not exactly the same 
    "usertype":"member_casual" # npt exactly the same
                               })
# Rearrange the columns in a similar order as the dataFrame of latest years
earlierYears_df = Renamed_earlierYears_df[["ride_id", "started_at", "ended_at","start_station_name",
                        "start_station_id", "end_station_name", "end_station_id",
                        "start_lat", "start_lng","end_lat", "end_lng", 
                         "member_casual", "tripduration"]]

earlierYears_df.head(2)  


# In[29]:


#replace the classifications in the member_casual column to match the later classifications
earlierYears_df['member_casual'] = earlierYears_df['member_casual'].replace({'Customer': 'casual', 
                                   'Subscriber': 'member'})


# In[32]:


earlierYears_df.head(2)


# In[35]:


# Concatenate DataFrames of all the selected years/months
df_cityBikeTrips = pd.concat([earlierYears_df, df_latestYears], axis=0)
df_cityBikeTrips.tail(2)


# In[36]:


df_cityBikeTrips.info()


# In[37]:


# export the dataFrames for earliest and latest years to csv files
df_cityBikeTrips.to_csv("citiBikeTrips.csv", index=False)
earlierYears_df.to_csv("citiBikeTripsEarlest.csv", index=False)
df_latestYears.to_csv("citiBikeTripsLatest.csv", index=False)

