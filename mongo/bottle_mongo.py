# -*- coding: utf-8 -*-
"""Mongo support for Bottle.

This module provides a Bottle extension for supporting MongoDB for:

    - injecting a MongoDB connection into handler functions
    - converting PyMongo style returns from handlers into JSON

This module contains the following public classes:

    - MongoPlugin -- The plugin for supporting handler functions.

"""

__all__ = ['MongoPlugin',]

try:
    from json import dumps
except ImportError:
    from simplejson import dumps
import inspect

from bottle import PluginError, response, JSONPlugin

try:
    from pymongo import MongoClient, MongoReplicaSetClient
except ImportError:
    # Backward compatibility with PyMongo 2.2
    from pymongo import Connection as MongoClient
    MongoReplicaSetClient = None

from pymongo.uri_parser import parse_uri
import bson.json_util


class MongoPlugin(object):

    """Mongo Plugin for Bottle.

    Connect to a mongodb instance, and add a DB in a Bottle callback
    Sample :

        import bottle
        from bottle.ext import mongo

        app = bottle.Bottle()
        plugin = mongo.MongoPlugin(uri="...", db="mydb", json_mongo=True)
        app.install(plugin)

        @app.route('/show/:item')
        def show(item, mongodb):
            doc = mongodb['items'].find({item:"item")})
            return doc

    uri : MongoDB hostname or uri
    db : Database
    json_mongo : Override Bottle serializer using Mongo one
    keyword : Override parameter name in Bottle function.
    post_create : Callback function to customize database obj after creation.

    This constructor passes any optional parameter of the pymongo
    Connection/MongoClient/MongoReplicaSetClient constructor.

    If you are using PyMongo 2.3 or greater, connections to ReplicaSets are
    available by passing in multiple nodes in the connection uri.

    """

    api = 2

    def get_mongo(self):
        """Return the mongo connection from the environment."""
        if self.mongo_db:
            return self.mongo_db

        if len(self.uri_params['nodelist']) > 1 and MongoReplicaSetClient:
            client = MongoReplicaSetClient(self.uri_params['nodelist'],
                                           **self.uri_params['options'])
        else:
            client = MongoClient(self.uri_params['nodelist'][0][0],
                                 self.uri_params['nodelist'][0][1],
                                 **self.uri_params['options'])

        db = client[self.uri_params['database']]
        if self.uri_params['username']:
            if not db.authenticate(self.uri_params['username'],
                                   self.uri_params['password']):
                raise PluginError('Cannot authenticate to MongoDB for '
                                  'user: %s' % self.uri_params['username'])

        if self.post_create:
            db = self.post_create(db)

        self.mongo_db = db

        return self.mongo_db

    def __init__(self, uri, db, keyword='mongodb', json_mongo=False,
                 post_create=None, **kwargs):
        if not uri:
            raise PluginError("MongoDB uri is required")

        self.uri_params = parse_uri(uri)
        if not len(self.uri_params['nodelist']):
            raise PluginError("MongoDB hostname and port not configured")

        self.uri_params['database'] = self.uri_params['database'] or db
        if not self.uri_params['database']:
            raise PluginError("MongoDB database name not configured")

        self.uri_params['options'].update(kwargs)

        self.keyword = keyword
        self.json_mongo = json_mongo
        self.mongo_db = None
        self.name = "mongo:" + keyword
        self.post_create = post_create

    def __str__(self):
        return "bottle_mongo.MongoPlugin(keyword=%r)" % (self.keyword)

    def __repr__(self):
        return "bottle_mongo.MongoPlugin(keyword=%r)" % (self.keyword)

    def normalize_object(self, obj):
        """Normalize mongo object for json serialization."""
        if isinstance(obj, dict):
            if "_id" in obj:
                obj["id"] = str(obj["_id"])
                del obj["_id"]
        if isinstance(obj, list):
            for a in obj:
                self.normalize_object(a)

    def setup(self, app):
        """Called as soon as the plugin is installed to an application."""
        for other in app.plugins:
            if not isinstance(other, MongoPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another MongoDB plugin with "
                                  "conflicting settings (non-unique keyword).")

        # Remove builtin JSON Plugin
        if self.json_mongo:
            for other in app.plugins:
                if isinstance(other, JSONPlugin):
                    app.uninstall(other)
                    return

    def apply(self, callback, context):
        """Return a decorated route callback."""
        args = inspect.getargspec(context.callback)[0]
        # Skip this callback if we don't need to do anything
        if self.keyword not in args:
            return callback

        def wrapper(*a, **ka):
            ka[self.keyword] = self.get_mongo()
            rv = callback(*a, **ka)
            if self.json_mongo:  # Override bottle JSON->String serializer
                if isinstance(rv, dict):
                    self.normalize_object(rv)
                    json_response = dumps(rv, default=bson.json_util.default)
                    response.content_type = 'application/json'
                    return json_response

            return rv

        return wrapper
