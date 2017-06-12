def getmodel():
	s="""<model>
<table name="_chapter">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_chapter__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_short" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_text" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_sort" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_chapter__seq" attname="id"/>
<index name="_chapter___sort" indexdef="CREATE INDEX _chapter___sort ON _chapter USING btree (_sort)"/>
<constraint name="_chapter__pkey" condef="PRIMARY KEY (id)"/>
<constraint name="_chapter__u_short" condef="UNIQUE (_short)"/>
</table>
<table name="_chapter_section">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_chapter_section__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_short" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_question" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_answer" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_chapter" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_sort" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_chapter_section__seq" attname="id"/>
<index name="_chapter_section___sort" indexdef="CREATE INDEX _chapter_section___sort ON _chapter_section USING btree (_sort)"/>
<constraint name="_chapter_section__f_chapter" condef="FOREIGN KEY (_chapter) REFERENCES _chapter(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_chapter_section__u_short" condef="UNIQUE (_short)"/>
<constraint name="_section__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_entry">
<attribute name="id" type="integer" notnull="True" attrel="None" read="True" write="False"/>
<attribute name="_started" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_finished" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_status" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>

<constraint name="_entry__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_entry_line">
<attribute name="id" type="integer" notnull="True" attrel="None" read="True" write="False"/>
<attribute name="_entry" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_account" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_amount" type="real" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_type" type="character varying(1)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_user" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_gallery" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_pic" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_tag" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_phrase" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_storage" type="integer" notnull="False" attrel="None" read="True" write="True"/>

<constraint name="_entry_line__f_entry" condef="FOREIGN KEY (_entry) REFERENCES _entry(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_line__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_news">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_news__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_date" type="date" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_text" type="text" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_news__seq" attname="id"/>
<constraint name="_news__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_product">
<attribute name="id" type="integer" notnull="True" attrel="None" read="True" write="False"/>
<attribute name="_price" type="real" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_active" type="boolean" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_gigabytes" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_description" type="text" notnull="False" attrel="None" read="True" write="True"/>

<constraint name="_product__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_testtable">
<attribute name="id" type="integer" notnull="False" attrel="None" read="True" write="False"/>
<attribute name="description" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="title" type="text" notnull="False" attrel="None" read="True" write="True"/>

</table>
<table name="_translate">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_translate__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_lid" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_user" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_lang" type="character(2)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_text" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_reviewed" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_revaccepted" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_ip" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_translate__seq" attname="id"/>
<index name="_translate___lang_lid" indexdef="CREATE INDEX _translate___lang_lid ON _translate USING btree (_lang, _lid)"/>
<constraint name="_translate__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_user">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_login" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_password" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_servershort" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_email" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_size_allowed" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_title" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_text" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datefirst" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_counter" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_lang" type="character(2)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_thestyleid" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_rows" type="character varying(63)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_cols" type="character varying(63)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_template" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_css" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_storefrom" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_storeto" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_synced" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_name" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_user__seq" attname="id"/>
<constraint name="_user__pkey" condef="PRIMARY KEY (id)"/>
<constraint name="_user__u_login" condef="UNIQUE (_login)"/>
<constraint name="_user__u_servershort" condef="UNIQUE (_servershort)"/>
</table>
<table name="_user_comment">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user_comment__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_user" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_id" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_login" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_name" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_email" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_title" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_text" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_reviewed" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_revaccepted" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<sequence name="_user_comment__seq" attname="id"/>
<constraint name="_user_comment__f_user" condef="FOREIGN KEY (_user) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_comment__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_user_friend">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user_friend__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_user" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_friend" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_user_friend__seq" attname="id"/>
<constraint name="_user_friend__f_user" condef="FOREIGN KEY (_user) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_friend__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_user_gallery">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user_gallery__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_user" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datefirst" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_counter" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_priority" type="character varying(63)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_cols" type="character varying(63)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_rows" type="character varying(63)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_title" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_text" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_bgcolor" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_fgcolor" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_style" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_secret" type="character varying(63)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_template_gallery" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_template_pic" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_css_gallery" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_css_pic" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_file" type="character varying(255)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_dir" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_skin_gallery" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_skin_pic" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_lat" type="real" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_lon" type="real" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_mode" type="character(1)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_isroot" type="character(1)" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_user_gallery__seq" attname="id"/>
<index name="_user_gallery___secret" indexdef="CREATE INDEX _user_gallery___secret ON _user_gallery USING btree (_secret)"/>
<index name="_user_gallery___user" indexdef="CREATE INDEX _user_gallery___user ON _user_gallery USING btree (_user)"/>
<constraint name="_user_gallery__f_user" condef="FOREIGN KEY (_user) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_gallery__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_user_gallery_comment">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user_gallery_comment__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_gallery" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_id" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_login" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_name" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_email" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_title" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_text" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_reviewed" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_revaccepted" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<sequence name="_user_gallery_comment__seq" attname="id"/>
<constraint name="_user_gallery_comment__f_gallery" condef="FOREIGN KEY (_gallery) REFERENCES _user_gallery(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_gallery_comment__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_user_gallery_pic">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user_gallery_pic__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_gallery" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_width" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_height" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_originalname" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_priority" type="character varying(63)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_make" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_model" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_aperture" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_exposuretime" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_focallength" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_meteringmode" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_flash" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_whitebalance" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_exposuremode" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_sensingmethod" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datetimeoriginal" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datetimedigitized" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_bgcolor" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_fgcolor" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datefirst" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_title" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_text" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_counter" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_reviewed" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_revaccepted" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_extension" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_done" type="character(1)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_link" type="character varying(254)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_lat" type="real" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_lon" type="real" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_notpop" type="bit(1)" notnull="False" attrel="B'0'::bit" read="True" write="True"/>
<attribute name="_datetimeoriginalsql" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_isospeedratings" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_sizeb" type="bigint" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_user" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_user_gallery_pic__seq" attname="id"/>
<index name="_user_gallery_pic___gallery" indexdef="CREATE INDEX _user_gallery_pic___gallery ON _user_gallery_pic USING btree (_gallery)"/>
<index name="_user_gallery_pic___make" indexdef="CREATE INDEX _user_gallery_pic___make ON _user_gallery_pic USING btree (_make)"/>
<index name="_user_gallery_pic___model" indexdef="CREATE INDEX _user_gallery_pic___model ON _user_gallery_pic USING btree (_model)"/>
<index name="_user_gallery_pic___notpop" indexdef="CREATE INDEX _user_gallery_pic___notpop ON _user_gallery_pic USING btree (_notpop)"/>
<constraint name="_user_gallery_pic__f_gallery" condef="FOREIGN KEY (_gallery) REFERENCES _user_gallery(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_gallery_pic__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_user_gallery_pic_comment">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user_gallery_pic_comment__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_pic" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_id" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_login" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_name" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_email" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_title" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_text" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_reviewed" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_revaccepted" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<sequence name="_user_gallery_pic_comment__seq" attname="id"/>
<constraint name="_user_gallery_pic_comment__f_pic" condef="FOREIGN KEY (_pic) REFERENCES _user_gallery_pic(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_gallery_pic_comment__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_user_gallery_pic_tag">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user_gallery_pic_tag__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_tagger" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_pic" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_thetags" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_thetext" type="text" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_thedatelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_reviewed" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_revaccepted" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_user_gallery_pic_tag__seq" attname="id"/>
<index name="_user_gallery_pic_tag___pic_tagger" indexdef="CREATE INDEX _user_gallery_pic_tag___pic_tagger ON _user_gallery_pic_tag USING btree (_pic, _tagger)"/>
<constraint name="_user_gallery_pic_tag__f_pic" condef="FOREIGN KEY (_pic) REFERENCES _user_gallery_pic(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_gallery_pic_tag__f_tagger" condef="FOREIGN KEY (_tagger) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_gallery_pic_tag__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_user_gallery_pic_vote">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user_gallery_pic_vote__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_pic" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_score" type="real" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_id" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_who_ip" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_datelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_reviewed" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_revaccepted" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<sequence name="_user_gallery_pic_vote__seq" attname="id"/>
<index name="_user_gallery_pic_vote___pic_revaccepted" indexdef="CREATE INDEX _user_gallery_pic_vote___pic_revaccepted ON _user_gallery_pic_vote USING btree (_pic, _revaccepted)"/>
<constraint name="_user_gallery_pic_vote__f_pic" condef="FOREIGN KEY (_pic) REFERENCES _user_gallery_pic(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_gallery_pic_vote__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_user_gallery_tag">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user_gallery_tag__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_tagger" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_gallery" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_thetags" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_thedatelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_reviewed" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_revaccepted" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_user_gallery_tag__seq" attname="id"/>
<index name="_user_gallery_tag___gallery_tagger" indexdef="CREATE INDEX _user_gallery_tag___gallery_tagger ON _user_gallery_tag USING btree (_gallery, _tagger)"/>
<constraint name="_user_gallery_tag__f_gallery" condef="FOREIGN KEY (_gallery) REFERENCES _user_gallery(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_gallery_tag__f_tagger" condef="FOREIGN KEY (_tagger) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_gallery_tag__pkey" condef="PRIMARY KEY (id)"/>
</table>
<table name="_user_tag">
<attribute name="id" type="integer" notnull="True" attrel="nextval(('_user_tag__seq'::text)::regclass)" read="True" write="False"/>
<attribute name="_tagger" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_user" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_thetags" type="character varying(127)" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_thedatelast" type="timestamp without time zone" notnull="False" attrel="None" read="True" write="True"/>
<attribute name="_reviewed" type="integer" notnull="False" attrel="0" read="True" write="True"/>
<attribute name="_revaccepted" type="integer" notnull="False" attrel="None" read="True" write="True"/>
<sequence name="_user_tag__seq" attname="id"/>
<index name="_user_tag___tagger_user" indexdef="CREATE INDEX _user_tag___tagger_user ON _user_tag USING btree (_tagger, _user)"/>
<constraint name="_user_tag__f_tagger" condef="FOREIGN KEY (_tagger) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_tag__f_user" condef="FOREIGN KEY (_user) REFERENCES _user(id) ON UPDATE CASCADE ON DELETE CASCADE"/>
<constraint name="_user_tag__pkey" condef="PRIMARY KEY (id)"/>
</table>
</model>
"""
	return s