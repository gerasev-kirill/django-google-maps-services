# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import six
import json

from .base import BaseGMap
from ..models import GMapPointCache, GMapDirectionCache
from .. import exceptions


bool_to_str = lambda x: 'Yes' if x else 'No'

def find_country_name(gmap_point_data):
    data = {}
    for c in gmap_point_data['address_components']:
        if 'country' in c['types'] and 'political' in c['types']:
            data['long_name'] = c['long_name']
            data['short_name'] = c['short_name']
    return data




class GMapClient(BaseGMap):
    map_error_msgs = {
        'geocode_invalid_type': "Invalid type for geocode function. Expected <type 'str'> or <type 'unicode'> or list/tuple of this types. Got - {type}",
        'empty_geocode_result': "Empty geocode result for search string '{search_string}'",
        'no_city_in_geocode_result': "Can't find city name in geocode result for search string '{search_string}'"
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



    def _geocode_city_only(self, single_point, ignore_cache=False):
        if not ignore_cache:
            try:
                point = GMapPointCache.objects.get(id="#C# "+single_point)
                return point.data
            except GMapPointCache.DoesNotExist:
                pass

        decoded = self._run_gmap_command('geocode', single_point)
        if decoded and not ignore_cache:
            GMapPointCache.objects.create(
                id="#C# "+single_point,
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



    def geocode_city_only(self, points, ignore_cache=False):
        i = 0
        decoded = []
        _points = points
        if not isinstance(_points, (list, tuple)):
            _points = [_points]

        for p in self.geocode(_points, ignore_cache=ignore_cache):
            if not p:
                raise exceptions.EmptyGeocodeResult(
                    self.map_error_msgs['empty_geocode_result'].format(search_string=_points[i])
                )
            country = None
            city = None
            for ac in p[0].get('address_components', []):
                types = ac.get('types', [])
                if 'political' in types and 'locality' in types:
                    city = ac['long_name']
                if 'political' in types and 'country' in types:
                    country = ac['long_name']
            if not city or not country:
                raise exceptions.NoCityNameInGeocodeResult(
                    self.map_error_msgs['no_city_in_geocode_result'].format(search_string=_points[i])
                )
            decoded.append(
                self._geocode_city_only(country+', '+city, ignore_cache=ignore_cache)
            )
            i += 1

        if isinstance(points, (list, tuple)):
            return decoded
        return decoded[0]



    def geocode_country_only(self, points, ignore_cache=False):
        decoded = []
        _points = points
        if not isinstance(_points, (list, tuple)):
            _points = [_points]

        for city in self.geocode_city_only(_points, ignore_cache=ignore_cache):
            decoded.append(find_country_name(city[0]))

        if isinstance(points, (list, tuple)):
            return decoded
        return decoded[0]



    def directions(self, origin, destination,
                   waypoints=None, optimize_waypoints=True,
                   mode='driving', ignore_cache=False, **kwargs):
        if not ignore_cache:
            id = [mode, bool_to_str(optimize_waypoints), self._location_to_str(origin)]
            for w in waypoints or []:
                id.append(self._location_to_str(w))
            id.append(self._location_to_str(destination))
            id = '#' + '#'.join(id) + '#'
            try:
                point = GMapDirectionCache.objects.get(id=id)
                return point.data
            except GMapDirectionCache.DoesNotExist:
                pass

        direction = self._run_gmap_command(
            'directions',
            origin, destination,
            waypoints=waypoints, optimize_waypoints=optimize_waypoints,
            mode=mode, **kwargs
        )
        if direction and not ignore_cache:
            GMapDirectionCache.objects.filter(id=id).delete()
            GMapDirectionCache.objects.create(id=id, data=direction)
        return direction



    def direction_statistics_by_country(self, direction_data):
        statistics = []
        current_country = None
        for leg in direction_data['legs']:
            if not current_country:
                current_country = self.geocode_country_only(
                    leg['start_address']
                )

            i = 0
            for step in leg['steps']:
                i += 1
                try:
                    nextStep = leg['steps'][i]
                except:
                    nextStep = None
                #print current_country
                current_country['distance'] = current_country.get('distance', 0)
                current_country['distance'] += step['distance']['value']
                #print step['distance']['text']
                if 'entering ' in step.get('html_instructions', '').lower():
                    #print '==========================='
                    #print step['html_instructions']

                    point = self._run_gmap_command(
                        'reverse_geocode',
                        (nextStep['start_location']['lat'], nextStep['start_location']['lng'])
                    )[0]
                    country = find_country_name(point)
                    if current_country['short_name'] != country['short_name']:
                        statistics.append(current_country)
                        current_country = country
                        continue

                    point = self._run_gmap_command(
                        'reverse_geocode',
                        (nextStep['end_location']['lat'], nextStep['end_location']['lng'])
                    )[0]
                    country = find_country_name(point)
                    if current_country['short_name'] != country['short_name']:
                        statistics.append(current_country)
                        current_country = country

        statistics.append(current_country)
        return statistics
