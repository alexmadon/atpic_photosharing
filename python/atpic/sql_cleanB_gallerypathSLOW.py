#!/usr/bin/python3

# populate the new gallery _path 
"""

WITH RECURSIVE _user_gallery_ancestors(id,_dir) 
AS (SELECT _user_gallery.id,_user_gallery._dir FROM _user_gallery WHERE _user_gallery._user=1 AND _user_gallery.id=1
UNION ALL
SELECT _user_gallery.id,_user_gallery._dir
FROM _user_gallery_ancestors,_user_gallery WHERE _user_gallery.id=_user_gallery_ancestors._dir AND _user_gallery._user=1)
SELECT * FROM _user_gallery_ancestors;



WITH RECURSIVE _user_gallery_ancestors(id,_dir) 
AS (
SELECT _user_gallery.id,_user_gallery._dir FROM _user_gallery WHERE _user_gallery._user=1 AND _user_gallery.id=1
UNION ALL
SELECT _user_gallery.id,_user_gallery._dir
FROM _user_gallery_ancestors,_user_gallery WHERE _user_gallery.id=_user_gallery_ancestors._dir AND _user_gallery._user=1
)
SELECT * FROM _user_gallery_ancestors;



WITH RECURSIVE _user_gallery_descendants(id,_dir,path) AS (
SELECT _user_gallery.id,_user_gallery._dir,'/' from _user_gallery where _user_gallery._user=1 and _user_gallery._dir=0
UNION ALL
SELECT _user_gallery.id,_user_gallery._dir,_user_gallery_descendants.path||coalesce(_user_gallery._file,_user_gallery.id::text)||'/'
FROM _user_gallery_descendants,_user_gallery WHERE _user_gallery._dir=_user_gallery_descendants.id and _user_gallery._user=1
)
select id,_dir,path from _user_gallery_descendants;








WITH RECURSIVE _user_gallery_descendants(id,_dir,path) AS (
SELECT _user_gallery.id,_user_gallery._dir,'/'||coalesce(_user_gallery._file,_user_gallery.id::text)||'/' from _user_gallery where _user_gallery._user=1 and _user_gallery._dir=0
UNION ALL
SELECT _user_gallery.id,_user_gallery._dir,_user_gallery_descendants.path||coalesce(_user_gallery._file,_user_gallery.id::text)||'/'
FROM _user_gallery_descendants,_user_gallery WHERE _user_gallery._dir=_user_gallery_descendants.id and _user_gallery._user=1
)
SELECT id,_dir,path from _user_gallery_descendants;



WITH RECURSIVE _user_gallery_descendants(id,_dir,path) AS (
SELECT _user_gallery.id,_user_gallery._dir,'/'||coalesce(_user_gallery._file,_user_gallery.id::text)||'/' from _user_gallery where _user_gallery._user=1256 and _user_gallery._dir=0
UNION ALL
SELECT _user_gallery.id,_user_gallery._dir,_user_gallery_descendants.path||coalesce(_user_gallery._file,_user_gallery.id::text)||'/'
FROM _user_gallery_descendants,_user_gallery WHERE _user_gallery._dir=_user_gallery_descendants.id and _user_gallery._user=1256
)
SELECT * from  _user_gallery_descendants;

UPDATE _user_gallery set _path=_user_gallery_descendants.path from _user_gallery_descendants where _user_gallery._user=1256 and _user_gallery.id=_user_gallery_descendants.id;

SELECT * from  _user_gallery_descendants;

UPDATE _user_gallery set _path=_user_gallery_descendants.path from _user_gallery_descendants where _user_gallery._user=1256 and _user_gallery.id=_user_gallery_descendants.id;




"""


"""
select id,_user,_dir,_file from _user_gallery where _user=1;

  id   | _user | _dir |    _file     
-------+-------+------+--------------
 17733 |     1 |    0 | test3
  7700 |     1 |    0 | italia2006
  7699 |     1 | 7700 | matrimonio
  7701 |     1 | 7700 | firenze
     7 |     1 |    0 | 
 12008 |     1 |    0 | macrod40
   128 |     1 |    3 | dama
 19859 |     1 |    0 | for_sale
     3 |     1 |    0 | avignon
 21716 |     1 |    0 | nathalie
 23109 |     1 |    0 | people
 38764 |     1 |    0 | screen_shots
 49724 |     1 |    0 | nikond40
 43577 |     1 |    0 | testp
  1035 |     1 |    1 | 
   145 |     1 |    0 | 
  5317 |     1 |    0 | 
     4 |     1 |    0 | 
     1 |     1 |    3 | 
(19 rows)



update _user_gallery set _dir=0 where _path is null;



"""





query=b"""
WITH RECURSIVE _user_gallery_descendants(id,_dir,path) AS (
SELECT _user_gallery.id,_user_gallery._dir,'/'||coalesce(_user_gallery._file,_user_gallery.id::text)||'/' from _user_gallery where _user_gallery._user=$1 and _user_gallery._dir=0
UNION ALL
SELECT _user_gallery.id,_user_gallery._dir,_user_gallery_descendants.path||coalesce(_user_gallery._file,_user_gallery.id::text)||'/'
FROM _user_gallery_descendants,_user_gallery WHERE _user_gallery._dir=_user_gallery_descendants.id and _user_gallery._user=$2
)
UPDATE _user_gallery set _path=trim(both '/' from _user_gallery_descendants.path) from _user_gallery_descendants where _user_gallery._user=$3 and _user_gallery.id=_user_gallery_descendants.id
RETURNING *
"""
import atpic.libpqalex
import atpic.cleaner
import types
import difflib
import atpic.mybytes
import atpic.log

xx=atpic.log.setmod("INFO","sql_cleanB")
db=atpic.libpqalex.db()

ps=atpic.libpqalex.pq_prepare(db,b'',query)
maxuser=12803
# maxuser=1
for i in range(0,maxuser):
    print("echo doing user",i,"/",maxuser)
    uid=atpic.mybytes.int2bytes(i)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(uid,uid,uid,))
    print(result)
    result=atpic.libpqalex.process_result(result)
    print(result)
