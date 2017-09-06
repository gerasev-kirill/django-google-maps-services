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

    def test_geocode_city_only_fail(self):
        places = ["EMPTY GEOCODE RESULT"]
        # empty result
        self.assertRaisesMessage(
            exceptions.EmptyGeocodeResult,
            ERROR_MSGS['empty_geocode_result'].format(
                search_string=places[0]
            ),
            self.G.geocode_city_only,
            places
        )


    def test_geocode_city_only(self):
        # fetch single
        amsterdam = self.G.geocode('Amsterdam')[0]['geometry']['location']
        places_in_amsterdam = ['NEMO Science Museum', 'Fjällräven Flagship Store Amsterdam']

        for place in places_in_amsterdam:
            place_coordinates = self.G.geocode(place)[0]['geometry']['location']
            city_coordinates = self.G.geocode_city_only(place)[0]['geometry']['location']

            # place in city 'amsterdam'
            self.assertDictEqual(
                city_coordinates,
                amsterdam
            )
            # coordinates is not real place coordinates but city
            self.assertNotEqual(
                city_coordinates['lat'],
                place_coordinates['lat']
            )
            self.assertNotEqual(
                city_coordinates['lng'],
                place_coordinates['lng']
            )

        history_len_last = len(gmap_history)
        # run geocode again.
        # this time no googlemaps call will be done
        self.G.geocode_city_only(places_in_amsterdam[0])
        self.assertEqual(len(gmap_history), history_len_last)
