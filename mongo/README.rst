Bottle MongoDB
==============

This bottle-mongodb plugin integrates MongoDB with your Bottle
application. It injects a MongoDB session in your route and handle the
session cycle.


Usage Example:

.. code-block:: python

    from bottle import Bottle ,redirect
    from bottle.ext.mongo import MongoPlugin

    from bson.json_util import dumps


    app = Bottle()
    plugin = MongoPlugin(uri="mongodb://127.0.0.1", db="mydb", json_mongo=True)
    app.install(plugin)

    @app.route('/', method='GET')
    def index(mongodb):
        return dumps(mongodb['collection'].find())

    @app.route('/create/', method='POST')
    def create(mongodb):
        mongodb['collection'].insert({'a': 1, 'b': 2})
        redirect("/")


