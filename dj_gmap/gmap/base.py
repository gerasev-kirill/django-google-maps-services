# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six
import googlemaps, time, sys
from django.conf import settings
from decimal import Decimal
from ..models import DJANGO_GC_MAP_POINT_PRECISION



DECIMAL_FORMAT_STR = "%."+str(abs(DJANGO_GC_MAP_POINT_PRECISION))+"f"
IS_TESTING_MODE = sys.argv[1:2] == ['test']

if IS_TESTING_MODE:
    history = []
    class HistoryObject(object):
        def __init__(self, **kwargs):
            for k,v in kwargs.items():
                setattr(self, k, v)

def import_class(cl):
    cl = str(cl)
    if '.site-packages.' in cl:
        cl = cl.split('.site-packages.')[-1]
    # http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
    d = cl.rfind(".")
    classname = cl[d+1:len(cl)]
    m = __import__(cl[0:d], {}, {}, [classname])
    return getattr(m, classname)


class BaseGMap(object):
    gmap_attempts = 0
    error_msgs = {
        'no_key': "Provide api key in settings.py. Variable 'DJANGO_GC_MAP_API_KEY'"
    }

    def __init__(self, key=None, **kwargs):
        if not key:
            key = getattr(settings, 'DJANGO_GC_MAP_API_KEY', None)
        if '.' in key:
            fn = None
            try:
                fn = import_class(key)
            except ImportError:
                pass
            if callable(fn):
                key = fn()
        assert key, self.error_msgs['no_key']
        self.key = key
        self._init_gmap()

    def _init_gmap(self):
        self._gmap = googlemaps.Client(key=self.key)

    def _run_gmap_command(self, action, *args, **kwargs):
        func = getattr(self._gmap, action)
        try:
            res = func(*args, **kwargs)
            if IS_TESTING_MODE:
                history.append(HistoryObject(
                    action=action,
                    args=args,
                    kwargs=kwargs,
                    response=res
                ))
            self.gmap_attempts = 0
            return res
        except googlemaps.exceptions.TransportError as e:
            self.gmap_attempts += 1
            if self.gmap_attempts > 10:
                raise googlemaps.exceptions.TransportError(e)
            time.sleep(0.1)
            self._init_gmap()
            return self._run_gmap_command(action, *args, **kwargs)


    def _coordinate_to_decimal(self, value):
        if isinstance(value, six.text_type) or isinstance(value, six.string_types):
            value = float(value)
        value = value or 0
        value = DECIMAL_FORMAT_STR % value
        return Decimal(value)

    def _location_to_str(self, value):
        if not value:
            return ''
        if isinstance(value, six.string_types) or isinstance(value, six.text_type):
            return value
        return googlemaps.convert.latlng(value)
