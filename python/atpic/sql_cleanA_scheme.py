#!/usr/bin/python3
out=[]

"""
-- I don't like having to add a TXT column: that duplicates the date; better to store it as HTML and then convert it on the fly
-- ALTER TABLE artist ADD COLUMN thetitle_txt text;
-- ALTER TABLE artist ADD COLUMN thetext_txt text;

-- ALTER TABLE artist_gallery ADD COLUMN thetitle_txt text;
-- ALTER TABLE artist_gallery ADD COLUMN thetext_txt text;

-- ALTER TABLE artist_pic ADD COLUMN thetitle_txt text;
-- ALTER TABLE artist_pic ADD COLUMN thetext_txt text;

"""

out.append("""
-- altering to text but no LIKE % allowing longer fields that varchar(127)

ALTER TABLE artist ALTER COLUMN thetitle TYPE text;
ALTER TABLE artist ALTER COLUMN thetext TYPE text;

ALTER TABLE artist_gallery ALTER COLUMN thetitle TYPE text;
ALTER TABLE artist_gallery ALTER COLUMN thetext TYPE text;

ALTER TABLE artist_pic ALTER COLUMN thetitle TYPE text;
ALTER TABLE artist_pic ALTER COLUMN thetext TYPE text;

""")

"""
-- drops the forum triggers defined in triggers.php
-- drops the pic triggers defined in triggers.php
-- Only the gallery triggers exists (for the path)
-- forums forumsfull forumsmax
-- drop view forums cascade;


-- to be used by a file system
-- NO: already done
-- ALTER TABLE artist_pic ADD COLUMN sizeb bigint;

-- mark the picture as "representative of the gallery"
-- NO: will use solr collapsed search
-- ALTER TABLE artist_pic ADD COLUMN repgallery boolean;

-- mark the picture as "representative of the year"
-- NO: will use solr collapsed search
-- ALTER TABLE artist_pic ADD COLUMN repyear boolean;

-- mark the picture as "representative of the month"
-- NO: will use solr collapsed search
-- ALTER TABLE artist_pic ADD COLUMN repmonth boolean;

-- mark the picture as "representative of the day
-- NO: will use solr collapsed search
-- ALTER TABLE artist_pic ADD COLUMN repday boolean;

-- (for global blog, we use a random field to choose randomly a representative user) 
-- (?not sure it is possible)
-- or should we put it in the gallery? No: this is a pic search, not a gallery search
-- but what happens if a gallery has no pic?

-- select aid,gid,pid,solr from select_flat_a(20);

-- UPDATE artist set thetitle_txt=pyclean(thetitle);
-- UPDATE artist set thetext_txt=pyclean(thetext);

-- UPDATE artist_gallery set thetitle_txt=pyclean(thetitle);
-- UPDATE artist_gallery set thetext_txt=pyclean(thetext);

-- UPDATE artist_pic set thetitle_txt=pyclean(thetitle);
-- UPDATE artist_pic set thetext_txt=pyclean(thetext);
"""


out.append("""
UPDATE artist set thetitle='' where thetitle=' ';
UPDATE artist set thetext='' where thetext=' ';
""")

"""
-- select now();
-- UPDATE artist set thetitle_txt=thetitle, thetext_txt=thetext;
-- select now();


-- SLOW due to : "path_down" line 11 at for over select rows PL/pgSQL function "path_down_artist"
"""



out.append("""
-- check the triggers with \d artist_gallery
-- DROP TRIGGER trigger_insert_artist_gallery ON artist_gallery;
-- DROP FUNCTION trigger_insert_artist_gallery();


UPDATE artist_gallery set thetitle='' where thetitle=' ';
UPDATE artist_gallery set thetext='' where thetext=' ';
-- select now();
-- UPDATE artist_gallery set thetitle_txt=thetitle,thetext_txt=thetext;
-- select now();

-- DROP TRIGGER trigger_insert_artist_pic ON artist_pic;
-- DROP FUNCTION trigger_insert_artist_pic();

UPDATE artist_pic set thetitle='' where thetitle=' ';
UPDATE artist_pic set thetext='' where thetext=' ';
-- select now();
-- UPDATE artist_pic set thetitle_txt=thetitle,thetext_txt=thetext;
-- select now();

-- should take 8 minutes 

""")


print("".join(out))
#!/usr/bin/python3
# we use a leading '_'
print("""
-- rename according to REST API
ALTER TABLE artist         RENAME TO _user; 
ALTER TABLE artist_gallery RENAME TO _user_gallery; 
ALTER TABLE artist_pic     RENAME TO _user_gallery_pic; 
ALTER TABLE tag_a          RENAME TO _user_tag;
ALTER TABLE tag_g          RENAME TO _user_gallery_tag;
ALTER TABLE tag_p          RENAME TO _user_gallery_pic_tag;
-- _user_gallery_pic_face
-- _user_gallery_phrase
-- _user_gallery_pic_phrase
ALTER TABLE vote_p         RENAME TO _user_gallery_pic_vote;
ALTER TABLE forum_a        RENAME TO _user_comment;
ALTER TABLE forum_g        RENAME TO _user_gallery_comment;
ALTER TABLE forum_p        RENAME TO _user_gallery_pic_comment;
-- _user_pmrec
-- _user_pmsent
-- _user_friend
-- _user_payment
-- _user_buy
-- _user_sell
ALTER TABLE wiki        RENAME TO  _translate;
-- _news
-- _faq

-- pmessage


ALTER TABLE _user_gallery RENAME COLUMN refartist TO _user;

ALTER TABLE _user_gallery_pic RENAME COLUMN refartist_gallery TO _gallery;

ALTER TABLE _user DROP COLUMN admin_country;
ALTER TABLE _user DROP COLUMN admin_firstname;
ALTER TABLE _user DROP COLUMN admin_lastname;
ALTER TABLE _user DROP COLUMN admin_password_clear;
ALTER TABLE _user DROP COLUMN supporter;
ALTER TABLE _user DROP COLUMN reviewed;
ALTER TABLE _user DROP COLUMN revaccepted;

ALTER TABLE _user DROP COLUMN allowpost;
ALTER TABLE _user DROP COLUMN server;
ALTER TABLE _user DROP COLUMN skin;
-- ALTER TABLE _user DROP COLUMN css;
ALTER TABLE _user DROP COLUMN newskin;
-- ALTER TABLE _user DROP COLUMN template;



ALTER TABLE _user ALTER COLUMN rows TYPE integer;
ALTER TABLE _user ALTER COLUMN cols TYPE integer;
ALTER TABLE _user ALTER COLUMN css TYPE integer;

update _user set rows='0' where rows='';
update _user set rows='0' where rows like 'p%';
update _user set cols='0' where cols='';




ALTER TABLE _user_gallery DROP COLUMN lang;
ALTER TABLE _user_gallery DROP COLUMN refgallery;
ALTER TABLE _user_gallery DROP COLUMN thenick;
ALTER TABLE _user_gallery DROP COLUMN reviewed;
ALTER TABLE _user_gallery DROP COLUMN revaccepted;
ALTER TABLE _user_gallery DROP COLUMN automaticframe;
ALTER TABLE _user_gallery DROP COLUMN section;
ALTER TABLE _user_gallery DROP COLUMN thestyle;




ALTER TABLE _user_comment DROP COLUMN parentype;
ALTER TABLE _user_gallery_comment DROP COLUMN parentype;
ALTER TABLE _user_gallery_pic_comment DROP COLUMN parentype;





ALTER TABLE _user_gallery_pic_vote DROP COLUMN parentype;
ALTER TABLE _user_gallery_pic_vote DROP COLUMN code_lesson;

ALTER TABLE _user ADD COLUMN _usage bigint;
ALTER TABLE _user ADD COLUMN _secret character varying(10);
ALTER TABLE _user ADD COLUMN _pdns character varying(127);



""")




#!/usr/bin/python3
print("""
ALTER TABLE _user_gallery_pic_tag RENAME COLUMN tagger TO _tagger;
ALTER TABLE _user_gallery_pic_tag RENAME COLUMN docid TO _pic;
ALTER TABLE _user_gallery_pic_tag RENAME COLUMN thetags TO _thetags;
ALTER TABLE _user_gallery_pic_tag RENAME COLUMN thetext TO _thetext;
ALTER TABLE _user_gallery_pic_tag RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _user_gallery_pic_tag RENAME COLUMN reviewed TO _reviewed;
ALTER TABLE _user_gallery_pic_tag RENAME COLUMN revaccepted TO _revaccepted;



ALTER TABLE _user RENAME COLUMN admin_login TO _login;
ALTER TABLE _user RENAME COLUMN admin_password TO _password;
ALTER TABLE _user RENAME COLUMN servershort TO _servershort;
ALTER TABLE _user RENAME COLUMN admin_email TO _email;
ALTER TABLE _user RENAME COLUMN size_allowed TO _size_allowed;
ALTER TABLE _user RENAME COLUMN thetitle TO _title;
ALTER TABLE _user RENAME COLUMN thetext TO _text;
ALTER TABLE _user RENAME COLUMN thedatefirst TO _datefirst;
ALTER TABLE _user RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _user RENAME COLUMN counter TO _counter;
ALTER TABLE _user RENAME COLUMN lang TO _lang;
ALTER TABLE _user RENAME COLUMN thestyleid TO _thestyleid;
ALTER TABLE _user RENAME COLUMN rows TO _rows;
ALTER TABLE _user RENAME COLUMN cols TO _cols ;
ALTER TABLE _user RENAME COLUMN template TO _template;
ALTER TABLE _user RENAME COLUMN css TO _css;
ALTER TABLE _user RENAME COLUMN storefrom TO _storefrom;
ALTER TABLE _user RENAME COLUMN storeto TO _storeto;
ALTER TABLE _user RENAME COLUMN synced TO _synced;
ALTER TABLE _user RENAME COLUMN admin_name TO _name;



ALTER TABLE _user_gallery RENAME COLUMN thedatefirst TO _datefirst;
ALTER TABLE _user_gallery RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _user_gallery RENAME COLUMN counter TO _counter;
ALTER TABLE _user_gallery RENAME COLUMN priority TO _priority;
ALTER TABLE _user_gallery RENAME COLUMN cols TO _cols;
ALTER TABLE _user_gallery RENAME COLUMN rows TO _rows;
ALTER TABLE _user_gallery RENAME COLUMN thetitle TO _title;
ALTER TABLE _user_gallery RENAME COLUMN thetext TO _text;
ALTER TABLE _user_gallery RENAME COLUMN bgcolor TO _bgcolor;
ALTER TABLE _user_gallery RENAME COLUMN fgcolor TO _fgcolor;
ALTER TABLE _user_gallery RENAME COLUMN thestyleid TO _style;
ALTER TABLE _user_gallery RENAME COLUMN secret TO _secret;
ALTER TABLE _user_gallery RENAME COLUMN template_gallery TO _template_gallery;
ALTER TABLE _user_gallery RENAME COLUMN template_pic TO _template_pic;
ALTER TABLE _user_gallery RENAME COLUMN css_gallery TO _css_gallery;
ALTER TABLE _user_gallery RENAME COLUMN css_pic TO _css_pic;
ALTER TABLE _user_gallery RENAME COLUMN file TO _file;
ALTER TABLE _user_gallery RENAME COLUMN dir TO _dir;
ALTER TABLE _user_gallery RENAME COLUMN skin_gallery TO _skin_gallery;
ALTER TABLE _user_gallery RENAME COLUMN skin_pic TO _skin_pic;
ALTER TABLE _user_gallery RENAME COLUMN lat TO _lat;
ALTER TABLE _user_gallery RENAME COLUMN long TO _lon;
ALTER TABLE _user_gallery RENAME COLUMN mode TO _mode;



ALTER TABLE _user_gallery_pic RENAME COLUMN width TO _width;
ALTER TABLE _user_gallery_pic RENAME COLUMN height TO _height;
ALTER TABLE _user_gallery_pic RENAME COLUMN originalname TO _originalname;
ALTER TABLE _user_gallery_pic RENAME COLUMN priority TO _priority;
ALTER TABLE _user_gallery_pic RENAME COLUMN make TO _make;
ALTER TABLE _user_gallery_pic RENAME COLUMN model TO _model;
ALTER TABLE _user_gallery_pic RENAME COLUMN aperture TO _aperture;
ALTER TABLE _user_gallery_pic RENAME COLUMN exposuretime TO _exposuretime;
ALTER TABLE _user_gallery_pic RENAME COLUMN focallength TO _focallength;
ALTER TABLE _user_gallery_pic RENAME COLUMN meteringmode TO _meteringmode;
ALTER TABLE _user_gallery_pic RENAME COLUMN flash TO _flash;
ALTER TABLE _user_gallery_pic RENAME COLUMN whitebalance TO _whitebalance;
ALTER TABLE _user_gallery_pic RENAME COLUMN exposuremode TO _exposuremode;
ALTER TABLE _user_gallery_pic RENAME COLUMN sensingmethod TO _sensingmethod;
ALTER TABLE _user_gallery_pic RENAME COLUMN datetimeoriginal TO _datetimeoriginal;
ALTER TABLE _user_gallery_pic RENAME COLUMN datetimedigitized TO _datetimedigitized;
ALTER TABLE _user_gallery_pic RENAME COLUMN bgcolor TO _bgcolor;
ALTER TABLE _user_gallery_pic RENAME COLUMN fgcolor TO _fgcolor;
ALTER TABLE _user_gallery_pic RENAME COLUMN thedatefirst TO _datefirst;
ALTER TABLE _user_gallery_pic RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _user_gallery_pic RENAME COLUMN thetitle TO _title;
ALTER TABLE _user_gallery_pic RENAME COLUMN thetext TO _text;
ALTER TABLE _user_gallery_pic RENAME COLUMN counter TO _counter;
ALTER TABLE _user_gallery_pic RENAME COLUMN reviewed TO _reviewed;
ALTER TABLE _user_gallery_pic RENAME COLUMN revaccepted TO _revaccepted;
ALTER TABLE _user_gallery_pic RENAME COLUMN extension TO _extension;
ALTER TABLE _user_gallery_pic RENAME COLUMN done TO _done;
ALTER TABLE _user_gallery_pic RENAME COLUMN link TO _link;
ALTER TABLE _user_gallery_pic RENAME COLUMN lat TO _lat;
ALTER TABLE _user_gallery_pic RENAME COLUMN long TO _lon;
ALTER TABLE _user_gallery_pic RENAME COLUMN notpop TO _notpop;
ALTER TABLE _user_gallery_pic RENAME COLUMN datetimeoriginalsql TO _datetimeoriginalsql;
ALTER TABLE _user_gallery_pic RENAME COLUMN isospeedratings TO _isospeedratings;
ALTER TABLE _user_gallery_pic RENAME COLUMN sizeb TO _sizeb;



ALTER TABLE _translate RENAME COLUMN lid TO _lid;
ALTER TABLE _translate RENAME COLUMN artistid TO _user;
ALTER TABLE _translate RENAME COLUMN lang TO _lang;
ALTER TABLE _translate RENAME COLUMN thetext TO _text;
ALTER TABLE _translate RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _translate RENAME COLUMN reviewed TO _reviewed;
ALTER TABLE _translate RENAME COLUMN revaccepted TO _revaccepted;
ALTER TABLE _translate RENAME COLUMN ip TO _ip;



ALTER TABLE _user_comment RENAME COLUMN refparent TO _user;
ALTER TABLE _user_comment RENAME COLUMN who_id TO _who_id;
ALTER TABLE _user_comment RENAME COLUMN who_login TO _who_login;
ALTER TABLE _user_comment RENAME COLUMN who_name TO _who_name;
ALTER TABLE _user_comment RENAME COLUMN who_email TO _who_email;
ALTER TABLE _user_comment RENAME COLUMN thetitle TO _title;
ALTER TABLE _user_comment RENAME COLUMN thetext TO _text;
ALTER TABLE _user_comment RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _user_comment RENAME COLUMN reviewed TO _reviewed;
ALTER TABLE _user_comment RENAME COLUMN revaccepted TO _revaccepted;



ALTER TABLE _user_gallery_comment RENAME COLUMN refparent TO _gallery;
ALTER TABLE _user_gallery_comment RENAME COLUMN who_id TO _who_id;
ALTER TABLE _user_gallery_comment RENAME COLUMN who_login TO _who_login;
ALTER TABLE _user_gallery_comment RENAME COLUMN who_name TO _who_name;
ALTER TABLE _user_gallery_comment RENAME COLUMN who_email TO _who_email;
ALTER TABLE _user_gallery_comment RENAME COLUMN thetitle TO _title;
ALTER TABLE _user_gallery_comment RENAME COLUMN thetext TO _text;
ALTER TABLE _user_gallery_comment RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _user_gallery_comment RENAME COLUMN reviewed TO _reviewed;
ALTER TABLE _user_gallery_comment RENAME COLUMN revaccepted TO _revaccepted;


ALTER TABLE _user_gallery_pic_comment RENAME COLUMN refparent TO _pic;
ALTER TABLE _user_gallery_pic_comment RENAME COLUMN who_id TO _who_id;
ALTER TABLE _user_gallery_pic_comment RENAME COLUMN who_login TO _who_login;
ALTER TABLE _user_gallery_pic_comment RENAME COLUMN who_name TO _who_name;
ALTER TABLE _user_gallery_pic_comment RENAME COLUMN who_email TO _who_email;
ALTER TABLE _user_gallery_pic_comment RENAME COLUMN thetitle TO _title;
ALTER TABLE _user_gallery_pic_comment RENAME COLUMN thetext TO _text;
ALTER TABLE _user_gallery_pic_comment RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _user_gallery_pic_comment RENAME COLUMN reviewed TO _reviewed;
ALTER TABLE _user_gallery_pic_comment RENAME COLUMN revaccepted TO _revaccepted;


ALTER TABLE _user_gallery_tag RENAME COLUMN tagger TO _tagger;
ALTER TABLE _user_gallery_tag RENAME COLUMN docid TO _gallery;
ALTER TABLE _user_gallery_tag RENAME COLUMN thetags TO _thetags;
-- ALTER TABLE _user_gallery_tag RENAME COLUMN thetext TO _thetext;
ALTER TABLE _user_gallery_tag RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _user_gallery_tag RENAME COLUMN reviewed TO _reviewed;
ALTER TABLE _user_gallery_tag RENAME COLUMN revaccepted TO _revaccepted;

ALTER TABLE _user_tag RENAME COLUMN tagger TO _tagger;
ALTER TABLE _user_tag RENAME COLUMN docid TO _user;
ALTER TABLE _user_tag RENAME COLUMN thetags TO _thetags;
-- ALTER TABLE _user_tag RENAME COLUMN thetext TO _thetext;
ALTER TABLE _user_tag RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _user_tag RENAME COLUMN reviewed TO _reviewed;
ALTER TABLE _user_tag RENAME COLUMN revaccepted TO _revaccepted;



ALTER TABLE _user_gallery_pic_vote RENAME COLUMN refparent TO _pic;
ALTER TABLE _user_gallery_pic_vote RENAME COLUMN score TO _score;
ALTER TABLE _user_gallery_pic_vote RENAME COLUMN who_id TO _who_id;
ALTER TABLE _user_gallery_pic_vote RENAME COLUMN who_ip TO _who_ip;
ALTER TABLE _user_gallery_pic_vote RENAME COLUMN thedatelast TO _datelast;
ALTER TABLE _user_gallery_pic_vote RENAME COLUMN reviewed TO _reviewed;
ALTER TABLE _user_gallery_pic_vote RENAME COLUMN revaccepted TO _revaccepted;


""")
#!/usr/bin/python3
# we add a '_user' column to each table below user:
# this can help in database partitionning and database clustering


# for res in ["1024","600","350","160","70","0","water600","water350","exif"]:
# will be renamed datestore
# print("""ALTER TABLE _user_gallery_pic ADD COLUMN _r%s timestamp without time zone;""" % res)
print("""ALTER TABLE _user_gallery_pic ADD COLUMN _pathstore VARCHAR(255);""")
# print("""ALTER TABLE _user_gallery_pic ADD COLUMN _size bigint;""" % res)
# print("""ALTER TABLE _user_gallery_pic ALTER COLUMN  _size%s  SET DEFAULT 0;""" % res)



# for col in ["datefirst","r1024","r600","r350","r160","r70","r0"]:
#     print("ALTER TABLE _user_gallery_pic ALTER COLUMN _%s SET DEFAULT now();" % col)


for colname in ["_mimetype_magic","_mimesubtype_magic","_mimetype_exiftool","_mimesubtype_exiftool",]:
    print("ALTER TABLE _user_gallery_pic ADD COLUMN %s character varying(127);" % colname)


# we add a '_user' column to each table below user:
# this can help in database partitionning and database clustering

print("""
ALTER TABLE _user ADD COLUMN _pricebase float;
ALTER TABLE _user_gallery_pic ADD COLUMN _user integer;
ALTER TABLE _user_gallery_pic ADD COLUMN _price float;
ALTER TABLE _user_gallery_pic ADD COLUMN _pricebase float;
-- ALTER TABLE _user_gallery_pic ADD COLUMN _mode character(1);
ALTER TABLE _user_gallery ADD COLUMN _pricebase float;
ALTER TABLE _user_gallery_pic_tag ADD COLUMN _user integer;
ALTER TABLE _user_gallery_tag ADD COLUMN _user integer;
ALTER TABLE _user_gallery_pic_comment ADD COLUMN _user integer;

ALTER TABLE _user_gallery_comment ADD COLUMN _user integer;


ALTER TABLE _user_gallery ADD COLUMN _path VARCHAR(1024);
ALTER TABLE _user_gallery ADD COLUMN _depth integer;


""")
