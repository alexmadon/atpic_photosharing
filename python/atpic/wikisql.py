# i18n: languages (table _translate)
# faq:
# user wiki: 
# atpic wiki: 
# news: 
# ==============
# _chapter
# _chapter_section => /faq/howto/video
# SQL: 
# 2 categories:
# a) versionable
# b) non versionable
# for versionable: need an index to the last (elasticsearch)

# atpic.com/wiki/API
# sql table _wiki: (id, key or path:api, date, who, ip, commit, sha1: sha1(content), content)
# sql table _user_wiki

# one big table for SHA1? this is a pure key-value
# http://stackoverflow.com/questions/1638577/storing-sha1-signature-as-primary-key-in-postgres-sql
# http://subversion.jfrog.org/artifactory/public/trunk/storage/db/src/main/resources/postgresql/postgresql.sql
#   sha1       CHAR(40) NOT NULL,
# could store on disk the gzip content or in DB

# but no sharding per UID!!!!


# update or leave:
# if sha1 of the last insert for the same path==sha1 of new one, then do nothing
#
# actions: insert, delete, select
# 

# PUT atpic.com/wiki/API (creates a new version if different from previous version)
# GET atpic.com/wiki/API
# GET atpic.com/wiki/API?rev=xxxxxxx
# GET atpic.com/wiki/API?diff=xxxxxxx,yyyyyy
# GET atpic.com/wiki/API?put
# GET atpic.com/wiki/API?post
# GET atpic.com/wiki/API?delete
# POST atpic.com/wiki/API?delete
# DELETE atpic.com/wiki/API


# normal formats: xml, json, xhtml
# wiki formats:
# Content-Type: application/x-fossil

# http://stackoverflow.com/questions/10701983/what-is-the-mime-type-for-markdown
# text/x-markdown; charset=UTF-8
# text/vnd.daringfireball.markdown

# MIME type for reStructuredText
# "official unofficial" standard MIME type is "text/x-rst".

# text/x-textile
# text/x-web-markdown;
# text/x-web-textile; 

# text (wikitext) -> xml -> xhtml
#                 -> json
# linktome
# links
# deadlinks

# DIFFERENCE with mormal page:
# here we start from text, normally we start from XML
# there is one costful additional operation

# need to index the last post into elasticsearch
# index stores links
# picture:1234

# or
# http://atpic.com/wiki/API/_delete
# http://atpic.com/wiki/API/_put
# http://atpic.com/wiki/API/_post
# http://atpic.com/wiki/API/_diff/xxxxxx,yyyyyy
# http://atpic.com/wiki/API/_version (collection)
# http://atpic.com/wiki/API/_version/xxxxxx

# RULE: no start with underscore in wiki names

# formats:
# XML: do not show intermediate XML (ASL) but show wikitext embededd in XML
# XHTML: catch the embedded wikitext and translate it to XML, 
# then transform the whole to xhtml 
