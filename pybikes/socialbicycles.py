# -*- coding: utf-8 -*-
# Copyright (C) 2016, Eduardo Mucelli Rezende Oliveira <edumucelli@gmail.com>
# Distributed under the AGPL license, see LICENSE.txt

import json

from .base import BikeShareSystem, BikeShareStation
from . import utils


BASE_URL = 'http://map.socialbicycles.com/hubs?network_id={network_id}'

__all__ = ['SocialBicycles']


class SocialBicycles(BikeShareSystem):

    sync = True

    meta = {
        'system': 'SocialBicycles',
        'company': ['Social Bicycles Inc.']
    }

    def __init__(self, tag, network_id, meta):
        super(SocialBicycles, self).__init__(tag, meta)
        self.url = BASE_URL.format(network_id=network_id)

    def update(self, scraper=None):
        if scraper is None:
            scraper = utils.PyBikesScraper()

        stations = []

        #  {  
        #   "id":251,
        #   "name":"TPA - 19th St and E Palm Ave",
        #   "racks_amount":7,
        #   "description":"01 - Ybor ",
        #   "network_id":11,
        #   "has_kiosk":false,
        #   "public":false,
        #   "display_method":"auto",
        #   "collapse_bikes":true,
        #   "area_id":102,
        #   "address":"2200-2298 North 19th Street, Tampa",
        #   "distance":null,
        #   "current_bikes":2,
        #   "available_bikes":2,
        #   "free_racks":5,
        #   "sponsored":false,
        #   "sponsored_bikes":0,
        #   "polygon":{  
        #      "type":"Polygon",
        #      "coordinates":[  
        #         ...
        #      ]
        #   },
        #   "middle_point":{  
        #      "type":"Point",
        #      "coordinates":[  
        #         -82.438056400783,
        #         27.9627193250593
        #      ]
        #   }
        # }

        data = json.loads(scraper.request(self.url))
        for station in data:
            name = station['name']
            longitude = float(station['middle_point']['coordinates'][0])
            latitude = float(station['middle_point']['coordinates'][1])
            bikes = int(station['available_bikes'])
            free = int(station['free_racks'])

            extra = {
                'slots': int(station['racks_amount']),
                'address': station['address'],
                'description': station['description'],
                'has_kiosk': station['has_kiosk']
            }

            station = BikeShareStation(name, latitude, longitude, bikes, free,
                                       extra)
            stations.append(station)

        self.stations = stations
