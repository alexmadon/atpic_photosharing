import atpic.database

import time
import pycurl

import StringIO
import cStringIO

time1=time.time()
for i in range(1,100):
    print i
    con=atpic.database.connect()
    listofdict=atpic.database.query("select 1",con)
    con.close()

time2=time.time()
print "=========="

con=atpic.database.connect()
for i in range(1,100):
    print i
    query="select id from artist_pic where id='%i'" % i
    listofdict=atpic.database.query(query,con)
con.close()
time3=time.time()





# using Solr + curl new curl handle each time (new socket)
#fp=open("/dev/null","w")
fp=cStringIO.StringIO()
for i in range(1,100):
    print i
    url="http://localhost:8983/solr/select/?q=pid:%i&fl=pid" % i
    c=pycurl.Curl()
    # c.setopt(c.WRITEDATA,fp);
    c.setopt(c.WRITEFUNCTION, fp.write)
    c.setopt(c.URL, url);
    c.perform()
    c.close()
    
    # print data

fp.close()
time4=time.time()

# using Solr + curl same curl handle
c=pycurl.Curl()
fp=cStringIO.StringIO()

for i in range(1,100):
    print i
    #c.setopt(c.WRITEDATA,fp);
    url="http://localhost:8983/solr/select/?q=pid:%i&fl=pid" % i
    c.setopt(c.WRITEFUNCTION, fp.write)

    c.setopt(c.URL, url);
    c.perform()
    
c.close()
fp.close()

time5=time.time()

print "Time1 %s" % (time2-time1)
print "Time2 %s" % (time3-time2)
print "Ratio=%f" % ((time2-time1)/(time3-time2))
print "Time3 %s" % (time4-time3)
print "Time4 %s" % (time5-time4)
