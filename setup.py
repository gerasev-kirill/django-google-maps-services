import os, sys
from setuptools import setup
try:
    README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    README = ''

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requirements = [
    'Django>=1.11',
    'googlemaps>=2.5.0',
    'unidecode'
]

try:
    import django
    if django.VERSION >= (3,1,0):
        pass
    else:
        requirements.append('jsonfield')
except ImportError:
    if sys.version_info.major >= (3,8,0):
        requirements[0] = 'Django>=3.1'
    else:
        requirements.append('jsonfield')

setup(
    name='django-google-maps-services',
    version='0.1.0',
    packages=['dj_gmap'],
    include_package_data=True,
    license='BSD License',
    description='Google maps caching functions for django. + helpers',
    long_description=README,
    author='Gerasev Kirill',
    author_email='gerasev.kirill@gmail.com',
    install_requires=requirements,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
