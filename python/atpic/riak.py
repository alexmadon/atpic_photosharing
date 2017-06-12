# store the artists

import atpic.database
import atpic.cleaner
import atpic.uni


import pycurl # debian package python-pycurl
from StringIO import StringIO


con=atpic.database.connect()

def pic_artist(artistid):
    query="select id from artist_gallery where refartist=%s" % artistid
    listofdict=atpic.database.query(query, con)
    rows=len(listofdict)
    out=[]
    if (rows>0):
        for dict in listofdict:
            # print dict
            print "artist %s, gallery id %s" % (artistid,dict["id"])
            galleryid=dict["id"]
            # json=couchdb_pic_gallery(galleryid)
            # curl_post(json)


def pic_all():
    query="select * from artist order by id limit 10000"
    listofdict=atpic.database.query(query, con)
    rows=len(listofdict)
    out=[]
    if (rows>0):
        for dict in listofdict:
            print dict
            print "artist id %s" % dict["id"]
            artistid=dict["id"]
            # pic_artist(artistid)
            json=[]
            json.append("""{"id":%s,""" % dict["id"])
            json.append(""" "admin_firstname":"%s",""" % dict["admin_firstname"])
            json.append(""" "admin_lastname":"%s",""" % dict["admin_lastname"])
            json.append(""" "admin_login":"%s",""" % dict["admin_login"])
            json.append(""" "admin_email":"%s"}""" % dict["admin_email"])
            jsons="\n".join(json)
            print jsons
            # ********** post
            url="http://127.0.0.1:8098/riak/atpica/%s?returnbody=true" % dict["id"]
            
            header = [ "Content-Type: application/json; charset=utf-8"];
            body = StringIO()
            c=pycurl.Curl()
            # $ch = cuRlq_init();
            
        
            c.setopt(c.URL, url);
            c.setopt(c.HTTPHEADER, header);
            # c.setopt(c.RETURNTRANSFER, 1);
            c.setopt(c.POST, 1)
            
            c.setopt(c.POSTFIELDS, atpic.uni.string(jsons)); # setopt expects a string
            c.setopt(c.VERBOSE, 1)
            c.setopt(c.WRITEFUNCTION, body.write)
            # c.setopt(c.HTTP_VERSION, CURL_HTTP_VERSION_1_1);
            # c.setopt(c.HEADER_OUT, 1);
            data=c.perform()
            c.close()
            contents = body.getvalue()
            print contents

pic_all()
