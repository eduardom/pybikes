# -*- coding: utf-8 -*-
# Copyright (C) Eduardo Mucelli Rezende Oliveira <edumucelli@gmail.com>
# Distributed under the AGPL license, see LICENSE.txt

import json
import re

from .base import BikeShareSystem, BikeShareStation
from . import utils, exceptions

__all__ = ['Changzhou', 'ChangzhouStation']

class Changzhou(BikeShareSystem):

    sync = True

    meta = {
        'system': 'Changzhou',
        'company': 'Changzhou Wing Public Bicycle Systems Co., Ltd.'
    }

    def __init__(self, tag, feed_url, meta):
        super(Changzhou, self).__init__(tag, meta)
        self.feed_url = feed_url

    def update(self, scraper = None):
        if scraper is None:
            scraper = utils.PyBikesScraper()
        
        html = scraper.request(self.feed_url)
        # There is one station in one of the cities in which the
        # address has a double quote mark in the middle of the string.
        # This makes the JSON invalid, SHIT!
        # {
        #     "id": 75,
        #     "name": "益华百货",
        #     "lat": 22.510574,
        #     "lng": 113.385837,
        #     "capacity": 20,
        #     "availBike": 0,       |-------| => These damn things here!
        #     "address": "中山市银通街"中银大厦"公交站南侧"
        # }
        html = re.sub(r'("address"\s*\:\s*".*?").*?(\})', r'\1\2', html)
        data = json.loads(html.replace('var ibike = ',''))
        # print data
        stations = []

        for station in data['station']:
            latitude = float(station['lat'])
            longitude = float(station['lng'])
            # Some stations have '0' for latitude and longitude 
            if latitude and longitude:
                name = station['name']
                bikes = int(station['availBike'])
                capacity = int(station['capacity'])
                # Site's code uses the same subtraction to infer 'free' bike stands
                free = capacity - bikes
                extra = {
                    'slots': capacity
                }
                station = ChangzhouStation(name, latitude, longitude,
                                                    bikes, free, extra)
                stations.append(station)
        self.stations = stations

class ChangzhouStation(BikeShareStation):
    def __init__(self, name, latitude, longitude, bikes, free, extra):
        super(ChangzhouStation, self).__init__()

        self.name      = name
        self.latitude  = latitude
        self.longitude = longitude
        self.bikes     = bikes
        self.free      = free
        self.extra     = extra