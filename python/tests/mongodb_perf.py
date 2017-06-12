import time
from pymongo.connection import Connection
connection = Connection()
db = connection.mydb
for collection in db.collection_names():
    print collection


collection = db.testCollection

doc = {"name": "MongoDB",
       "type": "database",
       "count": 1,
       "info": {"x": 203,
                "y": 102
                }
       }
collection.insert(doc)
print collection.find_one()

time1=time.time()
for i in range(1000000):
    collection.insert({"i": i})

time2=time.time()
dt=time2-time1
print "time mongodb: %s" % dt

print "thecount=%s" % collection.count()


quit()



cursor = collection.find()
for d in cursor:
    print d
    for key in d:
        print key
        print d[key]
        print d["i"]
    # print "a cursor %s" % d[u'i']




query = {"i": 71}
for d in collection.find(query):
    print d
