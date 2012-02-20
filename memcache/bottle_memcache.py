#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim:set tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8:
#

import memcache
import inspect


class MemcachePlugin(object):

    name = 'memcache'

    def __init__(self, servers=['localhost:11211', ], keyword='mc'):

        self.servers = servers
        self.keyword = keyword

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, MemcachePlugin): continue
            if other.keyword == self.keyword:
                raise PluginError("Found another memcache plugin with "\
                        "conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        conf = context['config'].get('memcache') or {}
        servers = conf.get('servers', self.servers)
        keyword = conf.get('keyword', self.keyword)

        args = inspect.getargspec(context['callback'])[0]
        if keyword not in args:
            return callback

        def wrapper(*args,**kwargs):
            mc = memcache.Client(servers=self.servers, debug=0)
            kwargs[self.keyword] = mc
            rv = callback(*args, **kwargs)
            return rv
        return wrapper

Plugin = MemcachePlugin

