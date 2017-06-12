#!/usr/bin/python3
# one phrase per tagger per pic?? # YES: more complicated but easier to use
# http://stackoverflow.com/questions/2560946/postgresql-group-concat-equivalent

# there are NO sequence here!!!!
# as there is NO ID!!!!!
# or id is the tagger id
# same thing for phrases!!!!

# tag, phrase, friend: the ID is the user id
# adding a friend can thus just be an empty POST

out="""

SELECT _tagger as id,0 as _user,_pic, string_agg(_thetags, ' ') as _text,max(_datelast) as _datelast
INTO TABLE _user_gallery_pic_tag2 
FROM _user_gallery_pic_tag GROUP BY _tagger,_pic;

ALTER TABLE _user_gallery_pic_tag RENAME TO _user_gallery_pic_tag_old;
ALTER TABLE _user_gallery_pic_tag2 RENAME TO _user_gallery_pic_tag;
-- DROP TABLE _user_gallery_pic_tag_old;

-- ALTER TABLE _user_gallery_pic_tag RENAME COLUMN _tagger TO id integer;

SELECT _tagger as id,0 as _user,_gallery, string_agg(_thetags, ' ') as _text,max(_datelast) as _datelast
INTO TABLE _user_gallery_tag2 
FROM _user_gallery_tag GROUP BY _tagger,_gallery;

ALTER TABLE _user_gallery_tag RENAME TO _user_gallery_tag_old;
ALTER TABLE _user_gallery_tag2 RENAME TO _user_gallery_tag;
-- ALTER TABLE _user_gallery_tag RENAME COLUMN _tagger TO id;

-- DROP TABLE _user_gallery_tag_old;


SELECT _tagger as id,_user, string_agg(_thetags, ' ') as _text
INTO TABLE _user_tag2 
FROM _user_tag GROUP BY _tagger,_user;

ALTER TABLE _user_tag RENAME TO _user_tag_old;
ALTER TABLE _user_tag2 RENAME TO _user_tag;
-- DROP TABLE _user_tag_old;

-- ALTER TABLE _user_tag RENAME COLUMN _tagger TO id;

-- ALTER TABLE _user_gallery_phrase DROP COLUMN _thetags;
-- ALTER TABLE _user_gallery_phrase ADD COLUMN _text text;

-- ALTER TABLE _user_gallery_pic_phrase DROP COLUMN _thephrase;






SELECT _who_id as id,0 as _user,_pic, avg(_score) as _score,max(_datelast) as _datelast
INTO TABLE _user_gallery_pic_vote2
FROM _user_gallery_pic_vote WHERE _who_id>0 GROUP BY _who_id,_pic;

ALTER TABLE _user_gallery_pic_vote RENAME TO _user_gallery_pic_vote_old;
ALTER TABLE _user_gallery_pic_vote2 RENAME TO _user_gallery_pic_vote;

-- DROP TABLE _user_gallery_pic_vote_old;



-- ALTER TABLE _user_gallery_tag ADD COLUMN _user int;
-- ALTER TABLE _user_gallery_pic_tag ADD COLUMN _user int;
-- ALTER TABLE _user_gallery_pic_vote ADD COLUMN _user int;



SELECT  id,to_id AS _user,who_id AS _from, thetitle AS _title, thetext AS _text,thedatelast AS _datelast, read AS _read INTO _user_pm FROM pmessage WHERE who_id>0;

SELECT  id,to_id AS _to,who_id AS _user, thetitle AS _title, thetext AS _text,thedatelast AS _datelast INTO _user_pmsent FROM pmessage WHERE who_id>0;

-- now removing votes without valid user
 delete from _user_gallery_pic_vote where id not in (select id from _user);

"""

print(out)
