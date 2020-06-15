#!/usr/bin/env python
# coding: utf-8

# In[1]:


# get_ipython().run_line_magic('matplotlib', 'inline')
# get_ipython().system('pip install -U tables')
import pandas as pd
import time
import numpy as np
import sklearn
from sklearn import linear_model
import json
import matplotlib.pyplot as plt
import os
from tqdm.notebook import tqdm
import mxnet as mx
import pandarallel
from mxboard import *


# In[2]:


#from google.colab import drive
#drive.mount('/content/gdrive')
seed = 42
dataset_root = os.path.expanduser('~/TaxiData')


# In[3]:


#num_samples = 1000000
#train_indices, test_indices = sklearn.model_selection.train_test_split(np.arange(num_samples))

def get_dataset():
    dataset = pd.read_hdf(os.path.join(dataset_root, 'data.h5'))
    train, test = sklearn.model_selection.train_test_split(dataset, random_state=seed)
    train = train.copy()
    test=  test.copy()
    return train, test


# In[4]:


train, test = get_dataset()


# In[5]:


use_numerical_cat = False


# In[6]:


category_features = {
    'VendorID':(2, 2),
    'PULocationID': (265, 30),
    'DOLocationID': (265, 30),
    'payment_type': (5, 2),
    'week': (53, 10),
    'dayofweek': (7, 3),
    'quarterofday': (96, 20)
}
exclude = ['tpep_pickup_datetime', 'tpep_dropoff_datetime'] + list(category_features.keys()) + ['snow', 'rain', 'PULocationIDX','PULocationIDY','DOLocationIDX','DOLocationIDY', 'isHoliday', 'pickup_loc_count', 'dropoff_loc_count']
exclude_minus = []
exclude = [c for c in exclude if c not in exclude_minus]
columns = [c for c in train.columns if c not in exclude]
columns += list(category_features.keys())
print(columns)


# In[7]:


train_pickup_counts = {i: 0 for i in range(1, 266)}
train_dropoff_counts = {i: 0 for i in range(1, 266)}
train_pickup_counts.update(train['PULocationID'].value_counts().to_dict())
train_dropoff_counts.update(train['DOLocationID'].value_counts().to_dict())

def get_pickup_dropoff_count(pu_map, do_map):
    def func(x):
      return pu_map[x['PULocationID']], do_map[x['DOLocationID']]
    return func


# In[8]:


def get_date(df):
    df['week'] = df['tpep_pickup_datetime'].dt.weekofyear
    df['dayofweek'] = df['tpep_pickup_datetime'].dt.dayofweek
    df['quarterofday'] = df['tpep_pickup_datetime'].dt.hour * 4 + df['tpep_pickup_datetime'].dt.quarter
    df['duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds()
    df.drop(columns=['tpep_dropoff_datetime', 'tpep_pickup_datetime'], inplace=True)


# In[9]:


def haversine_array(lat1, lng1, lat2, lng2):
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    AVG_EARTH_RADIUS = 6371  # in km
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * np.arcsin(np.sqrt(d))
    return h

def dummy_manhattan_distance(lat1, lng1, lat2, lng2):
    a = haversine_array(lat1, lng1, lat1, lng2)
    b = haversine_array(lat1, lng1, lat2, lng1)
    return a + b

def bearing_array(lat1, lng1, lat2, lng2):
    AVG_EARTH_RADIUS = 6371  # in km
    lng_delta_rad = np.radians(lng2 - lng1)
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    y = np.sin(lng_delta_rad) * np.cos(lat2)
    x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(lng_delta_rad)
    return np.degrees(np.arctan2(y, x))


# In[ ]:





# In[10]:


def preprocess(df, drop_outlier):
    get_date(df)
    #df['direction'] = bearing_array(df['PULocationX'].values, df['PULocationY'].values, df['DOLocationX'].values, df['DOLocationY'].values)
    #df['distance_haversine'] = haversine_array(df['PULocationX'].values, df['PULocationY'].values, df['DOLocationX'].values, df['DOLocationY'].values)
    #df['distance_dummy_manhattan'] = dummy_manhattan_distance(df['PULocationX'].values, df['PULocationY'].values, df['DOLocationX'].values, df['DOLocationY'].values)
    if drop_outlier:
        df.drop(df.loc[df['duration'] > 8*3600].index, inplace=True) # drop > 8 hours
    #df['pickup_loc_count'], df['dropoff_loc_count'] = zip(*df.parallel_apply(get_pickup_dropoff_count(train_pickup_counts, train_dropoff_counts), axis=1))
    dtype = 'float32'
    duration = df['duration'].to_numpy(dtype=dtype)
    # cats = [df[category_feature].to_numpy(dtype=dtype) for category_feature in category_features.keys()]
    conds = df[columns].to_numpy(dtype=dtype)
    return conds, duration


# In[11]:


train_data, train_labels = preprocess(train, True)
test_data, test_labels = preprocess(test, True)

del train
del test

import sklearn.datasets
sklearn.datasets.dump_svmlight_file(train_data, train_labels, './original_coord_dist/train.txt')
sklearn.datasets.dump_svmlight_file(test_data, test_labels, './original_coord_dist/test.txt')


