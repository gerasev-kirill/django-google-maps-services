# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.conf import settings
import json, os
from dj_gmap.gmap.gmap_static import GMapStaticClient
from dj_gmap.gmap.base import history as gmap_history
from dj_gmap import exceptions

ERROR_MSGS = GMapStaticClient.error_msgs






class TestGmapStaticHelper(TestCase):
    def setUp(self):
        self.G = GMapStaticClient()


    def test_fail(self):
        self.assertRaisesMessage(
            TypeError,
            ERROR_MSGS['static_map_invalid_type'].format(
                type=type(1000)
            ),
            self.G.map_canvas_to_url,
            1000
        )

        map_canvas = self.G.new_map_canvas()
        self.assertRaisesMessage(
            ValueError,
            ERROR_MSGS['center_required'],
            self.G.map_canvas_to_url,
            map_canvas
        )



    def test_map_generator(self):
        places = [
            (u'Днепропетровск', u'Днепропетровск', "blue", u"maptype=roadmap&language=en&size=200x150&markers=color:blue|label:D|Днепропетровск"),
            (u'London', u'London', "red", u"maptype=roadmap&language=en&size=200x150&markers=color:red|label:L|London"),
            (u'Paris', None, "yellow", u"maptype=roadmap&language=en&size=200x150&markers=color:yellow|Paris"),
            (u'Rome', 2, None, u"maptype=roadmap&language=en&size=200x150&markers=color:red|label:2|Rome"),
        ]
        # single markers
        for place in places:
            static_map_canvas = self.G.new_map_canvas()
            static_map_canvas.add_marker(place[0],label=place[1], color=place[2])
            url = self.G.map_canvas_to_url(static_map_canvas, width=200, height=150)
            self.assertEqual(
                url,
                self.G.GMAP_SERVER_URL + '?key='+settings.DJANGO_GC_MAP_API_KEY + '&' + place[-1]
            )


        # multiple markers
        static_map_canvas = self.G.new_map_canvas()
        for place in places:
            static_map_canvas.add_marker(place[0],label=place[1], color=place[2])
        url = self.G.map_canvas_to_url(static_map_canvas, width=600, height=450)
        params = u"maptype=roadmap&language=en&size=600x450&markers=color:blue|label:D|Днепропетровск&markers=color:red|label:L|London&markers=color:yellow|Paris&markers=color:red|label:2|Rome"
        self.assertEqual(
            url,
            self.G.GMAP_SERVER_URL + '?key='+settings.DJANGO_GC_MAP_API_KEY + '&' + params
        )

        # path with markers
        static_map_canvas.add_path([{'lat':60.04, 'lng':40.3}, 'Rome', 'London'], weight=1, color='blue')
        url = self.G.map_canvas_to_url(static_map_canvas, width=600, height=550)
        params = u"maptype=roadmap&language=en&size=600x550&markers=color:blue|label:D|Днепропетровск&markers=color:red|label:L|London&markers=color:yellow|Paris&markers=color:red|label:2|Rome&path=geodesic:false|weight:1|color:blue|60.04,40.3|Rome|London"
        self.assertEqual(
            url,
            self.G.GMAP_SERVER_URL + '?key='+settings.DJANGO_GC_MAP_API_KEY + '&' + params
        )
