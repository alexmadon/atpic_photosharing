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


print("""
-- WILL DO:
-- UPDATE _user_gallery_pic SET _user=(select _user_gallery._user from _user_gallery where _user_gallery.id=_user_gallery_pic._gallery);


-- UPDATE _user_gallery_pic_tag SET _user=(select _user_gallery_pic._user from _user_gallery_pic where _user_gallery_pic.id=_user_gallery_pic_tag._pic);

-- UPDATE _user_gallery_tag SET _user=(select _user_gallery._user from _user_gallery where _user_gallery.id=_user_gallery_tag._gallery);

""")

def put_values(query,table):
    db=atpic.libpqalex.db()
    hasmore=1
    query=query+b" where (_user is NULL or _user=0) and (id in (SELECT id from "+table+b" where (_user is NULL or _user=0) LIMIT 20)) returning *"
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
    print('Hi')

    queries=[
        # old table update:
        # (b"UPDATE artist_pic SET _user=(select artist_gallery.refartist from artist_gallery where artist_gallery.id=artist_pic.refartist_gallery)",b"artist_pic"),

        (b"UPDATE _user_gallery_pic SET _user=(select _user_gallery._user from _user_gallery where _user_gallery.id=_user_gallery_pic._gallery)",b"_user_gallery_pic"),
        # (b"UPDATE _user_gallery_pic_tag SET _user=(select _user_gallery_pic._user from _user_gallery_pic where _user_gallery_pic.id=_user_gallery_pic_tag._pic)",b"_user_gallery_pic_tag"),
        # (b"UPDATE _user_gallery_pic_tag SET _user=(select _user_gallery_pic._user from _user_gallery_pic where _user_gallery_pic.id=_user_gallery_pic_tag._pic and (_user_gallery_pic_tag._user is NULL or _user_gallery_pic_tag._user=0) limit 20)",b"_user_gallery_pic_tag"),

        # UPDATE _user_gallery_pic_tag SET _user=(select _user_gallery_pic._user from _user_gallery_pic where _user_gallery_pic.id=_user_gallery_pic_tag._pic)
        # (b"UPDATE _user_gallery_tag SET _user=(select _user_gallery._user from _user_gallery where _user_gallery.id=_user_gallery_tag._gallery)",b"_user_gallery_tag"),
        # (b"UPDATE _user_gallery_pic_vote SET _user=(select _user_gallery_pic._user from _user_gallery_pic where _user_gallery_pic.id=_user_gallery_pic_vote._pic)",b"_user_gallery_pic_vote"),
        ]
    for (query,table) in queries:
        put_values(query,table)
