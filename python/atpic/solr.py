#!/usr/bin/python3
# expects 2 arguments $type and $id (and $test)
# example:
# http:# atpic.foo/solr_post.php?type=a&id=2


# =========
#  $picid
#  or $galleryid
#  or artistid
# depending on what is updated (cascade to all picture if artist or gallery)
# an update is triggered at each tag update
# at each vote

# ====pop====
# put the popularity formula
# if a tag is added by another
# if vote

# === tag repeat====
#  a tag counts as 3 times if in pic
#  2 times in gallery
#  1 time in artist


# multiply by 2 if tagger different from 

# =====

# the tag cloud is just a dummy count

# don't hard code the picture URL as a server IP change would me re-index all
# instead store the logical entities necessary to build the image URL using XSL

# generate the <doc>
# expects a type and a $id

# cd ~/solr/apache-solr-1.3.0/example
# java -jar start.jar
# /home/madon/public_html/perso/entreprise/sql_current/site/atpic/config/conf/solr/schema.xml


# faceting by date (photoblog) 
# http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.field=date&facet.date=date&facet.date.start=NOW/DAY-12500DAYS&facet.date.end=NOW/DAY%2B1DAY&facet.date.gap=%2B1DAY

# http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.field=tag
# http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.field=tag&facet.prefix=a


# http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.field=make


# http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.field=model



from http.client import HTTPConnection
import urllib.request
import atpic.solr_sqlbased

def solr_query(query):
    f = urllib.request.urlopen(query.decode('utf8'))
    out=f.read()
    return out


def solr_add(type,id):
    """
    Add a document to index
    """
    DATA = atpic.solr_sqlbased.solr_generate(type,id)
    DATA=DATA.encode("utf-8")
    con = HTTPConnection('0.0.0.0:8983')
    con.putrequest('POST', '/solr/update/')
    con.putheader('content-length', str(len(DATA)))
    con.putheader('content-type', 'text/xml; charset=UTF-8')
    con.putheader('connection', 'close')
    con.endheaders()
    con.send(DATA)
    r = con.getresponse()
    if str(r.status) == '200':
        print(r.read())
    else:
        print(r.status)
        print(r.read())
        
def solr_commit():
    """
    commit changes
    """
    DATA = '<commit/>'
    DATA=DATA.encode("utf-8")
    con = HTTPConnection('0.0.0.0:8983')
    con.putrequest('POST', '/solr/update/')
    con.putheader('content-length', str(len(DATA)))
    con.putheader('content-type', 'text/xml; charset=UTF-8')
    con.endheaders()
    con.send(DATA)
    r = con.getresponse()
    if str(r.status) == '200':
        print(r.read())
    else:
        print(r.status)
        print(r.read())

if __name__ == "__main__":
    import sys
    # print sys.argv[1]
    # print(solr_generate('user',sys.argv[1]))
    solr_add('user',int(sys.argv[1]))
    solr_commit()
    # time for i in `seq 1 8537`; do date; echo doing $i; ./solr.py $i;  done
