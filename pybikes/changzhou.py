# -*- coding: utf-8 -*-
# Copyright (C) Eduardo Mucelli Rezende Oliveira <edumucelli@gmail.com>
# Distributed under the AGPL license, see LICENSE.txt

import json

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
        data = json.loads(html.replace('var ibike = ',''))

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