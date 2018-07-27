# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
import json, os
from dj_gmap.gmap.gmap import GMapClient
from dj_gmap.gmap.base import history as gmap_history
from dj_gmap import exceptions

ERROR_MSGS = GMapClient.error_msgs
ERROR_MSGS.update(GMapClient.map_error_msgs)




class TestGmapHelper(TestCase):
    def setUp(self):
        self.G = GMapClient()

    def test_geocode_country_only_fail(self):
        places = ["EMPTY GEOCODE RESULT"]
        # empty result
        self.assertRaisesMessage(
            exceptions.EmptyGeocodeResult,
            ERROR_MSGS['empty_geocode_result'].format(
                search_string=places[0]
            ),
            self.G.geocode_country_only,
            places
        )


    def test_geocode_contry_only(self):
        # fetch single
        places_in_amsterdam = ['NEMO Science Museum', 'Fjällräven Flagship Store Amsterdam']

        for place in places_in_amsterdam:
            country_info = self.G.geocode_country_only(place + ', ' + 'Amsterdam')
            self.assertDictEqual(
                country_info,
                {u'long_name': u'Netherlands', u'short_name': u'NL'}
            )

        history_len_last = len(gmap_history)
        # run geocode again.
        # this time no googlemaps call will be done
        self.G.geocode_city_only(places_in_amsterdam[0] + ', ' + 'Amsterdam')
        self.assertEqual(len(gmap_history), history_len_last)

        country_info = self.G.geocode_country_only(u'Одесса, Потемкинская лестница')
        self.assertDictEqual(
            country_info,
            {u'long_name': u'Ukraine', u'short_name': u'UA'}
        )
        self.assertEqual(len(gmap_history), history_len_last+2)
