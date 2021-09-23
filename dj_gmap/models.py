# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import json
from .fields import JSONField

DJANGO_GC_MAP_POINT_PRECISION = 7



class GMapPointCache(models.Model):
    id = models.CharField(max_length=300, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    lat = models.DecimalField(
        max_digits=2+DJANGO_GC_MAP_POINT_PRECISION,
        decimal_places=DJANGO_GC_MAP_POINT_PRECISION
    )
    lng = models.DecimalField(
        max_digits=2+DJANGO_GC_MAP_POINT_PRECISION,
        decimal_places=DJANGO_GC_MAP_POINT_PRECISION
    )
    data = JSONField(default=[])

    def get_data(self):
        if not isinstance(self.data, (dict, list)):
            self.data = json.loads(self.data)
            self.save(update_fields=['data'])
        return self.data



class GMapDirectionCache(models.Model):
    id = models.CharField(
        max_length=(4+2+DJANGO_GC_MAP_POINT_PRECISION)*30+2+10,
        primary_key=True
    )
    created = models.DateTimeField(auto_now_add=True)
    data = JSONField(default=[])

    def get_data(self):
        if not isinstance(self.data, (dict, list)):
            self.data = json.loads(self.data)
            self.save(update_fields=['data'])
        return self.data
