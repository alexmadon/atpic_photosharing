#!/usr/bin/python3

# we add a '_user' column to each table below user:
# this can help in database partitionning and database clustering

import atpic.libpqalex
import atpic.cleaner
import types
import time
import difflib
import atpic.mybytes
import atpic.log

xx=atpic.log.setmod("INFO","worker")
# WITH theids AS (SELECT id,_pic FROM _user_gallery_pic_tag WHERE _user is NULL OR _user=0 LIMIT 10)
# SELECT * FROM theids;


# WITH 
# idpic AS (SELECT id,_pic FROM _user_gallery_pic_tag WHERE _user is NULL OR _user=0 LIMIT 10),
# userpic AS (SELECT _user_gallery_pic._user,idpic.id,idpic._pic FROM _user_gallery_pic,idpic WHERE _user_gallery_pic.id=idpic._pic)
# SELECT * FROM userpic;



def put_values(query):
    db=atpic.libpqalex.db()
    hasmore=1
    print("doing: ",query)
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    loop=0
    while (hasmore> 0):
        start = time.time() # better than time.clock()
        loop=loop+1
        print('HASMORE',loop,query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',())
        result=atpic.libpqalex.process_result(result)
        listofdict=result # result.dictresult()
        print(query)
        rows=len(listofdict)
        print("rows",rows)
        if rows>0:
            hasmore=1
        else:
            hasmore=0
        elapsed = time.time() - start
        print('records/sec=',rows/elapsed,'(',rows,'/',elapsed,')')


if __name__ == "__main__":
    query_list=[
        b"""WITH 
idpic AS (SELECT id,_pic FROM _user_gallery_pic_tag WHERE _user is NULL OR _user=0 LIMIT 100),
userpic AS (SELECT _user_gallery_pic._user,idpic.id,idpic._pic FROM _user_gallery_pic,idpic WHERE _user_gallery_pic.id=idpic._pic)
UPDATE _user_gallery_pic_tag set _user=userpic._user FROM userpic WHERE userpic.id=_user_gallery_pic_tag.id AND userpic._pic=_user_gallery_pic_tag._pic RETURNING *""",
        b"""WITH 
idpic AS (SELECT id,_pic FROM _user_gallery_pic_vote WHERE _user is NULL OR _user=0 LIMIT 100),
userpic AS (SELECT _user_gallery_pic._user,idpic.id,idpic._pic FROM _user_gallery_pic,idpic WHERE _user_gallery_pic.id=idpic._pic)
UPDATE _user_gallery_pic_vote set _user=userpic._user FROM userpic WHERE userpic.id=_user_gallery_pic_vote.id AND userpic._pic=_user_gallery_pic_vote._pic RETURNING *""",
        b"""WITH 
idgallery AS (SELECT id,_gallery FROM _user_gallery_tag WHERE _user is NULL OR _user=0 LIMIT 100),
usergallery AS (SELECT _user_gallery._user,idgallery.id,idgallery._gallery FROM _user_gallery,idgallery WHERE _user_gallery.id=idgallery._gallery)
UPDATE _user_gallery_tag set _user=usergallery._user FROM usergallery WHERE usergallery.id=_user_gallery_tag.id AND usergallery._gallery=_user_gallery_tag._gallery RETURNING *""",

        b"""WITH 
sel1 AS (SELECT * FROM _user_gallery_comment WHERE _user IS NULL OR _user=0 LIMIT 10)
UPDATE _user_gallery_comment SET _user=_user_gallery._user FROM sel1,_user_gallery WHERE _user_gallery_comment._gallery=_user_gallery.id AND sel1._gallery=_user_gallery.id
RETURNING *""",


        b"""WITH 
sel1 AS (SELECT * FROM _user_gallery_pic_comment WHERE _user IS NULL OR _user=0 LIMIT 200)
UPDATE _user_gallery_pic_comment SET _user=_user_gallery_pic._user FROM sel1,_user_gallery_pic WHERE _user_gallery_pic_comment._pic=_user_gallery_pic.id AND sel1._pic=_user_gallery_pic.id
RETURNING *""",



#        b"""WITH 
# iduser AS (SELECT id,_user FROM _user_tag WHERE _user is NULL OR _user=0 LIMIT 100),
# useruser AS (SELECT _user._user,iduser.id,iduser._user FROM _user,iduser WHERE _user.id=iduser._user)
# UPDATE _user_tag set _user=useruser._user FROM useruser WHERE useruser.id=_user_tag.id AND useruser._user=_user_tag._user RETURNING *""",


        ]
    for query in query_list:
        put_values(query)
