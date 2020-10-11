# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six
from unidecode import unidecode
import googlemaps

from .static_map.MapMarker import MapMarker
from .static_map.MapPath import MapPath
from .base import BaseGMap






class GMapStaticCanvas(object):
    def __init__(self):
        self.markers = []
        self.paths = []

    def add_marker(self, point, label=None, size=None, color=None, icon=None):
        self.markers.append(
            MapMarker(point, label=label, size=size, color=color, icon=icon)
        )

    def add_path(self, points, weight=None, color=None, fillcolor=None, geodesic=False):
        self.paths.append(
            MapPath(points, weight=weight, color=color, fillcolor=fillcolor, geodesic=geodesic)
        )

    def to_url_params(self):
        params = []
        for m in self.markers:
            params.append(m.to_url_component())
        for p in self.paths:
            params.append(p.to_url_component())
        return '&'.join(params)





class GMapStaticClient(BaseGMap):
    GMAP_SERVER_URL = "https://maps.googleapis.com/maps/api/staticmap"
    error_msgs = {
        'format_invalid': "Invalid value for 'format' param. Got - '{value}'. Allowed are: 'png8', 'png', 'png32', 'gif', 'jpg', 'jpg-baseline'.",
        'maptype_invalid': "Invalid value for 'maptype' param. Got - '{value}'. Allowed are: 'roadmap', 'satellite', 'hybrid', 'terrain'.",
        'static_map_invalid_type': "map_canvas is not an instance of GMapStaticCanvas. Got - {type}",
        'center_required': "Static map doesn't have markers, so 'center' param is required for map_canvas_to_url function."
    }
    def __init__(self, maptype='roadmap', language='en', region=None, **kwargs):
        super(GMapStaticClient, self).__init__(**kwargs)
        _format = kwargs.get('format', None)
        if _format not in [None, 'png8', 'png', 'png32', 'gif', 'jpg', 'jpg-baseline']:
            raise ValueError(
                self.error_msgs['format_invalid'].format(value=_format)
            )
        if maptype not in ['roadmap', 'satellite', 'hybrid', 'terrain']:
            raise ValueError(
                self.error_msgs['maptype_invalid'].format(value=maptype)
            )
        self.maptype = maptype
        self.language = language
        self.region = region
        self.format = _format

    def _normalize_map_size(self, value):
        value = value or 640
        value = abs(int(value))
        if value > 2048:
            return 2048
        return value

    def new_map_canvas(self):
        return GMapStaticCanvas()

    def map_canvas_to_url(self, map_canvas, center=None, zoom='default', width=640, height=640):
        if not isinstance(map_canvas, GMapStaticCanvas):
            raise TypeError(
                self.error_msgs['static_map_invalid_type'].format(type=type(map_canvas))
            )
        if not map_canvas.markers and not center:
            raise ValueError(self.error_msgs['center_required'])

        params = [
            "key=" + self.key,
            "maptype=" + self.maptype,
            "language=" + self.language,
            "size={width}x{height}".format(width=width, height=height)
        ]
        if self.format:
            params.append("format=" + self.format)
        if self.region:
            params.append("region=" + self.region)
        if center:
            params.append("center=" + googlemaps.convert.latlng(center))
        if zoom != 'default':
            params.append("zoom={zoom}")

        params.append(map_canvas.to_url_params())

        return self.GMAP_SERVER_URL + '?' + '&'.join(params)
