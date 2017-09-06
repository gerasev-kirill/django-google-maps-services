import os
from setuptools import setup
try:
    README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    README = ''

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

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
    install_requires=[
        'Django>=1.11',
        'googlemaps>=2.5.0',
        'jsonfield',
        'unidecode'
    ],
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
