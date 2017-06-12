#!/usr/bin/python3
# populate the artefacts table

import atpic.libpqalex
import atpic.cleaner
import types
import time
import difflib
import atpic.mybytes
import atpic.log

# select id,_extension,_width,_height from _user_gallery_pic where _extension='jpg' and _user=1;
# select id,_extension,_width,_height from _user_gallery_pic where _extension='jpg' and (_width>1200 or _height>1200) and _user=1;
# SELECT 'r1024' AS _code, now() AS _datestore, _extension,'o/'||_user::text||'/'||_gallery::text||'/'||id::text||'/1024.'||_extension AS _pathstore, id ,_user from _user_gallery_pic where _extension='jpg' and (_width>1200 or _height>1200) and _user=1;
# INSERT INTO _user_gallery_pic_artefact ( _code, _datestore,_extension,_pathstore, _pic, _user) VALUES ();
# INSERT INTO _user_gallery_pic_artefact ( _code, _datestore,_extension,_pathstore, _pic, _user) SELECT 'r1024' AS _code, now() AS _datestore, _extension,'o/'||_user::text||'/'||_gallery::text||'/'||id::text||'/1024.'||_extension AS _pathstore, id ,_user from _user_gallery_pic where _extension='jpg' and (_width>1200 or _height>1200) and _user=1;


xx=atpic.log.setmod("INFO","sql_pop")
# query=b"""UPDATE _user_gallery_pic SET _pathstore='o/'||_user::text||'/'||_gallery::text||'/'||id::text||'/0.'||_extension WHERE _user=$1"""
import atpic.libpqalex
import atpic.cleaner
import types
import difflib
import atpic.mybytes
import atpic.log

xx=atpic.log.setmod("INFO","sql_cleanB")
db=atpic.libpqalex.db()

maxuser=12803

resolutions=(
    (b"1024",b"1200"),
    (b"600",b"720"),
    (b"350",b"420"),
    # (b"190",b"160"),
    # (b"90",b"70"),
    (b"160",b"190"),
    (b"70",b"90"),
)
for (res,ama) in resolutions:

    query=b"INSERT INTO _user_gallery_pic_artefact ( _code, _datestore,_extension,_pathstore, _pic, _user) SELECT 'r"+res+b"' AS _code, now() AS _datestore, _extension,'o/'||_user::text||'/'||_gallery::text||'/0/'||id::text||'/"+res+b".'||_extension AS _pathstore, id ,_user from _user_gallery_pic where _extension='jpg' and (_width>"+ama+b" or _height>"+ama+b") and _user=$1"
    print(query)
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    for i in range(0,maxuser):
        print("echo doing user",i,"/",maxuser,res)
        uid=atpic.mybytes.int2bytes(i)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',(uid,))
        print(result)
        result=atpic.libpqalex.process_result(result)
        print(result)
        
