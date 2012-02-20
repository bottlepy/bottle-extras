#!/usr/bin/env python
''' The bottle-extras module depends on all plugins of the bottle-extras
    collection. Installing it vith `pip` or `easy_install` also installs:
    * bottle.ext.sqlite
    * bottle.ext.werkzeug
    * bottle.ext.redis
    * bottle.ext.memcache
'''

import sys
import os
from distutils.core import setup

setup(
    name = 'bottle-extras',
    version = '0.1.0',
    url = 'http://bottlepy.org/docs/dev/plugins.html',
    description = 'Meta package to install the bottle plugin collection.',
    long_description = __doc__,
    author = 'Sean M. Collins',
    author_email = 'sean@coreitpro.com',
    license = 'MIT',
    platforms = 'any',
    requires = [
        'bottle (>=0.9)',
        'bottle_sqlite',
        'bottle_werkzeug',
        'bottle_redis',
        'bottle_memcache'
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
