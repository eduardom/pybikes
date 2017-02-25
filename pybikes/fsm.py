# -*- coding: utf-8 -*-
# Copyright (C) Eduardo Mucelli Rezende Oliveira <edumucelli@gmail.com>
# Distributed under the AGPL license, see LICENSE.txt

import re

from .base import BikeShareSystem, BikeShareStation
from . import utils, exceptions

__all__ = ['FSM', 'FSMStation']

STATIONS_RGX = "setMarker\((.*?), '<a href\="

# A station looks like big monsters with lots of HTML, which was discarded
    # setMarker(34.809,
    #           32.07,
    #           611,
    #           'וייצמן 57',
    #           'וייצמן 57 -  גבעתיים',
    #           '20',
    #           '20',
    #           '<a href="..." ...
    # lon, lat, id, name, address, poles, available, nearStationsDiv, isActive

class FSM(BikeShareSystem):

    sync = True

    meta = {
        'system': 'FSM',
        'company': 'FSM'
    }

    def __init__(self, tag, meta, feed_url):
        super(FSM, self).__init__(tag, meta)
        self.feed_url = feed_url

    def update(self, scraper = None):
        if scraper is None:
            scraper = utils.PyBikesScraper()
            
        stations = []

        html = scraper.request(self.feed_url)
        data = re.findall(STATIONS_RGX, html)
        for info in data:
            fields = info.replace('\'','').split(',')
            latitude = float(fields[0])
            longitude = float(fields[1])
            name = fields[3]
            address = fields[4]
            slots = int(fields[5])
            free = int(fields[6])
            bikes = slots - free
            extra = {'slots': slots,
                     'address': address}
            station = FSMStation(name, latitude, longitude, bikes, free, extra)
            stations.append(station)
        self.stations = stations

class FSMStation(BikeShareStation):
    def __init__(self, name, latitude, longitude, bikes, free, extra):
        super(FSMStation, self).__init__()
        self.name       = name
        self.latitude   = latitude
        self.longitude  = longitude
        self.bikes      = bikes
        self.free       = free
        self.extra      = extra