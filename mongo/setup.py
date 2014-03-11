#!/usr/bin/env python

from setuptools import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

setup(
    name = 'bottle-mongo',
    version = '0.2.2',
    url = 'http://github.com/bottlepy/bottle-extras/',
    description = 'MongoDB integration for Bottle',
    author = 'Florian Douetteau',
    author_email = 'florian@douetteau.net',
    license = 'MIT',
    platforms = 'any',
    py_modules = [
        'bottle_mongo'
    ],
    requires = [
        'bottle (>=0.9)',
        'pymongo'
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Environment :: Plugins',
        'Framework :: Bottle',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    cmdclass = {'build_py': build_py}
)
