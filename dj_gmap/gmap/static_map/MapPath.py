# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import six
from unidecode import unidecode
import json, re
import googlemaps


bool_to_str = lambda x: 'true' if x else 'false'



class MapPath(object):
    points = []
    weight = None
    color = None
    fillcolor = None
    geodesic = False
    error_msgs = {
        'invalid_points_type': "Invalid type for points. Expect <type 'list'> or <type 'tuple'>. Got - {type}"
    }
    def __init__(self, points, weight=None, color=None, fillcolor=None, geodesic=False):
        if not isinstance(points, (list, tuple)):
            raise TypeError(
                self.error_msgs['invalid_points_type'].format(type=type(points))
            )
        for p in points:
            self.points.append(googlemaps.convert.latlng(p))
        if weight:
            weight = abs(int(weight))
            if weight:
                self.weight = unicode(weight)
        self.color = color or 'red'



    def to_url_component(self):
        params = [
            "geodesic:" + bool_to_str(self.geodesic)
        ]

        for prop in ['weight', 'color', 'fillcolor']:
            value = getattr(self, prop, None)
            if value != None:
                params.append(prop+":"+value)
        for p in self.points:
            params.append(p)
        return "path=" + "|".join(params)
