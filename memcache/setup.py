#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim:set tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8:
#

import sys
import os
from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

setup(
    name = 'bottle-memcache',
    version = '0.1',
    url = 'http://github.com/sc68cal/bottle-extras/',
    description = 'Memcache integration for Bottle.',
    author = 'Jorge Gallegos',
    author_email = 'kad@blegh.net',
    license = 'MIT',
    platforms = 'any',
    py_modules = [
        'bottle_memcache'
    ],
    requires = [
        'bottle (>=0.9)',
        'memcache'
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
    cmdclass = {'build_py': build_py}
)

