#!/usr/bin/python3
import unittest
import atpic.xplo
import atpic.forgesql



def helper_sql(query,query_args):
    # create table _testtable (id int,description text,title text);
    db=atpic.libpqalex.db()
    ps=atpic.libpqalex.pq_prepare(db,b"ps",query)
    result=atpic.libpqalex.pq_exec_prepared(db,b"ps",query_args) # query_args is a list
    result=atpic.libpqalex.process_result(result)

    print("SQLRES",result)
    # print(dir(result))
    # print(type(result))
    db.close()


class forgesql_test(unittest.TestCase):
    def test_forge_query(self):
        lists=(

([(b'user', None)],[b'get'],1,b'en',[],b'0',b'from',b'+',b'',b'(WITH select4 AS (SELECT _user.* FROM _user WHERE _user.id<$1 AND _deleted=0 ORDER BY _user.id DESC LIMIT 1) SELECT * FROM select4 ORDER BY id ASC) UNION (WITH select4 AS (SELECT _user.* FROM _user WHERE _user.id>$2 AND _deleted=0 ORDER BY _user.id ASC LIMIT 11) SELECT * FROM select4 ORDER BY id ASC) ORDER BY id ASC',[b'1', b'0']),
([(b'user', None)],[b'get'],1,b'en',[],b'20',b'from',b'+',b'',b'(WITH select4 AS (SELECT _user.* FROM _user WHERE _user.id<$1 AND _deleted=0 ORDER BY _user.id DESC LIMIT 1) SELECT * FROM select4 ORDER BY id ASC) UNION (WITH select4 AS (SELECT _user.* FROM _user WHERE _user.id>$2 AND _deleted=0 ORDER BY _user.id ASC LIMIT 11) SELECT * FROM select4 ORDER BY id ASC) ORDER BY id ASC',[b'21', b'20']),
([(b'user', None)],[b'post'],1,b'en',[(b'age', False, b'222'), (b'name', False, b'alex')],b'0',b'from',b'+',b'',b"WITH select1 AS (INSERT INTO _user (_age,_name) VALUES ($1,$2) RETURNING *), select2 AS (INSERT INTO _user_gallery (_user,_path) SELECT select1.id,'' FROM select1) SELECT * FROM select1",[b'222', b'alex']),
([(b'user', b'111')],[b'get'],1,b'en',[],b'0',b'from',b'+',b'',b'WITH select4 AS (SELECT _user.* FROM _user WHERE _user.id=$1 AND _deleted=0) SELECT * FROM select4 ORDER BY id ASC',[b'111']),
([(b'user', b'111'), (b'gallery', b'222'), (b'pic', None)],[b'get'],2,b'en',[],b'0',b'from',b'+',b'',b"WITH select1 AS (SELECT _partition FROM _user WHERE id=$1 AND _deleted=0), select2 AS (SELECT $2::int AS id), select3 AS (SELECT _gallery,min(id) AS _pic FROM _user_gallery_pic WHERE _user=$3 AND _deleted=0 AND _gallery IN (SELECT id FROM select2) GROUP BY _gallery), select5 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$4 AND _pic IN (SELECT _pic FROM select3) GROUP BY _pic), select6 AS (SELECT select3._gallery,select5._artefact FROM select3 JOIN select5 ON select5._pic=select3._pic), select4 AS (SELECT _user_gallery.* FROM _user_gallery WHERE _user_gallery._user=$5 AND _user_gallery.id=$6 AND _deleted=0) SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select6 ON select6._gallery=select4.id ORDER BY id ASC",[b'111', b'222', b'111', b'111', b'111', b'222']),
([(b'user', b'111'), (b'gallery', b'222'), (b'pic', None)],[b'get'],2,b'en',[],b'20',b'from',b'+',b'',b"WITH select1 AS (SELECT _partition FROM _user WHERE id=$1 AND _deleted=0), select2 AS (SELECT $2::int AS id), select3 AS (SELECT _gallery,min(id) AS _pic FROM _user_gallery_pic WHERE _user=$3 AND _deleted=0 AND _gallery IN (SELECT id FROM select2) GROUP BY _gallery), select5 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$4 AND _pic IN (SELECT _pic FROM select3) GROUP BY _pic), select6 AS (SELECT select3._gallery,select5._artefact FROM select3 JOIN select5 ON select5._pic=select3._pic), select4 AS (SELECT _user_gallery.* FROM _user_gallery WHERE _user_gallery._user=$5 AND _user_gallery.id=$6 AND _deleted=0) SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select6 ON select6._gallery=select4.id ORDER BY id ASC",[b'111', b'222', b'111', b'111', b'111', b'222']),
([(b'user', b'111'), (b'gallery', b'222'), (b'pic', None)],[b'get'],3,b'en',[],b'0',b'from',b'+',b'',b"(WITH select1 AS (SELECT _partition FROM _user WHERE id=$1 AND _deleted=0), select2 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$2 AND _pic IN (SELECT id FROM _user_gallery_pic WHERE _gallery=$3 AND id<$4 AND _deleted=0 ORDER BY id DESC LIMIT 1) GROUP BY _pic), select4 AS (SELECT _user_gallery_pic.* FROM _user_gallery_pic WHERE _user_gallery_pic._user=$5 AND _user_gallery_pic._gallery=$6 AND _user_gallery_pic.id<$7 AND _deleted=0 ORDER BY _user_gallery_pic.id DESC LIMIT 1) SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select2 ON select2._pic=select4.id ORDER BY id ASC) UNION (WITH select1 AS (SELECT _partition FROM _user WHERE id=$8 AND _deleted=0), select2 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$9 AND _pic IN (SELECT id FROM _user_gallery_pic WHERE _gallery=$10 AND id>$11 AND _deleted=0 ORDER BY id ASC LIMIT 11) GROUP BY _pic), select4 AS (SELECT _user_gallery_pic.* FROM _user_gallery_pic WHERE _user_gallery_pic._user=$12 AND _user_gallery_pic._gallery=$13 AND _user_gallery_pic.id>$14 AND _deleted=0 ORDER BY _user_gallery_pic.id ASC LIMIT 11) SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select2 ON select2._pic=select4.id ORDER BY id ASC) ORDER BY id ASC",[b'111', b'111', b'222', b'1', b'111', b'222', b'1', b'111', b'111', b'222', b'0', b'111', b'222', b'0']),
([(b'user', b'111'), (b'gallery', b'222'), (b'pic', None)],[b'get'],3,b'en',[],b'20',b'from',b'+',b'',b"(WITH select1 AS (SELECT _partition FROM _user WHERE id=$1 AND _deleted=0), select2 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$2 AND _pic IN (SELECT id FROM _user_gallery_pic WHERE _gallery=$3 AND id<$4 AND _deleted=0 ORDER BY id DESC LIMIT 1) GROUP BY _pic), select4 AS (SELECT _user_gallery_pic.* FROM _user_gallery_pic WHERE _user_gallery_pic._user=$5 AND _user_gallery_pic._gallery=$6 AND _user_gallery_pic.id<$7 AND _deleted=0 ORDER BY _user_gallery_pic.id DESC LIMIT 1) SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select2 ON select2._pic=select4.id ORDER BY id ASC) UNION (WITH select1 AS (SELECT _partition FROM _user WHERE id=$8 AND _deleted=0), select2 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$9 AND _pic IN (SELECT id FROM _user_gallery_pic WHERE _gallery=$10 AND id>$11 AND _deleted=0 ORDER BY id ASC LIMIT 11) GROUP BY _pic), select4 AS (SELECT _user_gallery_pic.* FROM _user_gallery_pic WHERE _user_gallery_pic._user=$12 AND _user_gallery_pic._gallery=$13 AND _user_gallery_pic.id>$14 AND _deleted=0 ORDER BY _user_gallery_pic.id ASC LIMIT 11) SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select2 ON select2._pic=select4.id ORDER BY id ASC) ORDER BY id ASC",[b'111', b'111', b'222', b'21', b'111', b'222', b'21', b'111', b'111', b'222', b'20', b'111', b'222', b'20']),
([(b'user', b'111'), (b'gallery', b'222'), (b'pic', b'333')],[b'get'],1,b'en',[],b'0',b'from',b'+',b'',b'WITH select4 AS (SELECT _user.* FROM _user WHERE _user.id=$1 AND _deleted=0) SELECT * FROM select4 ORDER BY id ASC',[b'111']),
([(b'user', b'111'), (b'gallery', b'222'), (b'pic', b'333')],[b'get'],2,b'en',[],b'0',b'from',b'+',b'',b"WITH select1 AS (SELECT _partition FROM _user WHERE id=$1 AND _deleted=0), select2 AS (SELECT $2::int AS id), select3 AS (SELECT _gallery,min(id) AS _pic FROM _user_gallery_pic WHERE _user=$3 AND _deleted=0 AND _gallery IN (SELECT id FROM select2) GROUP BY _gallery), select5 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$4 AND _pic IN (SELECT _pic FROM select3) GROUP BY _pic), select6 AS (SELECT select3._gallery,select5._artefact FROM select3 JOIN select5 ON select5._pic=select3._pic), select4 AS (SELECT _user_gallery.* FROM _user_gallery WHERE _user_gallery._user=$5 AND _user_gallery.id=$6 AND _deleted=0) SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select6 ON select6._gallery=select4.id ORDER BY id ASC",[b'111', b'222', b'111', b'111', b'111', b'222']),
([(b'user', b'111'), (b'gallery', b'222'), (b'pic', b'333')],[b'get'],3,b'en',[],b'0',b'from',b'+',b'',b"WITH select1 AS (SELECT _partition FROM _user WHERE id=$1 AND _deleted=0), select2 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$2 AND _pic=$3 GROUP BY _pic), select4 AS (SELECT _user_gallery_pic.* FROM _user_gallery_pic WHERE _user_gallery_pic._user=$4 AND _user_gallery_pic._gallery=$5 AND _user_gallery_pic.id=$6 AND _deleted=0) SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select2 ON select2._pic=select4.id ORDER BY id ASC",[b'111', b'111', b'333', b'111', b'222', b'333']),
([(b'user', b'111')],[b'delete'],1,b'en',[],b'0',b'from',b'+',b'',b'WITH select1 AS (UPDATE _user SET _deleted=_deleted+1 WHERE _deleted>0), select2 AS (UPDATE _user SET _deleted=_deleted+1, _datelast=now() WHERE id=$1 RETURNING *) SELECT * FROM select2',[b'111']),
([(b'user', b'111'), (b'gallery', b'222')],[b'delete'],2,b'en',[],b'0',b'from',b'+',b'',b'WITH select1 AS (UPDATE _user_gallery SET _deleted=_deleted+1 WHERE _deleted>0 AND _user=$1), select2 AS (UPDATE _user_gallery SET _deleted=_deleted+1, _datelast=now() WHERE id=$2 AND _user=$3 RETURNING *) SELECT * FROM select2',[b'222', b'111', b'111']),
([(b'user', b'111'), (b'gallery', b'222'), (b'pic', b'333')],[b'delete'],3,b'en',[],b'0',b'from',b'+',b'',b'WITH select1 AS (UPDATE _user_gallery_pic SET _deleted=_deleted+1 WHERE _deleted>0 AND _user=$1), select2 AS (UPDATE _user_gallery_pic SET _deleted=_deleted+1, _datelast=now() WHERE id=$2 AND _user=$3 RETURNING *) SELECT * FROM select2',[b'333', b'111', b'111']),
([(b'user', b'111'), (b'gallery', None)],[b'get', b'post'],2,b'en',[],b'0',b'from',b'+',b'',b'SELECT original_query.* FROM (SELECT * FROM _user_gallery WHERE _user<-10 AND id<0 LIMIT 1 ) AS original_query RIGHT JOIN (SELECT 1) AS one_row ON true',[]),
([(b'news', None)],[b'post'],1,b'en',[],b'0',b'from',b'+',b'',b'INSERT INTO _news DEFAULT VALUES RETURNING *',[]),
([(b'user', b'1'), (b'gallery', None)],[b'post'],2,b'en',[],b'0',b'from',b'+',b'',b'INSERT INTO _user_gallery (_user) VALUES ($1) RETURNING *',[b'1']),
([(b'user', b'1'), (b'gallery', None)],[b'post', b'post'],2,b'en',[(b'title', False, b'tess')],b'0',b'from',b'+',b'',b'INSERT INTO _user_gallery (_user,_title) VALUES ($1,$2) RETURNING *',[b'1', b'tess']),
([(b'user', b'111'), (b'gallery', b'222'), (b'pic', None)],[b'post'],3,b'en',[(b'userfile', True, (b'/tmp/atup38bec3', b'myname.jpg', b'image/jpeg'))],b'0',b'from',b'+',b'',b'INSERT INTO _user_gallery_pic (_user,_gallery,_originalname) VALUES ($1,$2,$3) RETURNING *',[b'111', b'222', b'myname.jpg']),
([(b'user', b'1'), (b'gallery', b'99')],[b'get', b'put'],2,b'en',[],b'0',b'from',b'+',b'',b"WITH select1 AS (SELECT _partition FROM _user WHERE id=$1 AND _deleted=0), select2 AS (SELECT $2::int AS id), select3 AS (SELECT _gallery,min(id) AS _pic FROM _user_gallery_pic WHERE _user=$3 AND _deleted=0 AND _gallery IN (SELECT id FROM select2) GROUP BY _gallery), select5 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$4 AND _pic IN (SELECT _pic FROM select3) GROUP BY _pic), select6 AS (SELECT select3._gallery,select5._artefact FROM select3 JOIN select5 ON select5._pic=select3._pic), select4 AS (SELECT _user_gallery.* FROM _user_gallery WHERE _user_gallery._user=$5 AND _user_gallery.id=$6 AND _deleted=0) SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select6 ON select6._gallery=select4.id ORDER BY id ASC",[b'1', b'99', b'1', b'1', b'1', b'99']),
([(b'user', b'1'), (b'gallery', b'99'), (b'pic', b'888')],[b'post', b'put'],3,b'en',[(b'text', False, b'this is a Pittospore'), (b'title', False, b'Pittospore')],b'0',b'from',b'+',b'',b'UPDATE _user_gallery_pic SET _text=$1,_title=$2 WHERE _user=$3 AND id=$4 AND _deleted=0 RETURNING *',[b'this is a Pittospore', b'Pittospore', b'1', b'888']),
([(b'user', b'1'), (b'gallery', b'1'), (b'pic', None)],[b'get', b'post'],3,b'en',[],b'0',b'from',b'+',b'',b'SELECT original_query.* FROM (SELECT * FROM _user_gallery_pic WHERE _user<-10 AND id<0 LIMIT 1 ) AS original_query RIGHT JOIN (SELECT 1) AS one_row ON true',[]),
([(b'user', b'1'), (b'gallery', b'99'), (b'pic', b'888'), (b'tag', None)],[b'get'],4,b'en',[],b'0',b'from',b'+',b'',b'(WITH select4 AS (SELECT _user_gallery_pic_tag.* FROM _user_gallery_pic_tag WHERE _user_gallery_pic_tag._user=$1 AND _user_gallery_pic_tag._pic=$2 AND _user_gallery_pic_tag.id<$3 ORDER BY _user_gallery_pic_tag.id DESC LIMIT 1) SELECT * FROM select4 ORDER BY id ASC) UNION (WITH select4 AS (SELECT _user_gallery_pic_tag.* FROM _user_gallery_pic_tag WHERE _user_gallery_pic_tag._user=$4 AND _user_gallery_pic_tag._pic=$5 AND _user_gallery_pic_tag.id>$6 ORDER BY _user_gallery_pic_tag.id ASC LIMIT 11) SELECT * FROM select4 ORDER BY id ASC) ORDER BY id ASC',[b'1', b'888', b'1', b'1', b'888', b'0']),
([(b'user', b'1'), (b'gallery', b'99'), (b'pic', b'888'), (b'tag', b'7777')],[b'post', b'put'],4,b'en',[(b'text', False, b'paris france')],b'0',b'from',b'+',b'',b'WITH upsert1 AS (UPDATE _user_gallery_pic_tag SET _text=$1, _datelast=now() WHERE _user=$2 AND id=$3 AND _pic=$4 RETURNING *), upsert2 AS (INSERT INTO _user_gallery_pic_tag (_user,id,_pic,_text,_datelast) SELECT $5,$6,$7,$8,now() WHERE NOT EXISTS (SELECT 1 FROM upsert1) RETURNING *) SELECT * FROM upsert1 UNION SELECT * FROM upsert2',[b'paris france', b'1', b'7777', b'888', b'1', b'7777', b'888', b'paris france']),
([(b'user', b'1'), (b'gallery', b'99'), (b'pic', b'888'), (b'vote', b'7777')],[b'post', b'put'],4,b'en',[(b'score', False, b'4')],b'0',b'from',b'+',b'',b'WITH upsert1 AS (UPDATE _user_gallery_pic_vote SET _score=$1, _datelast=now() WHERE _user=$2 AND id=$3 AND _pic=$4 RETURNING *), upsert2 AS (INSERT INTO _user_gallery_pic_vote (_user,id,_pic,_score,_datelast) SELECT $5,$6,$7,$8,now() WHERE NOT EXISTS (SELECT 1 FROM upsert1) RETURNING *) SELECT * FROM upsert1 UNION SELECT * FROM upsert2',[b'4', b'1', b'7777', b'888', b'1', b'7777', b'888', b'4']),
([(b'user', b'1'), (b'gallery', b'22'), (b'tag', b'333')],[b'get', b'put'],3,b'en',[],b'0',b'from',b'+',b'',b'WITH select4 AS (SELECT _user_gallery_tag.* FROM _user_gallery_tag WHERE _user_gallery_tag._user=$1 AND _user_gallery_tag._gallery=$2 AND _user_gallery_tag.id=$3) SELECT * FROM select4 ORDER BY id ASC',[b'1', b'22', b'333']),
([(b'user', b'1'), (b'gallery', b'1'), (b'tag', b'1')],[b'get'],1,b'en',[],b'0',b'from',b'+',b'',b'WITH select4 AS (SELECT _user.* FROM _user WHERE _user.id=$1 AND _deleted=0) SELECT * FROM select4 ORDER BY id ASC',[b'1']),
([(b'user', b'1'), (b'gallery', b'22'), (b'pic', b'333'), (b'tag', None)],[b'get', b'post'],4,b'en',[],b'0',b'from',b'+',b'6969',b'WITH row AS (SELECT * FROM _user_gallery_pic_tag WHERE _user=$1 AND _pic=$2 AND id=$3), one AS (SELECT 1 AS uno) SELECT row.* FROM row RIGHT JOIN one ON true',[b'1', b'333', b'6969']),
([(b'user', b'1'), (b'gallery', b'22'), (b'pic', b'333'), (b'tag', b'6969')],[b'post', b'post'],4,b'en',[(b'text', False, b'pittospore2')],b'0',b'from',b'+',b'6969',b'WITH upsert1 AS (UPDATE _user_gallery_pic_tag SET _text=$1, _datelast=now() WHERE _user=$2 AND id=$3 AND _pic=$4 RETURNING *), upsert2 AS (INSERT INTO _user_gallery_pic_tag (_user,id,_pic,_text,_datelast) SELECT $5,$6,$7,$8,now() WHERE NOT EXISTS (SELECT 1 FROM upsert1) RETURNING *) SELECT * FROM upsert1 UNION SELECT * FROM upsert2',[b'pittospore2', b'1', b'6969', b'333', b'1', b'6969', b'333', b'pittospore2']),
([(b'user', b'2'), (b'pm', None)],[b'post', b'post'],2,b'en',[(b'text', False, b'text1'), (b'title', False, b'tit1')],b'0',b'from',b'+',b'1',b'WITH ins1 AS (INSERT INTO _user_pm (_from,_user,_text,_title) VALUES ($1,$2,$3,$4) RETURNING *), ins2 AS (INSERT INTO _user_pmsent (id,_to,_user,_text,_title) SELECT id, _user, _from,_text,_title FROM ins1 RETURNING *) SELECT * FROM ins1',[b'1', b'2', b'text1', b'tit1']),
([(b'user', b'1'), (b'friend', b'99')],[b'post', b'put'],2,b'en',[],b'0',b'from',b'+',b'',b'WITH upsert1 AS (UPDATE _user_friend SET _datelast=now() WHERE _user=$1 AND id=$2 RETURNING *), upsert2 AS (INSERT INTO _user_friend (_user,id,_datelast) SELECT $3,$4,now() WHERE NOT EXISTS (SELECT 1 FROM upsert1) RETURNING *) SELECT * FROM upsert1 UNION SELECT * FROM upsert2',[b'1', b'99', b'1', b'99']),
([(b'user', b'1'), (b'friend', b'99')],[b'post', b'put'],2,b'en',[],b'0',b'from',b'+',b'1',b'WITH upsert1 AS (UPDATE _user_friend SET _datelast=now() WHERE _user=$1 AND id=$2 RETURNING *), upsert2 AS (INSERT INTO _user_friend (_user,id,_datelast) SELECT $3,$4,now() WHERE NOT EXISTS (SELECT 1 FROM upsert1) RETURNING *) SELECT * FROM upsert1 UNION SELECT * FROM upsert2',[b'1', b'99', b'1', b'99']),
([(b'user', b'1'), (b'friend', b'99')],[b'post', b'post'],2,b'en',[(b'friend', False, b'99')],b'0',b'from',b'+',b'1',b'WITH upsert1 AS (UPDATE _user_friend SET _datelast=now() WHERE _user=$1 AND id=$2 RETURNING *), upsert2 AS (INSERT INTO _user_friend (_user,id,_datelast) SELECT $3,$4,now() WHERE NOT EXISTS (SELECT 1 FROM upsert1) RETURNING *) SELECT * FROM upsert1 UNION SELECT * FROM upsert2',[b'1', b'99', b'1', b'99']),
([(b'user', b'1'), (b'gallery', b'22'), (b'friend', b'3')],[b'post', b'post'],3,b'en',[(b'friend', False, b'3')],b'0',b'from',b'+',b'',b'WITH upsert1 AS (UPDATE _user_gallery_friend SET _datelast=now() WHERE _user=$1 AND id=$2 AND _gallery=$3 RETURNING *), upsert2 AS (INSERT INTO _user_gallery_friend (_user,id,_gallery,_datelast) SELECT $4,$5,$6,now() WHERE NOT EXISTS (SELECT 1 FROM upsert1) RETURNING *) SELECT * FROM upsert1 UNION SELECT * FROM upsert2',[b'1', b'3', b'22', b'1', b'3', b'22']),
([(b'user', b'1'), (b'gallery', b'1'), (b'pic', b'2'), (b'friend', b'88')],[b'post', b'post'],4,b'en',[(b'friend', False, b'88')],b'999',b'from',b'+',b'',b'WITH upsert1 AS (UPDATE _user_gallery_pic_friend SET _datelast=now() WHERE _user=$1 AND id=$2 AND _pic=$3 RETURNING *), upsert2 AS (INSERT INTO _user_gallery_pic_friend (_user,id,_pic,_datelast) SELECT $4,$5,$6,now() WHERE NOT EXISTS (SELECT 1 FROM upsert1) RETURNING *) SELECT * FROM upsert1 UNION SELECT * FROM upsert2',[b'1', b'88', b'2', b'1', b'88', b'2']),
([(b'user', b'1'), (b'wiki', b'/')],[b'get'],2,b'en',[],b'0',b'from',b'+',b'',b'WITH select1 AS ( SELECT * FROM _user_wiki WHERE _user=$1 AND _lang=$2 AND _path=$3 ORDER BY id DESC LIMIT $4 ), one AS (SELECT 1 AS uno) SELECT select1.* FROM select1',[b'1', b'en', b'_', b'1']),
([(b'user', b'1'), (b'wiki', b'/')],[b'get'],1,b'en',[],b'0',b'from',b'+',b'',b'WITH select4 AS (SELECT _user.* FROM _user WHERE _user.id=$1 AND _deleted=0) SELECT * FROM select4 ORDER BY id ASC',[b'1']),
([(b'wiki', b'/')],[b'post', b'post'],1,b'en',[(b'wikitext', False, b'some wiki')],b'0',b'from',b'+',b'',b'WITH select1 AS (SELECT * FROM _wiki WHERE _path=$1 AND _lang=$2 ORDER BY id DESC LIMIT 1), select2 AS (SELECT * FROM select1 WHERE _wikitext=$3 AND _lang=$4), select3 AS (INSERT INTO _wiki (_path,_wikitext,_lang,_message,_datepublished) SELECT $5,$6,$7,$8,now() WHERE NOT EXISTS (SELECT 1 FROM select2)      RETURNING *) SELECT * FROM select2 UNION SELECT * FROM select3',[b'_', b'en', b'some wiki', b'en', b'_', b'some wiki', b'en', b'']),
([(b'user', b'1'), (b'gallery', b'7699'), (b'pic', b'291708'), (b'tag', None)],[b'get'],3,b'en',[],b'0',b'from',b'+',b'',b"WITH select1 AS (SELECT _partition FROM _user WHERE id=$1 AND _deleted=0), select2 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$2 AND _pic=$3 GROUP BY _pic), select4 AS (SELECT _user_gallery_pic.* FROM _user_gallery_pic WHERE _user_gallery_pic._user=$4 AND _user_gallery_pic.id=$5 AND _deleted=0) SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select2 ON select2._pic=select4.id ORDER BY id ASC",[b'1', b'1', b'291708', b'1', b'291708']),
([(b'user', b'1'), (b'gallery', b'7699'), (b'pic', b'291708'), (b'tag', None)],[b'get'],4,b'en',[],b'0',b'from',b'+',b'',b'(WITH select4 AS (SELECT _user_gallery_pic_tag.* FROM _user_gallery_pic_tag WHERE _user_gallery_pic_tag._user=$1 AND _user_gallery_pic_tag._pic=$2 AND _user_gallery_pic_tag.id<$3 ORDER BY _user_gallery_pic_tag.id DESC LIMIT 1) SELECT * FROM select4 ORDER BY id ASC) UNION (WITH select4 AS (SELECT _user_gallery_pic_tag.* FROM _user_gallery_pic_tag WHERE _user_gallery_pic_tag._user=$4 AND _user_gallery_pic_tag._pic=$5 AND _user_gallery_pic_tag.id>$6 ORDER BY _user_gallery_pic_tag.id ASC LIMIT 11) SELECT * FROM select4 ORDER BY id ASC) ORDER BY id ASC',[b'1', b'291708', b'1', b'1', b'291708', b'0']),
([(b'user', b'1')],[b'post', b'put'],1,b'en',[(b'login', False, b'alexmadon'), (b'password', False, b'mypass'), (b'email', False, b'alex@example.foo')],b'0',b'from',b'+',b'1',b'UPDATE _user SET _email=$1,_login=$2,_password=$3 WHERE id=$4 AND _deleted=0 RETURNING *',[b'alex@example.foo', b'alexmadon', b'mypass', b'1']),



            )

        i=0
        for alist,actions,depth,lang,indata,start,fromto,direction,authid,expect_query,expect_query_args in lists:
        # for alist,actions,depth,indata,start,expect_query,expect_query_args in lists:
            # lang=b'en'
            # fromto=b'from'
            # direction=b'+'
            # authid=b''

            i=i+1
            
            print("+++++++++++++++++++++ test %s ++++++++++++++++++++++++" % i)
            print('direction',direction)
            print('authid',authid)
            pxplo=atpic.xplo.Xplo(alist)
            environ={}
            (query,query_args)=atpic.forgesql.forge_query(pxplo,actions,depth,lang,environ,indata=indata,start=start,fromto=fromto,direction=direction,authid=authid)
            

            print("XXXX(",alist,",",actions,",",depth,",",lang,",",indata,",",start,",",fromto,",",direction,",",authid,",",query,",",query_args,"),",sep="")
            self.assertEqual(query,expect_query)
            self.assertEqual(query_args,expect_query_args)


    def test_transform(self): 
        lists=(
            (b"one $%s two $%s",[b'11',b'22']),
            (b"one $, two $,",[b'11',b'22']),
           )
        i=0
        for (query,query_args) in lists:
            i=i+1
            print("+++++++++++++++++++++ transform test %s ++++++++++++++++++++++++" % i)
            (query_r,query_args_r)=atpic.forgesql.transform(query,query_args)
            print(query_r,query_args_r)
         





    def NOtest_forge_insert(self):
        inserts=(
            [(b"title", False, b"alex"),(b"description", False, b"madon")],
            [(b"title", False, b"a title"),(b"description", False, b"a longer text")],
            [(b"title", False, "cet été là".encode('utf8')),(b"description", False, "电子图书与".encode('utf8'))],

            )
        i=0
        for insert in inserts:
            i=i+1
            print("+++++++++++++++++++++ insert test %s ++++++++++++++++++++++++" % i)
            (query,query_args)=atpic.forgesql.forge_insert(None,b"_testtable",insert)
            print(query,query_args)
            # helper_sql(query,query_args)

    def NOtest_forge_update(self):
        inserts=(
            ([(b"title", False, "alex"),(b"description", False, "madon")],1),
            ([(b"title", False, "a title"),(b"description", False, "a longer text")],99),
            ([(b"title", False, "cet été là".encode('utf8')),(b"description", False, "电子图书与".encode('utf8'))],199),

            )
        i=0
        for (insert,id) in inserts:
            i=i+1
            print("+++++++++++++++++++++ update test %s ++++++++++++++++++++++++" % i)
            (query,query_args)=atpic.forgesql.forge_update(b"_testtable",insert,id)
            print(query,query_args)

    def NOtest_forge_delete(self):
        inserts=(
            99,
            )
        i=0
        for id in inserts:
            i=i+1
            print("+++++++++++++++++++++ DELETE test %s ++++++++++++++++++++++++" % i)

            (query,query_args)=atpic.forgesql.forge_delete(b"_testtable",id)
            print(query,query_args)

 
    def NOtest_update(self):
        query=b"UPDATE test2 set i=8 WHERE i NOT IN (1,2) RETURNING i"
        query_args=[]
        helper_sql(query,query_args)

        query=b"INSERT INTO test2 (i) values(2) RETURNING i"
        helper_sql(query,query_args)


    def test_pathbased_dirlist(self):
        paths=[
( b'alex' , b"WITH select1 AS (SELECT _path FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._deleted=0 AND _user_gallery._path ~ $2), select2 AS (SELECT string_to_array(_path,'/') as pathar FROM select1), select3 AS (SELECT pathar[$3] as dirname FROM select2) SELECT DISTINCT ON (dirname) dirname FROM select3 ORDER by dirname" , [b'alex', b'.+', b'1'] ),
( b'alex/italia2006' , b"WITH select1 AS (SELECT _path FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._deleted=0 AND _user_gallery._path ~ $2), select2 AS (SELECT string_to_array(_path,'/') as pathar FROM select1), select3 AS (SELECT pathar[$3] as dirname FROM select2) SELECT DISTINCT ON (dirname) dirname FROM select3 ORDER by dirname" , [b'alex', b'^italia2006/.+$', b'2'] ),
( b'alex/italia2006/firenze' , b"WITH select1 AS (SELECT _path FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._deleted=0 AND _user_gallery._path ~ $2), select2 AS (SELECT string_to_array(_path,'/') as pathar FROM select1), select3 AS (SELECT pathar[$3] as dirname FROM select2) SELECT DISTINCT ON (dirname) dirname FROM select3 ORDER by dirname" , [b'alex', b'^italia2006/firenze/.+$', b'3'] ),
( b'/alex' , b"WITH select1 AS (SELECT _path FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._deleted=0 AND _user_gallery._path ~ $2), select2 AS (SELECT string_to_array(_path,'/') as pathar FROM select1), select3 AS (SELECT pathar[$3] as dirname FROM select2) SELECT DISTINCT ON (dirname) dirname FROM select3 ORDER by dirname" , [b'alex', b'.+', b'1'] ),
( b'/alex/italia2006' , b"WITH select1 AS (SELECT _path FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._deleted=0 AND _user_gallery._path ~ $2), select2 AS (SELECT string_to_array(_path,'/') as pathar FROM select1), select3 AS (SELECT pathar[$3] as dirname FROM select2) SELECT DISTINCT ON (dirname) dirname FROM select3 ORDER by dirname" , [b'alex', b'^italia2006/.+$', b'2'] ),
( b'/alex/italia2006/firenze' , b"WITH select1 AS (SELECT _path FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._deleted=0 AND _user_gallery._path ~ $2), select2 AS (SELECT string_to_array(_path,'/') as pathar FROM select1), select3 AS (SELECT pathar[$3] as dirname FROM select2) SELECT DISTINCT ON (dirname) dirname FROM select3 ORDER by dirname" , [b'alex', b'^italia2006/firenze/.+$', b'3'] ),
            ]
        for (path,query_ex,query_args_ex) in paths:
            (query,query_args)=atpic.forgesql.forge_dirlist(path)
            print('YYY (',path,',',query,',',query_args,'),')
            self.assertEqual(query,query_ex)
            self.assertEqual(query_args,query_args_ex)



    def test_pathbased_piclist(self):
        paths=[
( b'alex' , b"WITH select1 AS (SELECT _user._partition AS partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._path = $2 AND _user_gallery._deleted=0), select2 AS (SELECT _user_gallery_pic._originalname AS originalname, '/' || select1.partition ||'/'||_user_gallery_pic._pathstore as fullpathstore FROM _user_gallery_pic JOIN select1 ON select1.gid=_user_gallery_pic._gallery WHERE _user_gallery_pic._user=select1.uid AND _user_gallery_pic._deleted=0) SELECT * FROM select2 ORDER BY originalname" , [b'alex', b''] ),
( b'alex/italia2006' , b"WITH select1 AS (SELECT _user._partition AS partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._path = $2 AND _user_gallery._deleted=0), select2 AS (SELECT _user_gallery_pic._originalname AS originalname, '/' || select1.partition ||'/'||_user_gallery_pic._pathstore as fullpathstore FROM _user_gallery_pic JOIN select1 ON select1.gid=_user_gallery_pic._gallery WHERE _user_gallery_pic._user=select1.uid AND _user_gallery_pic._deleted=0) SELECT * FROM select2 ORDER BY originalname" , [b'alex', b'italia2006'] ),
( b'alex/italia2006/firenze' , b"WITH select1 AS (SELECT _user._partition AS partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._path = $2 AND _user_gallery._deleted=0), select2 AS (SELECT _user_gallery_pic._originalname AS originalname, '/' || select1.partition ||'/'||_user_gallery_pic._pathstore as fullpathstore FROM _user_gallery_pic JOIN select1 ON select1.gid=_user_gallery_pic._gallery WHERE _user_gallery_pic._user=select1.uid AND _user_gallery_pic._deleted=0) SELECT * FROM select2 ORDER BY originalname" , [b'alex', b'italia2006/firenze'] ),
( b'/alex' , b"WITH select1 AS (SELECT _user._partition AS partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._path = $2 AND _user_gallery._deleted=0), select2 AS (SELECT _user_gallery_pic._originalname AS originalname, '/' || select1.partition ||'/'||_user_gallery_pic._pathstore as fullpathstore FROM _user_gallery_pic JOIN select1 ON select1.gid=_user_gallery_pic._gallery WHERE _user_gallery_pic._user=select1.uid AND _user_gallery_pic._deleted=0) SELECT * FROM select2 ORDER BY originalname" , [b'alex', b''] ),
( b'/alex/italia2006' , b"WITH select1 AS (SELECT _user._partition AS partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._path = $2 AND _user_gallery._deleted=0), select2 AS (SELECT _user_gallery_pic._originalname AS originalname, '/' || select1.partition ||'/'||_user_gallery_pic._pathstore as fullpathstore FROM _user_gallery_pic JOIN select1 ON select1.gid=_user_gallery_pic._gallery WHERE _user_gallery_pic._user=select1.uid AND _user_gallery_pic._deleted=0) SELECT * FROM select2 ORDER BY originalname" , [b'alex', b'italia2006'] ),
( b'/alex/italia2006/firenze' , b"WITH select1 AS (SELECT _user._partition AS partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._path = $2 AND _user_gallery._deleted=0), select2 AS (SELECT _user_gallery_pic._originalname AS originalname, '/' || select1.partition ||'/'||_user_gallery_pic._pathstore as fullpathstore FROM _user_gallery_pic JOIN select1 ON select1.gid=_user_gallery_pic._gallery WHERE _user_gallery_pic._user=select1.uid AND _user_gallery_pic._deleted=0) SELECT * FROM select2 ORDER BY originalname" , [b'alex', b'italia2006/firenze'] ),
            ]
        for (path,query_ex,query_args_ex) in paths:
            (query,query_args)=atpic.forgesql.forge_piclist(path)
            print('TTT (',path,',',query,',',query_args,'),')
            self.assertEqual(query,query_ex)
            self.assertEqual(query_args,query_args_ex)
















    def test_picpathstore(self):
        paths=[
( b'alex/italia2006/firenze/immagine_292.jpg' , b"WITH select1 AS (SELECT _user._partition AS partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._path = $2 AND _user_gallery._deleted=0), select2 AS (SELECT '/' || select1.partition ||'/'||_user_gallery_pic._pathstore as _fullpathstore,_user_gallery_pic.*,select1.partition as _partition FROM _user_gallery_pic JOIN select1 ON select1.gid=_user_gallery_pic._gallery WHERE _user_gallery_pic._user=select1.uid AND _user_gallery_pic._originalname=$3 AND _user_gallery_pic._deleted=0) SELECT * FROM select2" , [b'alex', b'italia2006/firenze', b'immagine_292.jpg'] ),


            ]
        for (path,query_ex,query_args_ex) in paths:
            (query,query_args)=atpic.forgesql.forge_picpathstore(path)
            print('MMM (',path,',',query,',',query_args,'),')
            self.assertEqual(query,query_ex)
            self.assertEqual(query_args,query_args_ex)

    def test_fuseupsert(self):
        paths=[
( b'alex/italia2006/firenze/immagine_292.jpg' , b"WITH select1 AS (SELECT _user._partition AS _partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user_gallery._path = $2 AND _user._deleted=0 AND _user_gallery._deleted=0), select2 AS (SELECT _user_gallery_pic.* FROM _user_gallery_pic JOIN select1 ON _user_gallery_pic._user=select1.uid AND _user_gallery_pic._gallery=select1.gid WHERE _originalname=$3 AND _user_gallery_pic._deleted=0), select3 AS (INSERT INTO _user_gallery_pic (_user,_gallery,_originalname,_pathstore) (SELECT uid,gid,$4,$5 FROM select1 WHERE NOT EXISTS (SELECT 1 FROM select2)) RETURNING *), select4 AS (SELECT 'update' AS _upsert,* FROM select2 UNION SELECT 'insert' AS _upsert,* FROM select3) SELECT select4.*,select1._partition FROM select4 JOIN select1 ON select1.uid=select4._user" , [b'alex', b'italia2006/firenze', b'immagine_292.jpg', b'immagine_292.jpg', b'atpicfs_AwMNKvJBaDTdb2N8Uk1zUfhO1Nu0Rd8ud8FIWWHO'] ),

# ( b'alex/italia2006/firenze/immagine_292.jpg' , b"WITH select1 AS (SELECT _user._partition AS _partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user_gallery._path = $2), select2 AS (SELECT _user_gallery_pic.* FROM _user_gallery_pic JOIN select1 ON _user_gallery_pic._user=select1.uid AND _user_gallery_pic._gallery=select1.gid WHERE _originalname=$3), select3 AS (INSERT INTO _user_gallery_pic (_user,_gallery,_originalname) (SELECT uid,gid,$4 FROM select1 WHERE NOT EXISTS (SELECT 1 FROM select2)) RETURNING *) SELECT 'update' AS _upsert,* FROM select2 UNION SELECT 'insert' AS _upsert,* FROM select3" , [b'alex', b'italia2006/firenze', b'immagine_292.jpg', b'immagine_292.jpg'] ),
            ]
        for (path,query_ex,query_args_ex) in paths:
            (query,query_args)=atpic.forgesql.forge_fuseupsert(path)
            print('NNN (',path,',',query,',',query_args,'),')
            self.assertEqual(query,query_ex)
            # self.assertEqual(query_args,query_args_ex)



    def test_asyncpro(self):
        print('Hi')
        messages=[
(b'A|4|6666|47927|exif|xml|n/2014/05/23/14/20/4_6666_exif.xml', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'4', b'6666', b'47927', b'exif', b'xml', b'n/2014/05/23/14/20/4_6666_exif.xml'])) ,
(b'U|4|6666|image/x-canon-cr2|4368|2912||Canon|Canon EOS 5D|10.0|0.005|180|16|0|1|2006:01:15 19:04:48||', (b'UPDATE _user_gallery_pic SET _width=$1, _height=$2, _exifmake=$3, _exifmodel=$4, _exifaperture=$5, _exifexposuretime=$6, _exiffocallength=$7, _exifflash=$8, _exifwhitebalance=$9, _exifexposuremode=$10, _exifdatetimeoriginal=$11, _datetimeoriginalsql=$12, _mimetype_exiftool=$13, _mimesubtype_exiftool=$14 WHERE _user=$15 AND id=$16', [b'4368', b'2912', b'Canon', b'Canon EOS 5D', b'10.0', b'0.005', b'180', b'16', b'0', b'1', b'2006:01:15 19:04:48', b'2006-01-15 19:04:48.000000', b'image', b'x-canon-cr2', b'4', b'6666'])) ,
(b'A|4|6666|390316|0|jpg|n/2014/05/23/14/20/4_6666_0.jpg', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'4', b'6666', b'390316', b'0', b'jpg', b'n/2014/05/23/14/20/4_6666_0.jpg'])) ,
(b'A|4|6666|73609|r1024|jpg|n/2014/05/23/14/20/4_6666_r1024.jpg', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'4', b'6666', b'73609', b'r1024', b'jpg', b'n/2014/05/23/14/20/4_6666_r1024.jpg'])) ,
(b'A|4|6666|34874|r600|jpg|n/2014/05/23/14/20/4_6666_r600.jpg', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'4', b'6666', b'34874', b'r600', b'jpg', b'n/2014/05/23/14/20/4_6666_r600.jpg'])) ,
(b'A|4|6666|20944|r350|jpg|n/2014/05/23/14/20/4_6666_r350.jpg', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'4', b'6666', b'20944', b'r350', b'jpg', b'n/2014/05/23/14/20/4_6666_r350.jpg'])) ,
(b'A|4|6666|13844|r160|jpg|n/2014/05/23/14/20/4_6666_r160.jpg', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'4', b'6666', b'13844', b'r160', b'jpg', b'n/2014/05/23/14/20/4_6666_r160.jpg'])) ,
(b'A|4|6666|11680|r70|jpg|n/2014/05/23/14/20/4_6666_r70.jpg', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'4', b'6666', b'11680', b'r70', b'jpg', b'n/2014/05/23/14/20/4_6666_r70.jpg'])) ,
(b'A|18|8888|14497|exif|xml|n/2014/05/23/14/21/18_8888_exif.xml', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'18', b'8888', b'14497', b'exif', b'xml', b'n/2014/05/23/14/21/18_8888_exif.xml'])) ,
(b'U|18|8888|video/quicktime|190|240||||||||||||', (b'UPDATE _user_gallery_pic SET _width=$1, _height=$2, _exifmake=$3, _exifmodel=$4, _exifaperture=$5, _exifexposuretime=$6, _exiffocallength=$7, _exifflash=$8, _exifwhitebalance=$9, _exifexposuremode=$10, _exifdatetimeoriginal=$11, _mimetype_exiftool=$12, _mimesubtype_exiftool=$13 WHERE _user=$14 AND id=$15', [b'190', b'240', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'video', b'quicktime', b'18', b'8888'])) ,
(b'A|18|8888|932|v0|png|n/2014/05/23/14/21/18_8888_v0.png', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'18', b'8888', b'932', b'v0', b'png', b'n/2014/05/23/14/21/18_8888_v0.png'])) ,
(b'A|18|8888|1806|vf0|png|n/2014/05/23/14/21/18_8888_vf0.png', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'18', b'8888', b'1806', b'vf0', b'png', b'n/2014/05/23/14/21/18_8888_vf0.png'])) ,
(b'A|18|8888|482|v160|png|n/2014/05/23/14/21/18_8888_v160.png', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'18', b'8888', b'482', b'v160', b'png', b'n/2014/05/23/14/21/18_8888_v160.png'])) ,
(b'A|18|8888|1311|vf160|png|n/2014/05/23/14/21/18_8888_vf160.png', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'18', b'8888', b'1311', b'vf160', b'png', b'n/2014/05/23/14/21/18_8888_vf160.png'])) ,
(b'A|18|8888|391|v70|png|n/2014/05/23/14/21/18_8888_v70.png', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'18', b'8888', b'391', b'v70', b'png', b'n/2014/05/23/14/21/18_8888_v70.png'])) ,
(b'A|18|8888|1021|vf70|png|n/2014/05/23/14/21/18_8888_vf70.png', (b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($1,$2,$3,$4,$5,$6)', [b'18', b'8888', b'1021', b'vf70', b'png', b'n/2014/05/23/14/21/18_8888_vf70.png'])) ,
]
        for (message,(query_ex,query_args_ex)) in messages:
            print("Doing message")
            (query,query_args)=atpic.forgesql.asyncpro(message)
            print('res=',(query,query_args))
            print('ZZZZ',(message,(query,query_args)),',')
            self.assertEqual(query,query_ex)
            self.assertEqual(query_args,query_args_ex)

if __name__=="__main__":
    unittest.main()
