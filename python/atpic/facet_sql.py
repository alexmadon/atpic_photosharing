#!/usr/bin/python3
# we avoid elasticsearch factes
# as we know in advance (cheap) the terms of the facets
# select _user,id,_path from _user_gallery order by _user,id;

# we know the UID, as this is for user site navigation:

# select _user,id,_path from _user_gallery where regexp_matches() order by _user,id;
# select _user,id,_path from _user_gallery where _path ~'^/avignon/[^/]+/$' order by _user,id;
# select _user,id,_path from _user_gallery where _path ~'^avignon/[^/]+$' order by _user,id;

# now virtual dirs:
# mydatabase=# select * from _user_gallery_pic_path;
#  _datelast | _pic |    _path     | _user | id 
# -----------+------+--------------+-------+----
#            |    1 | /alex/china/ |     1 |  1
#            |    1 | /alex/best/  |     1 |  2
# (2 rows)

# concatenate array_to_string as it is difficult to pass arays in libpq
"""
WITH
a1 AS (SELECT id,string_to_array(_path,'/') as pathar, _path FROM _user_gallery where _user=1),
a2 AS (SELECT * FROM a1 where array_to_string(pathar[1:1],'/') = 'italia2006')
SELECT DISTINCT(pathar[2]) FROM a2 WHERE array_length(pathar,1)> 1;
"""
# then a DISTINCT
# WITH
# a1 AS (SELECT string_to_array(trim(both '/' from _path),'/') as pathar FROM _user_gallery_pic_path WHERE _user=1)
# SELECT * FROM a1;
import time

import atpic.forgesql
import atpic.mybytes

def query_dir(uid,path,table=b'_user_gallery'):
    # table can be:
    # b'_user_gallery'
    # b'_user_gallery_pic_path'
    query_list=[]
    path=path.strip(b'/')
    slashnb=path.count(b'/')
    if path==b'':
        slashnb=-1
    print('slashnb',slashnb)
    query_list.append(b"WITH")
    # breaks into an array
    query_list.append(b"a1 AS (SELECT id,string_to_array(_path,'/') as pathar, _path FROM "+table+b" where _user=$),")
    # concats into an string the first N elements of the array so that we can have an exact match on 'path'
    query_list.append(b"a2 AS (SELECT * FROM a1 where array_to_string(pathar[0:$],'/') = $)")
    query_list.append(b"SELECT DISTINCT(pathar[$]) as apath FROM a2 WHERE array_length(pathar,1)> $ ORDER BY apath")
    query=b' '.join(query_list)
    query_args=[
        uid,
        atpic.mybytes.int2bytes(slashnb+1),
        path,atpic.mybytes.int2bytes(slashnb+2),
        atpic.mybytes.int2bytes(slashnb+1)
        ]
    (query,query_args)=atpic.forgesql.transform(query,query_args)
    return  (query,query_args)


def query_dir2list(conn,uid,path,table=b'_user_gallery'):
    (query,query_args)=query_dir(uid,path,table) 
    statement=b""
    t1=time.time()
    result1=atpic.libpqalex.pq_prepare(conn,statement,query)
    result=atpic.libpqalex.pq_exec_prepared(conn,statement,query_args)
    res=atpic.libpqalex.process_result(result)
    t2=time.time()
    print('took',t2-t1)
    out=[]
    for ares in res:
        out.append(ares[b'apath'])
    print('out',out)
    return out

if __name__ == "__main__":
    # (query,query_args)=query_dir(b'1',b'alex',b'_user_gallery_pic_path') # (b'1',b'italia2006')
    # (query,query_args)=query_dir(b'1',b'',b'_user_gallery') # (b'1',b'italia2006')
    # print((query,query_args))



    import atpic.libpqalex
    conn=atpic.libpqalex.db()
    query_dir2list(conn,b'1',b'',b'_user_gallery') 
    query_dir2list(conn,b'1',b'',b'_user_gallery_pic_path') 
