#!/usr/bin/python3
from atpic.mybytes import *


full=[]

"""
Extracts the model currently used in SQL

"""

"""
SELECT n.nspname as "Schema",
	  c.relname as "Name",
	  CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' END as "Type",
	  pg_catalog.pg_get_userbyid(c.relowner) as "Owner"
	FROM pg_catalog.pg_class c
	     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
	WHERE c.relkind IN ('r','')
	      AND n.nspname <> 'pg_catalog'
	      AND n.nspname <> 'information_schema'
	      AND n.nspname !~ '^pg_toast'
	  AND pg_catalog.pg_table_is_visible(c.oid)
	ORDER BY 1,2;





                     List of relations
 Schema |             Name              | Type  |   Owner   
--------+-------------------------------+-------+-----------
 public | _testtable                    | table | alexmadon
 public | _translate                    | table | alexmadon
 public | _user                         | table | alexmadon
 public | _user_comment                 | table | alexmadon
 public | _user_gallery                 | table | alexmadon
 public | _user_gallery_comment         | table | alexmadon
 public | _user_gallery_pic             | table | alexmadon
 public | _user_gallery_pic_comment     | table | alexmadon
 public | _user_gallery_pic_tag         | table | alexmadon
 public | _user_gallery_pic_vote        | table | alexmadon
 public | _user_gallery_tag             | table | alexmadon
 public | _user_tag                     | table | alexmadon
 public | artist_css                    | table | alexmadon
 public | artist_du                     | table | alexmadon



\d _user 








=========================================================

makes several queries:




2011-09-05 18:00:53 BST LOG:  duration: 3.176 ms  statement: 


SELECT c.oid,
	  n.nspname,
	  c.relname
	FROM pg_catalog.pg_class c
	     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
	WHERE c.relname ~ '^(_user)$'
	  AND pg_catalog.pg_table_is_visible(c.oid)
	ORDER BY 2, 3;






2011-09-05 18:00:53 BST LOG:  duration: 99.674 ms  statement: 



SELECT c.relchecks, c.relkind, c.relhasindex, c.relhasrules, c.relhastriggers, c.relhasoids, '', c.reltablespace, CASE WHEN c.reloftype = 0 THEN '' ELSE c.reloftype::pg_catalog.regtype::pg_catalog.text END
	FROM pg_catalog.pg_class c
	 LEFT JOIN pg_catalog.pg_class tc ON (c.reltoastrelid = tc.oid)
	WHERE c.oid = '16460'
	







2011-09-05 18:00:53 BST LOG:  duration: 60.076 ms  statement: 


--- attributes

SELECT a.attname,
	  pg_catalog.format_type(a.atttypid, a.atttypmod),
	  (SELECT substring(pg_catalog.pg_get_expr(d.adbin, d.adrelid) for 128)
	   FROM pg_catalog.pg_attrdef d
	   WHERE d.adrelid = a.attrelid AND d.adnum = a.attnum AND a.atthasdef),
	  a.attnotnull, a.attnum
	FROM pg_catalog.pg_attribute a
	WHERE a.attrelid = '16460' AND a.attnum > 0 AND NOT a.attisdropped
	ORDER BY a.attnum










2011-09-05 18:00:53 BST LOG:  duration: 52.117 ms  statement: 

----indexes

SELECT c2.relname, i.indisprimary, i.indisunique, i.indisclustered, i.indisvalid, pg_catalog.pg_get_indexdef(i.indexrelid, 0, true),
	  pg_catalog.pg_get_constraintdef(con.oid, true), contype, condeferrable, condeferred, c2.reltablespace
	FROM pg_catalog.pg_class c, pg_catalog.pg_class c2, pg_catalog.pg_index i
	  LEFT JOIN pg_catalog.pg_constraint con ON (conrelid = i.indrelid AND conindid = i.indexrelid AND contype IN ('p','u','x'))
	WHERE c.oid = '16460' AND c.oid = i.indrelid AND i.indexrelid = c2.oid
	ORDER BY i.indisprimary DESC, i.indisunique DESC, c2.relname










2011-09-05 18:00:53 BST LOG:  duration: 1.466 ms  statement: 


--- constraints

SELECT conname,
	  pg_catalog.pg_get_constraintdef(r.oid, true) as condef
	FROM pg_catalog.pg_constraint r
	WHERE r.conrelid = '16460' AND r.contype = 'f' ORDER BY 1

2011-09-05 18:00:53 BST LOG:  duration: 31.045 ms  statement: 

SELECT conname, conrelid::pg_catalog.regclass,
	  pg_catalog.pg_get_constraintdef(c.oid, true) as condef
	FROM pg_catalog.pg_constraint c
	WHERE c.confrelid = '16460' AND c.contype = 'f' ORDER BY 1








2011-09-05 18:00:53 BST LOG:  duration: 15.067 ms  statement: SELECT t.tgname, pg_catalog.pg_get_triggerdef(t.oid, true), t.tgenabled
	FROM pg_catalog.pg_trigger t
	WHERE t.tgrelid = '16460' AND NOT t.tgisinternal
	ORDER BY 1





2011-09-05 18:00:53 BST LOG:  duration: 10.084 ms  statement: SELECT c.oid::pg_catalog.regclass FROM pg_catalog.pg_class c, pg_catalog.pg_inherits i WHERE c.oid=i.inhparent AND i.inhrelid = '16460' ORDER BY inhseqno






2011-09-05 18:00:53 BST LOG:  duration: 9.366 ms  statement: SELECT c.oid::pg_catalog.regclass FROM pg_catalog.pg_class c, pg_catalog.pg_inherits i WHERE c.oid=i.inhrelid AND i.inhparent = '16460' ORDER BY c.oid::pg_catalog.regclass::pg_catalog.text;




    Column     |            Type             |                           Modifiers                           
---------------+-----------------------------+---------------------------------------------------------------
 id            | integer                     | not null default nextval(('"artist_id_seq"'::text)::regclass)
 _login        | character varying(127)      | 
 _password     | character varying(127)      | 
 _servershort  | character varying(127)      | 
 _email        | character varying(127)      | 
 _size_allowed | integer                     | 
 _title        | text                        | 
 _text         | text                        | 
 _datefirst    | timestamp without time zone | 
 _datelast     | timestamp without time zone | 
 _counter      | integer                     | default 0
 _lang         | character(2)                | 
 _thestyleid   | integer                     | 
 _rows         | character varying(63)       | 




 _storefrom    | integer                     | 
 _storeto      | integer                     | 
 _synced       | integer                     | 
 _name         | character varying(127)      | 
Indexes:
    "artist_pkey" PRIMARY KEY, btree (id)
    "admin_loginunic" UNIQUE, btree (_login)
    "servershortunic" UNIQUE, btree (_servershort)
Referenced by:
    TABLE "artist_du" CONSTRAINT "artist_du_ref" FOREIGN KEY (refartist) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "_user_gallery" CONSTRAINT "artist_gallery_ref" FOREIGN KEY (_user) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "_user_comment" CONSTRAINT "forum_a_ref" FOREIGN KEY (_user) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "_user_tag" CONSTRAINT "tag_a_docid_ref" FOREIGN KEY (_user) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "_user_tag" CONSTRAINT "tag_a_tagger_ref" FOREIGN KEY (_tagger) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "_user_gallery_tag" CONSTRAINT "tag_g_tagger_ref" FOREIGN KEY (_tagger) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE "_user_gallery_pic_tag" CONSTRAINT "tag_p_tagger_ref" FOREIGN KEY (_tagger) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE
"""

import atpic.libpqalex
# import logging
import atpic.log
import re

# # logging.basicConfig(level=logging.DEBUG)
xx=atpic.log.setmod("INFO","model_extract_db2xml")



def get_constraints(oid,db):
    yy=atpic.log.setname(xx,'get_constraints')
    query=b"""
SELECT conname, conrelid::pg_catalog.regclass as relid,
	  pg_catalog.pg_get_constraintdef(c.oid, true) as condef
	FROM pg_catalog.pg_constraint c
	WHERE c.conrelid = '"""+oid+b"""' ORDER BY 1


""" 

    # 	WHERE c.conrelid = '%s' AND c.contype = 'f' ORDER BY 1

    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',())
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,'CONSTRAINTS ',result)
    for acons in result:
        atpic.log.debug(yy,'ACONS ',acons)
        full.append(b'<constraint name="'+acons[b'conname']+b'" condef="'+acons[b'condef']+b'"/>')


def get_indexes(oid,db):
    yy=atpic.log.setname(xx,'get_indexes')
    # get indexes

    query=b"""
SELECT c2.relname, i.indisprimary, i.indisunique, i.indisclustered, i.indisvalid, pg_catalog.pg_get_indexdef(i.indexrelid, 0, true) as indexdef,
	  pg_catalog.pg_get_constraintdef(con.oid, true) as constraintdef, contype, condeferrable, condeferred, c2.reltablespace
	FROM pg_catalog.pg_class c, pg_catalog.pg_class c2, pg_catalog.pg_index i
	  LEFT JOIN pg_catalog.pg_constraint con ON (conrelid = i.indrelid AND conindid = i.indexrelid AND contype IN ('p','u','x'))
	WHERE c.oid = '"""+oid+b"""' AND c.oid = i.indrelid AND i.indexrelid = c2.oid
	ORDER BY i.indisprimary DESC, i.indisunique DESC, c2.relname

"""


    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',())
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,'INDEXES',result)
    for aindex in result:
        atpic.log.debug(yy,'AINDEX',aindex)
        if not aindex[b'constraintdef']:
            # this is a pure index (i.e. it does not come from a constraint)
            # full.append('<index relname="%s" indisprimary="%s" indisunique="%s" indexdef="%s" constraintdef="%s" contype="%s"/>' % (aindex['relname'],aindex['indisprimary'],aindex['indisunique'],aindex['indexdef'],aindex['constraintdef'],aindex['contype']))
            full.append(b'<index name="'+aindex[b'relname']+b'" indexdef="'+aindex[b'indexdef']+b'"/>')


def get_oid(name,db):
    yy=atpic.log.setname(xx,'get_oid')

    query=b"""
SELECT c.oid,
	  n.nspname,
	  c.relname
	FROM pg_catalog.pg_class c
	     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
	WHERE c.relname = '"""+name+b"""'
	  AND pg_catalog.pg_table_is_visible(c.oid)
	ORDER BY 2, 3;
""" 

    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',())
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,'oid',result)
    oid=result[0][b'oid']
    return oid

def get_attributes(oid,db):
    yy=atpic.log.setname(xx,'get_attributes')


    query=b"""
SELECT a.attname,
	  pg_catalog.format_type(a.atttypid, a.atttypmod) as atttype,
	  (SELECT substring(pg_catalog.pg_get_expr(d.adbin, d.adrelid) for 128)
	   FROM pg_catalog.pg_attrdef d
	   WHERE d.adrelid = a.attrelid AND d.adnum = a.attnum AND a.atthasdef) as attrel,
	  a.attnotnull, a.attnum,
	  a.attstorage, pg_catalog.col_description(a.attrelid, a.attnum) as comment
	FROM pg_catalog.pg_attribute a
	WHERE a.attrelid = '"""+oid+b"""' AND a.attnum > 0 AND NOT a.attisdropped
	ORDER BY a.attname
	
""" 	
    # ORDER BY a.attnum

    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',())
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,'AAA %s',result)
    seqs=b""
    for field in result:
        atpic.log.debug(yy,'afield',field)
        attrel=field[b'attrel']
        attrel=attrel.replace(b'"',b'')
        comment=field[b'comment']
        if comment:
            pass
        else:
            comment=b''
        full.append(b'<attribute name="'+field[b'attname']+b'" type="'+field[b'atttype']+b'" notnull="'+field[b'attnotnull']+b'" attrel="'+attrel+b'" '+comment+b'/>')
        # full.append('DESC',field['comment']) # this is inserted using the COMMENT command
        # this is a hack
        if re.match(b'nextval',attrel):
            atpic.log.debug(yy,'the is a sequence')
            # eg=nextval(('artist_gallery_id_seq'::text)::regclass)
            res=re.search(b"nextval\(\('([^']+)\'",attrel)
            # full.append('sequences %s' % dir(res))
            # full.append('sequences %s' % res.group(1))
            seqname=res.group(1)
            atpic.log.debug(yy,'seqname',seqname)
            atpic.log.debug(yy,'attname',field[b'attname'])
            seqs=seqs+b'<sequence name="'+seqname+b'" attname="'+field[b'attname']+b'"/>'


    full.append(seqs) # we append the sequences at the end to XSLT easily using following-sibling

def get_model():
    yy=atpic.log.setname(xx,'get_model')
    db=atpic.libpqalex.db_native()
    query=b"""
SELECT n.nspname as "Schema",
	  c.relname as "Name",
	  CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' END as "Type",
	  pg_catalog.pg_get_userbyid(c.relowner) as "Owner"
	FROM pg_catalog.pg_class c
	     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
	WHERE c.relkind IN ('r','')
	      AND n.nspname <> 'pg_catalog'
	      AND n.nspname <> 'information_schema'
	      AND n.nspname !~ '^pg_toast'
	  AND pg_catalog.pg_table_is_visible(c.oid)
	ORDER BY 1,2;
"""
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',())
    result=atpic.libpqalex.process_result(result)

    atpic.log.debug(yy,'CCC',result)
    full.append(b"<model>")
    for row in result:
        atpic.log.debug(yy,'row',row)
        name=row[b"Name"]
        if name[:1]==b'_':
            atpic.log.debug(yy,'Ok')
            full.append(b'<table name="'+name+b'">')
            oid=get_oid(name,db)
            get_attributes(oid,db)
            get_indexes(oid,db)
            get_constraints(oid,db)
            full.append(b"</table>")
    full.append(b"</model>")

if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    get_model()
    print(b'\n'.join(full).decode('utf8'))
