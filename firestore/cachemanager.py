import firebase_admin
from cachetools import TTLCache, cached
from firebase_admin import db

ADMIN_CACHE = TTLCache(maxsize=128, ttl=3600*24)
INCIDENT_CACHE = TTLCache(maxsize=1024, ttl=3600*24)
INCIDENT_STATS_CACHE = TTLCache(maxsize=1024, ttl=3600*24)


def flush_cache():
    ADMIN_CACHE.clear()
    INCIDENT_CACHE.clear()
    INCIDENT_STATS_CACHE.clear()


def __listener(event):
    ADMIN_CACHE.clear()
    INCIDENT_CACHE.clear()
    INCIDENT_STATS_CACHE.clear()
    print(event.event_type)  # can be 'put' or 'patch'
    print(event.path)  # relative to the reference, it seems
    print(event.data)  # new data at /reference/event.path. None if deleted


# Make sure to create a realtime db with the following URL and a json path called as /cache_update
my_app_name = 'hate-crime-tracker'
options = {'databaseURL': 'https://hate-crime-tracker-default-rtdb.firebaseio.com',
           'storageBucket': 'hate-crime-tracker.appspot.com'}
filebase_app = firebase_admin.initialize_app(options=options, name=my_app_name)
db.reference('/cache_update', app=filebase_app).listen(__listener)
