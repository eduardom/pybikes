# -*- coding: utf-8 -*-
# Copyright (C) Eduardo Mucelli Rezende Oliveira <edumucelli@gmail.com>
# Distributed under the AGPL license, see LICENSE.txt

import json

from .base import BikeShareSystem, BikeShareStation
from . import utils, exceptions

__all__ = ['Velobike', 'VelobikeStation']

"""
Each station is formatted as:
{
    u 'code': u '036', 
    u 'is_deleted': 0,
    u 'name': u ' Hotel "Diplomat"  ',
    u 'photo': None,
    u 'is_sales': 0,
    u 'avl_bikes': 1,
    u 'free_slots': 7,
    u 'address': u '\u041d\u0430 
                    \u043f\u0435\u0440\u0435\u0441\u0435\u0447\u0435\u043d\u0438\u0438
                    \u0443\u043b.
                    \u0410\u043a\u043c\u0435\u0448\u0435\u0442\u044c,
                    \u0443\u043b.\u041a\u0443\u043d\u0430\u0435\u0432\u0430.',
    u 'lat': u '51.130769',
    u 'lng': u '71.429361',
    u 'total_slots': 8,
    u 'id': 41,
    u 'is_not_active': 0,
    u 'desc': u ''
}

"""

class Velobike(BikeShareSystem):

    sync = True

    meta = {
        'system': 'Velobike',
        'company': ['Agency for Physical Culture and Sports of \
                    the Republic of Kazakhstan', 
                    'Sovereign Wealth Fund "Samruk-Kazyna" JSC',
                    'Akimat of Astana', 'Smoove']
    }

    def __init__(self, tag, feed_url, meta):
        super(Velobike, self).__init__(tag, meta)
        self.feed_url = feed_url

    def update(self, scraper = None):
        if scraper is None:
            scraper = utils.PyBikesScraper()

        data = json.loads(scraper.request(self.feed_url))
        
        stations = []
        for station in data['data']:
            """ 
            Discard stations as VeloBike's 'Sales Department', which
            does not have information about available bikes:
            {
                "id":48,"code":"sales1","name":"Sales Department",
                "lat":"51.145528","lng":"71.413569","photo":null,
                "desc":"","total_slots":null,"free_slots":null,
                "address":"Astana city, Mega mart 2nd floor, 
                                        Qurghalzhyn Highway 1",
                "avl_bikes":null,"is_deleted":0,"is_sales":1,"is_not_active":0
            }"""
            try:
                bikes = int(station['avl_bikes'])
            except TypeError:
                continue
            name = station['name']
            latitude = float(station['lat'])
            longitude = float(station['lng'])
            free = int(station['free_slots'])
            extra = {
                'slots': int(station['total_slots']),
                'address': station['address'],
                'closed': bool(station['is_not_active'])
            }
            station = VelobikeStation(name, latitude, longitude,
                                      bikes, free, extra)
            stations.append(station)
        self.stations = stations

class VelobikeStation(BikeShareStation):
    def __init__(self, name, latitude, longitude, bikes, free, extra):
        super(VelobikeStation, self).__init__()

        self.name      = name
        self.latitude  = latitude
        self.longitude = longitude
        self.bikes     = bikes
        self.free      = free
        self.extra     = extra