from django.db import models
from jsonfield import JSONField


DJANGO_GC_MAP_POINT_PRECISION = 7



class GMapPointCache(models.Model):
    id = models.CharField(max_length=300, primary_key=True)
    lat = models.DecimalField(
        max_digits=2+DJANGO_GC_MAP_POINT_PRECISION,
        decimal_places=DJANGO_GC_MAP_POINT_PRECISION
    )
    lng = models.DecimalField(
        max_digits=2+DJANGO_GC_MAP_POINT_PRECISION,
        decimal_places=DJANGO_GC_MAP_POINT_PRECISION
    )
    data = JSONField(default=[])
