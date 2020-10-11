# -*- coding: utf-8 -*-
import django, copy


if django.VERSION[0] >= 3 and django.VERSION[1] >= 1:
    from django.db.models import JSONField as JSONFieldBase
    from django.core.serializers.json import DjangoJSONEncoder

    '''
        https://docs.djangoproject.com/en/3.1/ref/models/fields/
        If you give the field a default, ensure it’s an immutable object, such as a str,
        or a callable object that returns a fresh mutable object each time,
        such as dict or a function.
        Providing a mutable default object like default={} or default=[] shares the one object between all model instances.
    '''

    class JSONField(JSONFieldBase):
        def __init__(self, *args, **kwargs):
            if 'encoder' not in kwargs:
                kwargs['encoder'] = DjangoJSONEncoder
            self.__default_value = kwargs.get('default', None)
            if self.__default_value is not None and not callable(self.__default_value):
                kwargs['default'] = kwargs['default'].__class__
            super(JSONField, self).__init__(*args, **kwargs)

        def get_default(self):
            """Return the default value for this field."""
            if self.__default_value is not None:
                return copy.deepcopy(self.__default_value)
            return self._get_default()


else:
    from jsonfield.fields import JSONFieldBase, models

    class JSONField(JSONFieldBase, models.TextField):
        def __init__(self, *args, encoder=None, decoder=None, **kwargs):
            super(JSONField, self).__init__(*args, **kwargs)
