# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.conf import settings
import json, os
from dj_gmap.gmap.gmap import GMapClient
from dj_gmap.gmap.base import history as gmap_history
from dj_gmap import exceptions
import googlemaps

ERROR_MSGS = GMapClient.error_msgs
ERROR_MSGS.update(GMapClient.map_error_msgs)




class TestGmapHelper(TestCase):
    def setUp(self):
        self.G = GMapClient()
        self.client = googlemaps.Client(key=settings.DJANGO_GC_MAP_API_KEY)



    def test_directions(self):
        self.assertEqual(len(gmap_history), 0)
        res = self.G.directions('Paris', 'Amsterdam', mode='driving')
        self.assertEqual(len(gmap_history), 1)
        self.assertEqual(
            res,
            self.client.directions('Paris', 'Amsterdam', mode='driving')
        )
        # call again to fetch from cache
        res = self.G.directions('Paris', 'Amsterdam', mode='driving')
        self.assertEqual(len(gmap_history), 1)
        self.assertEqual(
            res,
            self.client.directions('Paris', 'Amsterdam', mode='driving')
        )


    def test_directions_statistics(self):
        res = self.G.directions(u'Киев', u'Берлин', mode='driving')
        stat = self.G.direction_statistics_by_country(res[0])
        #print json.dumps(stat)
        self.assertEqual(
            len(stat),
            3
        )
        self.assertEqual(
            stat[0]['short_name'],
            'UA' # ukraine
        )
        self.assertTrue(
            520000 > stat[0]['distance'] > 510000
        )
        self.assertEqual(
            stat[1]['short_name'],
            'PL' # poland
        )
        self.assertTrue(
            727000 > stat[1]['distance'] > 726000
        )
        self.assertEqual(
            stat[2]['short_name'],
            'DE' # germany
        )
        self.assertTrue(
            103000 > stat[2]['distance'] > 102000
        )
