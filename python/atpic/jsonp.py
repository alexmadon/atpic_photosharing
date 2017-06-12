"""
json protcol used by the internal servers:

Tokyo POSTs
SQL layer
Disk layer

More secure than 'pickle' (?)
"""
# http://deron.meranda.us/python/comparing_json_modules/
# import json # in 2.6
import simplejson as json

def serialize(apython):
    return json.dumps(apython)


def unserialize(ajson):
    return json.loads(ajson)
