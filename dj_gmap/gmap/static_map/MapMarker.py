# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import six
from unidecode import unidecode
import json, re
import googlemaps
import urllib



class MapMarker(object):
    latLng = None
    label = None
    color = None
    icon = None
    size = None
    error_msgs = {
        'invalid_label_type': "Invalid type for label '{label}'. Expect <type 'str'> or <type 'unicode'> or <type 'int'>. Got - {type}",
        'invalid_marker_size': "Invalid marker size '{size}'. Allowed are 'tiny', 'mid', 'small'",
        'invalid_marker_icon_type': "Invalid type for icon '{icon}'. Expect <type 'str'> or <type 'unicode'>. Got - {type}"
    }

    def __init__(self, point, label=None, size=None, color=None, icon=None):
        if size not in [None, 'tiny', 'mid', 'small']:
            raise ValueError(
                self.error_msgs['invalid_marker_size'].format(size=size)
            )

        if icon:
            if not isinstance(icon, six.text_type) and not isinstance(icon, six.string_types):
                raise TypeError(
                    self.error_msgs['invalid_marker_icon_type'].format(
                        icon=icon, type=type(icon)
                    )
                )
            self.icon = urllib.quote(icon)
        if label != None:
            self.label = self._normalize_marker_label(label)
        self.size = size
        self.color = color or 'red'
        self.latLng = googlemaps.convert.latlng(point)



    def _normalize_marker_label(self, label):
        if isinstance(label, int):
            label = unicode(label)
        if not isinstance(label, six.text_type) and not isinstance(label, six.string_types):
            raise TypeError(
                self.error_msgs['invalid_label_type'].format(
                    label=label,
                    type=type(label)
                )
            )
        if not label:
            return label
        # гугль карта будет игнорировать любые символы для маркера
        # кроме англ и цифр
        label = unidecode(label[:5])
        label = label[0].upper()
        if not label.isalnum():
            return None
        return label



    def to_url_component(self):
        params = []
        for prop in ['color', 'size', 'label', 'icon']:
            value = getattr(self, prop, None)
            if value != None:
                params.append(prop+":"+value)
        params.append(self.latLng)
        return "markers=" + "|".join(params)
