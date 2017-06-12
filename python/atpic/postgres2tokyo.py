# we open PG
# and we open tokyo
import time

import atpic.database
import atpic.tokyo as tc

# profiler
from guppy import hpy

con = atpic.database.connect()
tdb=tc.Tdb("tokyodb.tct", tc.TDBOWRITER | tc.TDBOCREAT)

def artists():
    print "Doing artists"
    query="select id,servershort from artist order by id"
    listofdict=atpic.database.query(query, con)
    rows=len(listofdict)
    for thedict in listofdict:
        # print "i=%s" % i
        # thedict=listofdict[i]
        print "a%s,servershort=%s" % (thedict["id"],thedict["servershort"])
        # keep tokyo names short
        # n=node, "p"=path, t=type (a,g,p)
        tdb.put("a%s" % thedict["id"],{"t":"a","n":thedict["id"],"p":thedict["servershort"]}) 
    h = hpy()
    print h.heap()

def galleries(offset):

    print "Doing galleries"
    query="select id,refartist,file from artist_gallery order by id limit 1000 offset %s " % offset
    listofdict=atpic.database.query(query, con)
    rows=len(listofdict)
    for thedict in listofdict:
        # print "i=%s" % i
        # thedict=listofdict[i]
        # keep tokyo names short
        # n=node, "p"=path, t=type (a,g,p)
        if not thedict["file"]:
            tfile=thedict["id"]
        else:
            tfile=thedict["file"]
        print "g%s,file=%s,nfile=%s" % (thedict["id"],thedict["file"],tfile)
        tdb.put("g%s" % thedict["id"],{"t":"g","n":thedict["id"],"p":tfile,"a":thedict["refartist"]}) 
    h = hpy()
    print h.heap()
    return rows


def pictures(offset):

    print "Doing pics"
    time1=time.time()
    query="select id,refartist_gallery,originalname,date_part('epoch',datetimeoriginalsql) as unixtime ,sizeb from artist_pic order by id limit 1000 offset %s " % offset
    listofdict=atpic.database.query(query, con)
    time2=time.time()
    dt=time2-time1
    print "query was done is %s" % dt
    rows=len(listofdict)
    for thedict in listofdict:
        # print "i=%s" % i
        # thedict=listofdict[i]
        # keep tokyo names short
        # n=node, "p"=path, t=type (a,g,p), 'g', the parent gid
        
        print "p%s,file=%s,sizeb=%s,date=%s" % (thedict["id"],thedict["originalname"],thedict["sizeb"],thedict["unixtime"])
        tdb.put("p%s" % thedict["id"],
                {"t":"p",
                 "n":thedict["id"],
                 "p":thedict["originalname"],
                 "d":thedict["unixtime"],
                 "s":thedict["sizeb"],
                 "g":thedict["refartist_gallery"],
                 }) 
    time3=time.time()
    dt=time3-time2
    print "insert was done is %s" % dt
    h = hpy()
    print h.heap()

    return rows



artists()
for i in range(0,1000):
    rows=galleries(i*1000)
    print "loop %s, rows=%s" % (i,rows)
    if rows==0:
        break

for i in range(0,1000):
    rows=pictures(i*1000)
    print "loop %s, rows=%s" % (i,rows)
    if rows==0:
        break

tdb.close()
con.close()
