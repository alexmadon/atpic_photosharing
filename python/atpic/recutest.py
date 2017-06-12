-- WITH RECURSIVE test

SELECT id,_file,_dir,_isroot FROM _user_gallery WHERE _user=1 AND _isroot='r'
UNION
SELECT id,_file,_dir,_isroot,coalesce(_file,id::text) FROM _user_gallery WHERE _user=1 AND _isroot='n';


WITH RECURSIVE _user_gallery_descendants(id,_dir) AS (
SELECT _user_gallery.id,_user_gallery._dir from _user_gallery where _user_gallery._user=1 and _user_gallery._isroot='r'
UNION ALL
SELECT _user_gallery.id,_user_gallery._dir
FROM _user_gallery_descendants,_user_gallery WHERE _user_gallery._dir=_user_gallery_descendants.id and _user_gallery._user=1
)
select id,_dir from _user_gallery_descendants;





EXPLAIN
WITH RECURSIVE _user_gallery_descendants(id,_dir,path) AS (
SELECT _user_gallery.id,_user_gallery._dir,'/' from _user_gallery where _user_gallery._user=1 and _user_gallery._isroot='r'
UNION ALL
SELECT _user_gallery.id,_user_gallery._dir,_user_gallery_descendants.path||coalesce(_user_gallery._file,_user_gallery.id::text)||'/'
FROM _user_gallery_descendants,_user_gallery WHERE _user_gallery._dir=_user_gallery_descendants.id and _user_gallery._user=1
)
select id,_dir,path from _user_gallery_descendants;



=====================



WITH RECURSIVE _user_gallery_descendants(id,_dir,path,ctime,mtime) AS (
SELECT _user_gallery.id,_user_gallery._dir,'/',extract(EPOCH from _user_gallery._datefirst),extract(EPOCH from _user_gallery._datelast) from _user_gallery where _user_gallery._user=20 and _user_gallery._isroot='r'
UNION ALL
SELECT _user_gallery.id,_user_gallery._dir,'/'||trim(leading '/' from _user_gallery_descendants.path||'/'||coalesce(_user_gallery._file,_user_gallery.id::text)),extract(EPOCH from _user_gallery._datefirst),extract(EPOCH from _user_gallery._datelast)
FROM _user_gallery_descendants,_user_gallery WHERE _user_gallery._dir=_user_gallery_descendants.id and _user_gallery._user=20
)
select id,_dir,path,ctime::int,mtime::int  from _user_gallery_descendants;










SELECT * FROM _user_gallery where id not in (select id from _user_gallery_descendants) and _user_gallery._user=$ and id>$ order by id limit 10;
