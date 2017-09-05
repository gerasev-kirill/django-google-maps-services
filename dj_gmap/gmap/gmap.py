from django.utils import six
import json
from .base import BaseGMap
from ..models import GMapPointCache




class GMapClient(BaseGMap):
    map_error_msgs = {
        'geocode_invalid_type': "Invalid type for geocode function. Expected <type 'str'> or <type 'unicode'> or list/tuple of this types. Got - {type}"
    }

    def _geocode(self, single_point, ignore_cache=False):
        if not ignore_cache:
            try:
                point = GMapPointCache.objects.get(id=single_point)
                return point.data
            except GMapPointCache.DoesNotExist:
                pass

        decoded = self._run_gmap_command('geocode', single_point)
        if decoded and not ignore_cache:
            GMapPointCache.objects.create(
                id=single_point,
                data=decoded,
                lat=self._coordinate_to_decimal(
                    decoded[0]['geometry']['location']['lat']
                ),
                lng=self._coordinate_to_decimal(
                    decoded[0]['geometry']['location']['lng']
                )
            )
        return decoded



    def geocode(self, points, ignore_cache=False):
        if isinstance(points, six.text_type) or isinstance(points, six.string_types):
            return self._geocode(points, ignore_cache=ignore_cache)

        if isinstance(points, (list, tuple)):
            decoded = []
            for p in points:
                if not isinstance(p, six.text_type) and not isinstance(p, six.string_types):
                    raise TypeError(
                        self.map_error_msgs['geocode_invalid_type'].format(type=type(p))
                    )
                decoded.append(self._geocode(p, ignore_cache=ignore_cache))
            return decoded

        raise TypeError(
            self.map_error_msgs['geocode_invalid_type'].format(type=type(points))
        )
