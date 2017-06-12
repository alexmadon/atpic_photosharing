#!/usr/bin/python3
print("""
UPDATE _user_gallery SET _file = NULL where _file='';

-- necessary to make the one below work:
-- SELECT id,_file,_dir,_isroot,coalesce(_file,id::text) FROM _user_gallery WHERE _user=1 AND _isroot='n';

""")
