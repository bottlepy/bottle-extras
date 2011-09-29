=====================
Bottle-Redis
=====================

Redis is an open source, advanced key-value store. It is often referred
to as a data structure server since keys can contain strings, hashes,
lists, sets and sorted sets.

This plugin simplifies the use of redis databases in your Bottle applications.
Once installed, all you have to do is to add a ``rdb`` keyword argument
(configurable) to route callbacks that need a database connection.

Installation
===============

Install with one of the following commands::

    $ pip install bottle-redis
    $ easy_install bottle-redis

or download the latest version from github::

    $ git clone git://github.com/bottlepy/bottle-extras.git
    $ cd bottle-extras/redis
    $ python setup.py install

Usage
===============

Once installed to an application, the plugin passes an open
:class:`redis.Redis` instance to all routes that require a ``rdb`` keyword
argument::

    import bottle

    app = bottle.Bottle()
    plugin = bottle.ext.redis.RedisPlugin(host='localhost')
    app.install(plugin)

    @app.route('/show/:item')
    def show(item, rdb):
        row = rdb.get(item)
        if row:
            return template('showitem', item=item)
        return HTTPError(404, "Page not found")

Routes that do not expect a ``rdb`` keyword argument are not affected.

Configuration
=============

The following configuration options exist for the plugin class:

* **host**: Host on which the Redis server is located (default: localhost ).
* **port**: Port on which the Redis server is listening (default: 6379)
* **database** : Select the database to use (default: 0)
* **keyword**: The keyword argument name that triggers the plugin (default: 'rdb').
