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
