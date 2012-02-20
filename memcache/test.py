#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim:set tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8:
#

import unittest
import os
import bottle
from bottle.ext import memcache as mc_plugin
import memcache
from datetime import datetime

class MemcacheTest(unittest.TestCase):

    test_key = 'bottle_memcache_test_value'

    def setUp(self):
        self.app = bottle.Bottle(catchall=False)

    def test_with_keyword(self):
        self.plugin = self.app.install(mc_plugin.Plugin())

        @self.app.get('/')
        def test(mc):
            self.assertEqual(type(mc), type(memcache.Client(servers=['localhost:11211'])))
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET'}, lambda x, y: None)

    def test_without_keyword(self):
        self.plugin = self.app.install(mc_plugin.Plugin())

        @self.app.get('/')
        def test():
            pass
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET'}, lambda x, y: None)

        @self.app.get('/2')
        def test(**kw):
            self.assertFalse('mc' in kw)
        self.app({'PATH_INFO':'/2', 'REQUEST_METHOD':'GET'}, lambda x, y: None)

    def test_set_and_retrieve(self):
        self.plugin = self.app.install(mc_plugin.Plugin())

        @self.app.get('/3')
        def test(mc):
            in_val = str(datetime.now())
            mc.set(self.test_key, in_val)
            mc2 = memcache.Client(servers=['localhost:11211'])
            out_val = mc2.get(self.test_key)
            self.assertEqual(in_val, out_val)
        self.app({'PATH_INFO':'/3', 'REQUEST_METHOD':'GET'}, lambda x, y: None)

    def tearDown(self):
        mc2 = memcache.Client(servers=['localhost:11211'])
        mc2.delete(self.test_key)

if __name__ == '__main__':
    unittest.main()

