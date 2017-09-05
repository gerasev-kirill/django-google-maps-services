import django, sys, os
from django.conf import settings

BASE_DIR = os.path.dirname(__file__)
SECRET_KEY = '--'

DEBUG=True
DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
INSTALLED_APPS=[
    'dj_gmap',
    'tests'
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
    }
}

DJANGO_GC_MAP_API_KEY = os.environ['DJANGO_GC_MAP_API_KEY']
