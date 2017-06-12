# http://beyondrelational.com/modules/2/blogs/80/posts/10750/day-8-stringtoarray-function-in-postgresql.aspx

# for virtual directories, maybe the best timestamp to have is to set to now()

SELECT id,_path from _user_gallery where _user=1;
SELECT id,string_to_array(_path,'/') from _user_gallery where _user=1;
SELECT id,unnest(string_to_array(_path,'/')) from _user_gallery where _user=1;

SELECT id, generate_subscripts(string_to_array(_path,'/'), 1) AS s, _path FROM _user_gallery where _user=1;


WITH
a1 AS (SELECT id,string_to_array(_path,'/') as pathar, _path FROM _user_gallery where _user=1),
a2 AS (SELECT id, generate_subscripts(pathar, 1) as pos, _path,pathar FROM a1),
a3 AS  (SELECT id, _path, pos,pathar[pos] as diratpos, array_to_string(pathar[1:pos],'/') as subpath,  array_to_string(pathar[1:pos-1],'/') as subpathshort, array_length(pathar, 1) as length FROM a2)
SELECT DISTINCT ON (diratpos) * FROM a3 
WHERE subpathshort='avignon' ORDER BY diratpos,length;

