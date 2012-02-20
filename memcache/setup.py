#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim:set tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8:
#

import sys
import os
from setuptools import setup


extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True


setup(
    name = 'bottle-memcache',
    version = '0.1',
    url = 'http://github.com/bottlepy/bottle-extras/',
    description = 'Memcache integration for Bottle.',
    author = 'Jorge Gallegos',
    author_email = 'kad@blegh.net',
    license = 'MIT',
    platforms = 'any',
    py_modules = [
        'bottle_memcache'
    ],
    install_requires = [
        'distribute',
        'bottle>=0.9',
        'python-memcached',
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    **extra
)

