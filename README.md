
# Ecommer Django App
## live-link :- #

This Ecommer Website 
<b>coded by [Aman Verma](https://github.com/itsamanverma)</b>
### 👍 HAVE FUN 👍
Thanks, people

![Watch Now](./ecom.jpg)

Deploy

Building
It is best to use the python virtualenv tool to build locally:

$ virtualenv-2.7 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ DEVELOPMENT=1 python manage.py runserver
Then visit http://localhost:8000 to view the app. Alternatively you can use foreman and gunicorn to run the server locally (after copying dev.env to .env):

$ foreman start
Deploy to Heroku
Run the following commands to deploy the app to Heroku:

$ git clone https://github.com/itsamanverma/Djnago_ecommer.git
$ cd ecom
$ heroku create
$ heroku addons:add memcachier:dev
$ git push heroku master:master
$ heroku open
requirements.txt
MemCachier has been tested with the pylibmc memcache client, but the default client doesn't support SASL authentication. Run the following commands to install the necessary pips:

$ sudo brew install libmemcached
$ pip install django-pylibmc pylibmc
Don't forget to update your requirements.txt file with these new pips. requirements.txt should have the following two lines:

django-pylibmc==0.6.1
pylibmc==1.5.1
Configuring MemCachier (settings.py)
To configure Django to use pylibmc with SASL authentication. You'll also need to setup your environment, because pylibmc expects different environment variables than MemCachier provides. Somewhere in your settings.py file you should have the following lines:

os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
    'default': {
        # Use pylibmc
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',

        # Use binary memcache protocol (needed for authentication)
        'BINARY': True,

        # TIMEOUT is not the connection timeout! It's the default expiration
        # timeout that should be applied to keys! Setting it to `None`
        # disables expiration.
        'TIMEOUT': None,
        'OPTIONS': {
            # Enable faster IO
            'tcp_nodelay': True,

            # Keep connection alive
            'tcp_keepalive': True,

            # Timeout settings
            'connect_timeout': 2000, # ms
            'send_timeout': 750 * 1000, # us
            'receive_timeout': 750 * 1000, # us
            '_poll_timeout': 2000, # ms

            # Better failover
            'ketama': True,
            'remove_failed': 1,
            'retry_timeout': 2,
            'dead_timeout': 30,
        }
    }
}
Persistent Connections
By default, Django doesn't use persistent connections with memcached. This is a huge performance problem, especially when using SASL authentication as the connection setup is even more expensive than normal.

You can fix this by putting the following code in your wsgi.py file:

# Fix django closing connection to MemCachier after every request (#11331)
from django.core.cache.backends.memcached import BaseMemcachedCache
BaseMemcachedCache.close = lambda self, **kwargs: None
There is a bug file against Django for this issue (#11331).

Application Code
In your application, use django.core.cache methods to access MemCachier. A description of the low-level caching API can be found here. All the built-in Django caching tools will work, too.

Take a look at memcachier_algebra/views.py in this repository for an example.

Get involved!
We are happy to receive bug reports, fixes, documentation enhancements, and other improvements.

Please report bugs via the github issue tracker.

Master git repository:

git clone https://github.com/itsamanverma/Djnago_ecommer.git
Licensing
This library is BSD-licensed.