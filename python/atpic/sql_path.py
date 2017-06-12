# try to implement in SQL the solr grouping feature as
# it doesnot exist in elastic search yet as per 0.9.10

"""
select * from _user_gallery where _user=1 and _path like '/avignon/%';

mydatabase=# select id,_path from _user_gallery where _user=1 and _path like '/avignon/%';
  id  |      _path       
------+------------------
    3 | /avignon/
  128 | /avignon/dama/
    1 | /avignon/1/
 1035 | /avignon/1/1035/
(4 rows)


# there is no direct function in postgresql to count the occurrence 
# of a charcater
# but this trick works:
# select id,_path, length(_path)-length(replace(_path,'/','')) as len from  _user_gallery where _user=1;
select id,_path, length(_path)-length(replace(_path,'/','')) as len from  _user_gallery;


"""




print("""
-- add a new column
ALTER TABLE _user_gallery ADD COLUMN _depth integer;

-- set the depth as the number of slashes
UPDATE _user_gallery SET _depth=length(_path)-length(replace(_path,'/',''));
""")


"""
mydatabase=#  select id,_depth,_path from _user_gallery where _user=1 and _path like '/avignon/%' and _depth>2 order by _depth;
  id  | _depth |      _path       
------+--------+------------------
    1 |      3 | /avignon/1/
  128 |      3 | /avignon/dama/
 1035 |      4 | /avignon/1/1035/
(3 rows)


"""
