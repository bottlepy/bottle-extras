# -*- coding: utf-8 -*-
from bottle import PluginError, response

try:
    from pymongo import MongoClient, MongoReplicaSetClient
except ImportError:
    # Backward compatibility with PyMongo 2.2
    from pymongo import Connection as MongoClient
    MongoReplicaSetClient = None

from pymongo.cursor import Cursor
from pymongo.uri_parser import parse_uri
from bottle import JSONPlugin
import bson.json_util

try:
    from json import dumps as json_dumps
except ImportError:
    from simplejson import dumps as json_dumps
import inspect


class MongoPlugin(object):
    """
    Mongo Plugin for Bottle
    Connect to a mongodb instance, and  add a DB in a Bottle callback
    Sample :

    app = bottle.Bottle()
    plugin = bottle.ext.mongo.MongoPlugin(uri="...", db="mydb", json_mongo=True)
    app.install(plugin)

    @app.route('/show/:item')
    def show(item, mongodb):
        doc = mongodb['items'].find({item:"item")})
        return doc
    """
    api = 2

    mongo_db = None

    def get_mongo(self):
        "Retrieve the mongo instance from the environment"
        if self.mongo_db:
            return self.mongo_db

        if len(self.uri_params['nodelist']) > 1 and MongoReplicaSetClient:
            client = MongoReplicaSetClient(self.uri_params['nodelist'], **self.uri_params['options'])
        else:
            client = MongoClient(self.uri_params['nodelist'][0][0], self.uri_params['nodelist'][0][1],
                                 **self.uri_params['options'])

        db = client[self.uri_params['database']]
        if self.uri_params['username']:
            if not db.authenticate(self.uri_params['username'], self.uri_params['password']):
                raise PluginError('Cannot authenticate to MongoDB for user: %s' % self.uri_params['username'])

        self.mongo_db = db
        return self.mongo_db

    def __init__(self, uri, db, keyword='mongodb', json_mongo=False, **kwargs):
        """
        uri : MongoDB hostname or uri
        db : Database
        json_mongo : Override Bottle serializer using Mongo one
        keyword : Override parameter name in Bottle function.
        This constructor any optional parameter of the pymongo.Connection constructor.
        """
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

    def normalize_object(self, obj):
        """Normalize mongo object for json serialization"""
        if isinstance(obj, dict):
            if "_id" in obj:
                obj["id"] = str(obj["_id"])
                del obj["_id"]
        if isinstance(obj, list):
            for a in obj:
                self.normalize_object(a)

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, MongoPlugin): continue
            if other.keyword == self.keyword:
                raise PluginError("Found another MongoDB plugin with "\
                        "conflicting settings (non-unique keyword).")
                        
        # Remove builtin JSON Plugin
        if self.json_mongo:
            for other in app.plugins:
                if isinstance(other, JSONPlugin):
                    app.uninstall(other)
                    return

    def apply(self, callback, context):
        dumps = json_dumps
        if not dumps: return callback

        args = inspect.getargspec(context.callback)[0]

        def wrapper(*a, **ka):
            if self.keyword in args:
                ka[self.keyword] = self.get_mongo()
            rv = callback(*a, **ka)
            if self.json_mongo:  # Override builtin bottle JSON->String serializer
                if isinstance(rv, Cursor):
                    rv = [record for record in rv]

                if isinstance(rv, dict) or isinstance(rv, list):
                    self.normalize_object(rv)
                    json_response = dumps(rv, default=bson.json_util.default)
                    response.content_type = 'application/json'
                    return json_response

            return rv

        return wrapper

