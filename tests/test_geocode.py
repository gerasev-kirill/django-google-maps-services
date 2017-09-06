# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
import json, os
from dj_gmap.gmap.gmap import GMapClient
from dj_gmap.gmap.base import history as gmap_history


ERROR_MSGS = GMapClient.error_msgs
ERROR_MSGS.update(GMapClient.map_error_msgs)

class TestGmapHelper(TestCase):
    def setUp(self):
        self.G = GMapClient()

    def test_fail_decode(self):
        # invalid input type 'float'
        self.assertRaisesMessage(
            TypeError,
            ERROR_MSGS['geocode_invalid_type'].format(
                type=type(1.1)
            ),
            self.G.geocode,
            1.1
        )
        # invalid input type 'int' inside list
        self.assertRaisesMessage(
            TypeError,
            ERROR_MSGS['geocode_invalid_type'].format(
                type=type(1)
            ),
            self.G.geocode,
            [1, 'Paris']
        )

    def test_geocode(self):
        self.assertEqual(len(gmap_history), 0)
        # fetch single
        self.G.geocode('Amsterdam')
        self.assertEqual(len(gmap_history), 1)


        # fetch from cache
        self.G.geocode('Amsterdam')
        self.assertEqual(len(gmap_history), 1)


        # ignore cache
        self.G.geocode('Amsterdam', ignore_cache=True)
        self.assertEqual(len(gmap_history), 2)
        self.assertEqual(
            gmap_history[1].action,
            'geocode'
        )
        self.assertEqual(
            gmap_history[1].args,
            ('Amsterdam',)
        )


        # fetch multiple locations
        res = self.G.geocode(['Paris', 'Amsterdam'])
        self.assertEqual(len(gmap_history), 3)
        # only 'Paris', 'Amsterdam' we have in cache
        self.assertEqual(
            gmap_history[2].action,
            'geocode'
        )
        self.assertEqual(
            gmap_history[2].args,
            ('Paris',)
        )
        # paris coordinates
        self.assertEqual(
            res[0][0]['geometry']['location']['lat'],
            48.856614
        )
        self.assertEqual(
            res[0][0]['geometry']['location']['lng'],
            2.3522219
        )

        # amsterdam coordinates
        self.assertEqual(
            res[1][0]['geometry']['location']['lat'],
            52.3702157
        )
        self.assertEqual(
            res[1][0]['geometry']['location']['lng'],
            4.895167900000001
        )

        # fetch multiple locations from cache
        res = self.G.geocode(['Paris', 'Amsterdam'])
        self.assertEqual(len(gmap_history), 3)
