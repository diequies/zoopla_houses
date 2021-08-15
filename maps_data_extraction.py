#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 23:32:47 2021

@author: diego
"""

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