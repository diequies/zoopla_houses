#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 21:38:38 2021

@author: diego
"""
import requests
from bs4 import BeautifulSoup as soup
import numpy as np
import pandas as pd
import math
import json
import time

def number_of_search_pages(url):
    
    """
    Function to get the number of pages and houses of an specific borough.
    
    It requires as input the url to the first page of the search.
    
    """
    
    page = requests.get(url)
    if page.status_code != 200:
        print('Url provided not valid')
    else:
        bsobj = soup(page.content, 'html5lib')
        pages_html = bsobj.find('p',{'data-testid':'total-results'})
        pages = pages_html.get_text().split()
        house_num = int(pages[0])
        pages = math.ceil(int(pages[0])/25)
        return pd.Series((pages, house_num))
    

def get_borough_url(link1,link2):
    
    """
    Function to build the url for the search of each borough
    
    The inputs are both items that defines the search location. It is specific of each borough.
    
    """
    
    url = 'https://www.zoopla.co.uk/for-sale/property/' + link1 + '/?page_size=25&q='\
    + link2 + '&radius=0&results_sort=newest_listings&pn=1'
    return url


def get_main_house_details(url_initial, pages, house_num):
    
    """
    Function to scrape links and other details from main search page of each house.
    
    It requires to provide the url without the search page number, the amount of pages
    and the amount of houses.
    
    """
    
    url_initial = url_initial[:-1]
    link = []
    listed = []
    for i in range(1,pages+1):
        url = url_initial + str(i)
        page = requests.get(url)
        bsobj = soup(page.content, 'html5lib')
        for j in bsobj.findAll('a',{'data-testid':'listing-details-link'}, href=True):
            link.append(j.get('href'))
        for j in bsobj.findAll('span',{'data-testid':'date-published'}):
            listed.append(j.text)
        print('Request {0} of {1}'.format(i,pages))
        time.sleep(1)
    return link, listed

def get_house_inner_details(link,listed,borough):
    
    """
    The function takes json code from each house page, parses it and takes the 
    information.
    
    The inputs are a set of series for the link, when was listed and the borough. 
    The link to access the information and the other two series to join with the
    rest of the information.
    
    The output is a dataframe with the information for each element of the initial
    series.
    
    It requires a try and except approach to avoid errors from empty and None 
    features.
    
    """
    
    borough = []
    agency_name = []
    agency_phone = []
    chain_free = []
    address = []
    isRetirementHome = []
    isSharedOwnership = []
    listingCondition = []
    listingStatus = []
    RoomCount = []
    price = []
    propertyType = []
    floorArea = []
    tenure = []
    detailedDescription = []
    features = []
    furnishedState = []
    title = []
    latitude = []
    longitude = []
    statusSummary = []
    isAuction = []
    priceHistory = []
    columns = ['agency_name','agency_phone','chain_free','address','isRetirementHome','isSharedOwnership',
              'listingCondition','listingStatus','RoomCount','price','propertyType','isAuction','priceHistory',
              'floorArea','tenure','detailedDescription','features','furnishedState','title','latitude',
              'longitude','statusSummary']
    for index, value in enumerate(link):
        url = 'https://www.zoopla.co.uk' + value
        page = requests.get(url)
        bsobj = soup(page.content, 'html5lib')
        main_json = bsobj.find('script',{'id':'__NEXT_DATA__'})
        parsed_json = json.loads(main_json.text)
        borough.append(borough)
        try:
            agency_name.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                           ['branch']['name'])
        except TypeError:
            agency_name.append(np.nan)
        except KeyError:
            agency_name.append(np.nan)
        try:
            agency_phone.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                            ['branch']['phone'])
        except TypeError:
            agency_phone.append(np.nan)
        except KeyError:
            agency_phone.append(np.nan)
        try:
            chain_free.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                          ['adTargeting']['chainFree'])
        except TypeError:
            chain_free.append(np.nan)
        except KeyError:
            chain_free.append(np.nan)
        try:
            address.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                       ['adTargeting']['displayAddress'])
        except TypeError:
            address.append(np.nan)
        except KeyError:
            address.append(np.nan)
        try:
            isRetirementHome.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                                ['adTargeting']['isRetirementHome'])
        except TypeError:
            isRetirementHome.append(np.nan)
        except KeyError:
            isRetirementHome.append(np.nan)
        try:
            isSharedOwnership.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                                 ['adTargeting']['isSharedOwnership'])
        except TypeError:
            isSharedOwnership.append(np.nan)
        except KeyError:
            isSharedOwnership.append(np.nan)
        try:
            listingCondition.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                                ['adTargeting']['listingCondition'])
        except TypeError:
            listingCondition.append(np.nan)
        except KeyError:
            listingCondition.append(np.nan)
        try:
            listingStatus.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                             ['adTargeting']['listingStatus'])
        except TypeError:
            listingStatus.append(np.nan)
        except KeyError:
            listingStatus.append(np.nan)
        try:
            RoomCount.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                        ['counts'])
        except TypeError:
            RoomCount.append(np.nan)
        except KeyError:
            RoomCount.append(np.nan)
        try:
            price.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                     ['adTargeting']['price'])
        except TypeError:
            price.append(np.nan)
        except KeyError:
            price.append(np.nan)
        try:
            propertyType.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                            ['adTargeting']['propertyType'])
        except TypeError:
            propertyType.append(np.nan)
        except KeyError:
            propertyType.append(np.nan)
        try:
            floorArea.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                          ['floorArea'])
        except TypeError:
            floorArea.append(np.nan)
        except KeyError:
            floorArea.append(np.nan)
        try:
            tenure.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                      ['adTargeting']['tenure'])
        except TypeError:
            tenure.append(np.nan)
        except KeyError:
            tenure.append(np.nan)
        try:
            detailedDescription.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                                   ['detailedDescription'])
        except TypeError:
            detailedDescription.append(np.nan)
        except KeyError:
            detailedDescription.append(np.nan)
        try:
            features.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                        ['features']['bullets'])
        except TypeError:
            features.append(np.nan)
        except KeyError:
            features.append(np.nan)
        try:
            furnishedState.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                              ['features']['flags']['furnishedState'])
        except TypeError:
            furnishedState.append(np.nan)
        except KeyError:
            furnishedState.append(np.nan)
        try:
            title.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                         ['title'])
        except TypeError:
            title.append(np.nan)
        except KeyError:
            title.append(np.nan)
        try:
            latitude.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                        ['location']['coordinates']['latitude'])
        except TypeError:
            latitude.append(np.nan)
        except KeyError:
            latitude.append(np.nan)
        try:
            longitude.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                         ['location']['coordinates']['longitude'])
        except TypeError:
            longitude.append(np.nan)
        except KeyError:
            longitude.append(np.nan)
        try:
            statusSummary.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                             ['statusSummary']['label'])
        except TypeError:
            statusSummary.append(np.nan)
        except KeyError:
            statusSummary.append(np.nan)
        try:
            isAuction.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                         ['pricing']['isAuction'])
        except TypeError:
            isAuction.append(np.nan)
        except KeyError:
            isAuction.append(np.nan)
        try:
            priceHistory.append(parsed_json['props']['initialProps']['pageProps']['data']['listing']\
                            ['priceHistory'])
        except TypeError:
            priceHistory.append(np.nan)
        except KeyError:
            priceHistory.append(np.nan)
        print('Request {0} of {1}'.format(index,len(link)-1))
        time.sleep(1)
    df_result = pd.DataFrame({'agency_name':agency_name,'agency_phone':agency_phone,
                              'chain_free':chain_free,'address':address,'isRetirementHome':isRetirementHome,
                              'isSharedOwnership':isSharedOwnership,'listingCondition':listingCondition,
                              'listingStatus':listingStatus,'RoomCount':RoomCount,'price':price,
                              'propertyType':propertyType,'isAuction':isAuction,'priceHistory':priceHistory,
                              'floorArea':floorArea,'tenure':tenure,'detailedDescription':detailedDescription,
                              'features':features,'furnishedState':furnishedState,'title':title,
                              'latitude':latitude,'longitude':longitude,'statusSummary':statusSummary},
                            columns = columns)
    return df_result

def data_wrangle(data):
    
    """
    Function to modify the raw features to a final set of usable features to
    input into the SQL database.
    
    """
    
    data['floorArea'].fillna(value = np.nan, inplace = True)
    data['floor_area_amount'] = data['floorArea'].apply(lambda x: x['value'] if type(x) == dict else np.nan)
    data['floor_area_units'] = data['floorArea'].apply(lambda x: x['unitsLabel'] if type(x) == dict else np.nan)
    data['floor_area_msq'] = data.apply(lambda x: (round(x['floor_area_amount']/10.7639))\
                                        if (x['floor_area_units'] == 'sq. ft') else x['floor_area_amount'],
                                        axis = 1)
    data['numBedrooms'] = data['RoomCount'].apply(lambda x: 0\
                                                  if pd.isnull(x['numBedrooms']) else x['numBedrooms'])
    data['numBathrooms'] = data['RoomCount'].apply(lambda x: 0\
                                                  if pd.isnull(x['numBathrooms']) else x['numBathrooms'])
    data['numLivingRooms'] = data['RoomCount'].apply(lambda x: 0\
                                                  if pd.isnull(x['numLivingRooms']) else x['numLivingRooms'])
    data['firstPublished'] = data['priceHistory'].apply(lambda x: None if pd.isnull(x) else x['firstPublished'])
    data['lastSale'] = data['priceHistory'].apply(lambda x: None if pd.isnull(x) else x['lastSale'])
    data['firstPublishedDate'] = data['firstPublished'].apply(lambda x: None if pd.isnull(x)\
                                                              else x['firstPublishedDate'])
    data['firstPublishedPrice'] = data['firstPublished'].apply(lambda x: None if pd.isnull(x)\
                                                              else x['priceLabel'])
    data['lastSaleDate'] = data['lastSale'].apply(lambda x: None if pd.isnull(x) else x['date'])
    data['lastSaleNewBuild'] = data['lastSale'].apply(lambda x: None if pd.isnull(x) else x['newBuild'])
    data['lastSalePrice'] = data['lastSale'].apply(lambda x: None if pd.isnull(x) else x['price'])
    data['firstPublishedPrice'] = data['firstPublishedPrice'].apply(lambda x:None if pd.isnull(x)\
                                                                    else int(x.replace(',','').split('£')[-1]))
    return data