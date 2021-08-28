#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 23:32:47 2021

@author: diego
"""

from json.decoder import JSONDecodeError
import numpy as np
import pandas as pd
import requests
import json
import time

def find_stations(lat,long):
    
    '''
    
    Providing coordinates (latitude and longitude) it will request to Overpass Turbo
    API for a list of the tube stations within an square area of 2km per side.
    
    '''
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    (node["railway"="stop"][subway=yes](around:3000,""" + str((lat)) + "," +\
    str((long)) + """);
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    data = response.json()
    
    stations = list()
    time.sleep(20)
    
    if not data['elements']:
        return stations
    else:
        for element in data['elements']:
            station = list()
            station.append(element['tags']['name'])
            station.append(element['lat'])
            station.append(element['lon'])
            stations.append(station)
#        stations = list(set(stations))
        return stations

def closest_station(lat, long, data_stations_temp, index):
    url_base = 'https://api.mapbox.com/directions/v5/mapbox/walking/'
    token = 'pk.eyJ1IjoiZGllcXVpZXMiLCJhIjoiY2tyOGRwZzVuMndhajJvbW53bDJoNGVhZSJ9.YxoxeYN6lUM4IJ4cEjZQnw'
    data_stations_temp['lat_dif'] = data_stations_temp['latitude'] - lat
    data_stations_temp['long_dif'] = data_stations_temp['longitude'] - long
    data_stations_temp['sqrt'] = ((data_stations_temp['lat_dif']**2) + (data_stations_temp['long_dif']**2))**0.5
    data_stations_temp.sort_values('sqrt', inplace = True)
    data_stations_temp.reset_index(drop = True, inplace = True)
    data_stations_temp.drop(['lat_dif','long_dif','sqrt'], axis = 1)
    duration = list()
    for i in range(0,2):
        url = url_base + str(long) + ',' + str(lat) + ';' + str(data_stations_temp.iloc[i]['longitude']) + ',' +\
        str(data_stations_temp.iloc[i]['latitude']) + '?geometries=geojson&access_token=' + token
        response = requests.get(url)
        data = response.json()
        duration.append(data['routes'][0]['legs'][0]['duration'])
    idx_max = np.argmax(duration) - 1
    closest_station = [data_stations_temp.iloc[idx_max]['name']]
    closest_station.append(duration[idx_max])
    time.sleep(1)
    print(index)
    return closest_station

def pub_restaurant_count(latitude,longitude):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """[out:json];
    (
    node[amenity=pub](around:500,""" + str(latitude) + "," + str(longitude) + """);
    node[amenity=restaurant](around:500,""" + str(latitude) + "," + str(longitude) + """);
    );
    out count;"""
    try:
        response = requests.get(overpass_url, 
                                params={'data': overpass_query})
        data = response.json()
    except JSONDecodeError:
        time.sleep(5)
        response = requests.get(overpass_url, 
                                params={'data': overpass_query})
        data = response.json()
    count = data['elements'][0]['tags']['nodes']
    return int(count)