#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse


import atpic.dispatcher

"""
Atom Publishing Protocol Summary

Resource 	Method 	Description
Entry 	        GET 	Get the latest
Entry 	        PUT 	Update an entry
Entry 	        DELETE 	Delete the entry
Collection 	GET 	Get a list of entries
Collection 	POST 	Create a new entry
"""

"""
ATPIC Atom Publishing Protocol Summary

Resource 	Method 	Description

Entry 	        PUT 	Update an entry
Entry 	        DELETE 	Delete the entry

EntryCol 	GET 	Get the latest entry + all children (can filter by type)
Collection 	POST 	Create a new entry (need to specify the type in URL or data)

type=entry,collection and then simple,home,google(views),blog,tree
if entry or collection: object=pic, etc...
action=get,etc..
if entry id
format=xml, etc...
showxsl=

context=atpic or user
"""

# ===================================================
# ===================================================
#     3rd possible:
#     look at the position of the paths
# ===================================================
# ===================================================





urls_before=[
# those should NOT hit python as dealt with by apache directly 
# before hitting python

# views (Note: if you remove the 'alex' there is not much sense to 
# http://tree.atpic.com, blog.atpic.com, dav.atpic.com, ftp.atpic.com
# ("GET","http://alex.fs.atpic.com"), # do not put after slash to avoidrules on folders names
# OR:
# ("GET","http://alex.atpic.com/fs")
# ("GET","http://alex.maps.atpic.com"),
# ("GET","http://alex.google.atpic.com"),

# tree protocols:
("GET","http://alex.dav.atpic.com"),
# OR:
# ("GET","http://alex.atpic.com/dav"), # NOT Good as cannot put a different DNS than above for speed

("GET","http://alex.ftp.atpic.com"),
# buffer protocols:
("GET","http://alex.davb.atpic.com"),
("GET","http://alex.ftpb.atpic.com"),

# disktier
("GET","http://user3.atpic.com/disktier"), # each server has its disktier
# sql tier

# hbase tier
]


paths_id=[
"/pic/999",
# "/pic/998.xml",  xml format is passes in query string f=xml
# "/pic/997.xml.xsl",
"/pic/997/delete",
"/pic/997/put",
"/pic/post",
"/pic/171546/jtfgimzxcdylugbmebyq",
# "/pic/171546/jtfgimzxcdylugbmebyq.xml",
"/999",
"/gallery/171546/jtfgimzxcdylugbmebyq",
"/flash/98", # flash gallery
]

paths_id_legacy=[
"/999", # legacy
"/999/1024", # legacy
"/fr/999", # legacy
"/999/secret", # legacy
"/999/1024/secret", # legacy
"/171546/0/jtfgimzxcdylugbmebyq", #http://pic.atpic.com/171546/0/jtfgimzxcdylugbmebyq
"/fr/171546/600/jtfgimzxcdylugbmebyq", #http://pic.atpic.com/fr/171546/600/jtfgimzxcdylugbmebyq
"/fr/1538986", #http://pic.atpic.com/fr/1538986
"/de/1282892/600", #http://pic.atpic.com/de/1282892/600
]


paths_tree=[
"/tree",
"/tree/",
"/tree/france",
"/tree/france/",
"/tree/france/paris",
"/tree/france/paris/",
"/tree/france/paris/eiffel_tower",
]


paths_ymd=[
"/blog/2009",
# "/blog/2009.xml",
# "/blog/2009.xml.xsl",
"/blog/2009/12",
# "/blog/2009/12.xml",
# "/blog/2009/12.xml.xsl",
"/blog/2009/12/31",
# "/blog/2009/12/31.xml",
# "/blog/2009/12/31.xml.xsl",
]

hosts=[
"www.atpic.com",
"alex.atpic.com",
"pic.atpic.com",
"gallery.atpic.com",
"faq.atpic.com",
"www.atpic.faa",
"alex.atpic.faa",
"my.photo.com", # sell DNS

]

urls2=[
# METHOD, URL, expected tuple
("GET","http://atpic.com/sitemap.xml",('get_atpic_com_sitemap_xml', 'GET atpic.com/sitemap.xml', {}) ),
("GET","http://atpic.com/favicon.ico",('get_atpic_com_favicon_ico', 'GET atpic.com/favicon.ico', {}) ), # or alias?
("GET","http://atpic.com", ('get_atpic_com', 'GET atpic.com', {}) ),
("GET","http://atpic.com/", ('get_atpic_com', 'GET atpic.com', {}) ),
("GET","http://atpic.com/user", ('get_atpic_com_user', 'GET atpic.com/user', {}) ),
("GET","http://atpic.com/gallery", ('get_atpic_com_gallery', 'GET atpic.com/gallery', {}) ),
("GET","http://atpic.com/gallery/53", ('get_atpic_com_gallery__id', 'GET atpic.com/gallery/:id', {'id': '53'}) ),
("GET","http://atpic.com/gallery/53/somesecret", ('get_atpic_com_gallery__id__secret', 'GET atpic.com/gallery/:id/:secret', {'id': '53' , 'secret':'somesecret'}) ),
("GET","http://atpic.com/pic", ('get_atpic_com_pic', 'GET atpic.com/pic', {}) ),
("GET","http://atpic.com/pic/", ('get_atpic_com_pic', 'GET atpic.com/pic', {}) ),
("GET","http://atpic.com/pic/1", ('get_atpic_com_pic__id', 'GET atpic.com/pic/:id', {'id': '1'}) ),
("GET","http://atpic.com/pic/1/somesecret", ('get_atpic_com_pic__id__secret', 'GET atpic.com/pic/:id/:secret', {'id': '1', 'secret':'somesecret'}) ),
("GET","http://atpic.com/pm", ('get_atpic_com_pm', 'GET atpic.com/pm', {}) ),
("GET","http://atpic.com/buy", ('get_atpic_com_buy', 'GET atpic.com/buy', {}) ),
("GET","http://atpic.com/pay", ('get_atpic_com_pay', 'GET atpic.com/pay', {}) ),
("GET","http://atpic.com/phrase", ('get_atpic_com_phrase', 'GET atpic.com/phrase', {}) ),
("GET","http://atpic.com/tag", ('get_atpic_com_tag', 'GET atpic.com/tag', {}) ),
("GET","http://atpic.com/faq", ('get_atpic_com_faq', 'GET atpic.com/faq', {}) ),
("GET","http://atpic.com/news", ('get_atpic_com_news', 'GET atpic.com/news', {}) ),
("GET","http://atpic.com/wiki", ('get_atpic_com_wiki', 'GET atpic.com/wiki', {}) ),
("GET","http://atpic.com/du", ('get_atpic_com_du', 'GET atpic.com/du', {}) ),


("GET","http://atpic.com/calendar", ('get_atpic_com_calendar', 'GET atpic.com/calendar', {}) ),
("GET","http://atpic.com/top", ('get_atpic_com_top', 'GET atpic.com/top', {}) ),
("GET","http://atpic.com/random", ('get_atpic_com_random', 'GET atpic.com/random', {}) ),
("GET","http://atpic.com/tagcloud", ('get_atpic_com_tagcloud', 'GET atpic.com/tagcloud', {}) ),



("GET","http://atpic.com/contact", ('get_atpic_com_contact', 'GET atpic.com/contact', {}) ),




("GET","http://atpic.com/alex", ('get_atpic_com__uname', 'GET atpic.com/:uname', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/maps", ('get_atpic_com__uname_maps', 'GET atpic.com/:uname/maps', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/google", ('get_atpic_com__uname_google', 'GET atpic.com/:uname/google', {'uname': 'alex'}) ),


("GET","http://atpic.com/alex/tree", ('get_atpic_com__uname_tree', 'GET atpic.com/:uname/tree', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/tree/france", ('get_atpic_com__uname_tree__tree', 'GET atpic.com/:uname/tree/:tree', {'uname': 'alex', 'tree': '/france'}) ),
("GET","http://atpic.com/alex/tree/france/paris", ('get_atpic_com__uname_tree__tree', 'GET atpic.com/:uname/tree/:tree', {'uname': 'alex', 'tree': '/france/paris'}) ),
("GET","http://atpic.com/alex/tree/france/paris/eiffel_tower.html", ('get_atpic_com__uname_tree__tree', 'GET atpic.com/:uname/tree/:tree', {'uname': 'alex', 'tree': '/france/paris/eiffel_tower.html'}) ),


("GET","http://atpic.com/alex/contact", ('get_atpic_com__uname_contact', 'GET atpic.com/:uname/contact', {'uname': 'alex'}) ),





("GET","http://atpic.com/alex/blog", ('get_atpic_com__uname_blog', 'GET atpic.com/:uname/blog', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/blog/2010", ('get_atpic_com__uname_blog__year', 'GET atpic.com/:uname/blog/:year', {'uname': 'alex', 'year': '2010'}) ),
("GET","http://atpic.com/alex/blog/2010/12", ('get_atpic_com__uname_blog__year__month', 'GET atpic.com/:uname/blog/:year/:month', {'uname': 'alex', 'month': '12', 'year': '2010'}) ),
("GET","http://atpic.com/alex/blog/2010/12/31", ('get_atpic_com__uname_blog__year__month__day', 'GET atpic.com/:uname/blog/:year/:month/:day', {'uname': 'alex', 'month': '12', 'day': '31', 'year': '2010'}) ),



("GET","http://atpic.com/alex/calendar", ('get_atpic_com__uname_calendar', 'GET atpic.com/:uname/calendar', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/calendar/2010", ('get_atpic_com__uname_calendar__year', 'GET atpic.com/:uname/calendar/:year', {'uname': 'alex', 'year': '2010'}) ),
("GET","http://atpic.com/alex/calendar/2010/12", ('get_atpic_com__uname_calendar__year__month', 'GET atpic.com/:uname/calendar/:year/:month', {'uname': 'alex', 'month': '12', 'year': '2010'}) ),
("GET","http://atpic.com/alex/calendar/2010/12/31", ('get_atpic_com__uname_calendar__year__month__day', 'GET atpic.com/:uname/calendar/:year/:month/:day', {'uname': 'alex', 'month': '12', 'day': '31', 'year': '2010'}) ),
("GET","http://atpic.com/alex/calendar", ('get_atpic_com__uname_calendar', 'GET atpic.com/:uname/calendar', {'uname': 'alex'}) ),





("GET","http://atpic.com/alex/top", ('get_atpic_com__uname_top', 'GET atpic.com/:uname/top', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/random", ('get_atpic_com__uname_random', 'GET atpic.com/:uname/random', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/friends", ('get_atpic_com__uname_friends', 'GET atpic.com/:uname/friends', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/contact", ('get_atpic_com__uname_contact', 'GET atpic.com/:uname/contact', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/du", ('get_atpic_com__uname_du', 'GET atpic.com/:uname/du', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/pm", ('get_atpic_com__uname_pm', 'GET atpic.com/:uname/pm', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/gallery", ('get_atpic_com__uname_gallery', 'GET atpic.com/:uname/gallery', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/buy", ('get_atpic_com__uname_buy', 'GET atpic.com/:uname/buy', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/tag", ('get_atpic_com__uname_tag', 'GET atpic.com/:uname/tag', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/phrase", ('get_atpic_com__uname_phrase', 'GET atpic.com/:uname/phrase', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/pm", ('get_atpic_com__uname_pm', 'GET atpic.com/:uname/pm', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/du", ('get_atpic_com__uname_du', 'GET atpic.com/:uname/du', {'uname': 'alex'}) ),
("GET","http://atpic.com/alex/audit", ('get_atpic_com__uname_audit', 'GET atpic.com/:uname/audit', {'uname': 'alex'}) ),


# sell dns

("GET","http://adns.com/tree", ('get__selldns_tree', 'GET :selldns/tree', {'dns': 'adns.com'}) ),
("GET","http://adns.com/tree/france", ('get__selldns_tree__tree', 'GET :selldns/tree/:tree', {'tree': '/france', 'dns': 'adns.com'}) ),
("GET","http://adns.com/tree/france/paris", ('get__selldns_tree__tree', 'GET :selldns/tree/:tree', {'tree': '/france/paris', 'dns': 'adns.com'}) ),
("GET","http://adns.com/tree/france/paris/eiffel_tower.html", ('get__selldns_tree__tree', 'GET :selldns/tree/:tree', {'tree': '/france/paris/eiffel_tower.html', 'dns': 'adns.com'}) ),


("GET","http://adns.com/contact", ('get__selldns_contact', 'GET :selldns/contact', {'dns': 'adns.com'}) ),

("GET","http://adns.com/blog", ('get__selldns_blog', 'GET :selldns/blog', {'dns': 'adns.com'}) ),
("GET","http://adns.com/blog/2010", ('get__selldns_blog__year', 'GET :selldns/blog/:year', {'dns': 'adns.com', 'year': '2010'}) ),
("GET","http://adns.com/blog/2010/12", ('get__selldns_blog__year__month', 'GET :selldns/blog/:year/:month', {'month': '12', 'dns': 'adns.com', 'year': '2010'}) ),
("GET","http://adns.com/blog/2010/12/31", ('get__selldns_blog__year__month__day', 'GET :selldns/blog/:year/:month/:day', {'month': '12', 'day': '31', 'dns': 'adns.com', 'year': '2010'}) ),



("GET","http://adns.com/calendar", ('get__selldns_calendar', 'GET :selldns/calendar', {'dns': 'adns.com'}) ),
("GET","http://adns.com/calendar/2010", ('get__selldns_calendar__year', 'GET :selldns/calendar/:year', {'dns': 'adns.com', 'year': '2010'}) ),
("GET","http://adns.com/calendar/2010/12", ('get__selldns_calendar__year__month', 'GET :selldns/calendar/:year/:month', {'month': '12', 'dns': 'adns.com', 'year': '2010'}) ),
("GET","http://adns.com/calendar/2010/12/31", ('get__selldns_calendar__year__month__day', 'GET :selldns/calendar/:year/:month/:day', {'month': '12', 'day': '31', 'dns': 'adns.com', 'year': '2010'}) ),




# legacy
("GET","http://atpic.com/fr", ('redir', 'http://atpic.com/', {}) ),
("GET","http://atpic.com/fr/1", ('redir', 'http://atpic.com/1', {}) ),
("GET","http://atpic.com/1", ('redir', 'http://atpic.com/user/1', {}) ),
("GET","http://pic.atpic.com/1", ('redir', 'http://atpic.com/pic/1', {'legacyobject': 'pic', 'id': '1'}) ),
("GET","http://pic.atpic.com/fr/1", ('redir', 'http://atpic.com/pic/1', {'legacyobject': 'pic', 'id': '1'}) ),
("GET","http://gallery.atpic.com/1", ('redir', 'http://atpic.com/gallery/1', {'legacyobject': 'gallery', 'id': '1'}) ),
("GET","http://gallery.atpic.com/fr/1", ('redir', 'http://atpic.com/gallery/1', {'legacyobject': 'gallery', 'id': '1'}) ),
("GET","http://pm.atpic.com", ('redir', 'http://atpic.com/pm', {'legacyobject': 'pm'}) ),
("GET","http://du.atpic.com", ('redir', 'http://atpic.com/du', {'legacyobject': 'du'}) ),
("GET","http://wiki.atpic.com", ('redir', 'http://atpic.com/wiki', {'legacyobject': 'wiki'}) ),
("GET","http://faq.atpic.com", ('redir', 'http://atpic.com/faq', {'legacyobject': 'faq'}) ),
("GET","http://alex.atpic.com/", ('redir', 'http://atpic.com/alex', {'uname': 'alex'}) ),
("GET","http://alex.atpic.com", ('redir', 'http://atpic.com/alex', {'uname': 'alex'}) ),

("POST","http://user1.atpic.com/artist/post", ('post__disktier_artist_post', 'POST :disktier/artist/post', {}) ),
("POST","http://user1.atpic.com/gallery/delete", ('post__disktier_gallery_delete', 'POST :disktier/gallery/delete', {}) ),
("POST","http://user1.atpic.com/gallery/post", ('post__disktier_gallery_post', 'POST :disktier/gallery/post', {}) ),
("POST","http://user1.atpic.com/pic/exif", ('post__disktier_pic_exif', 'POST :disktier/pic/exif', {}) ),
("POST","http://user1.atpic.com/pic/size", ('post__disktier_pic_size', 'POST :disktier/pic/size', {}) ),
("POST","http://user1.atpic.com/pic/sizeb", ('post__disktier_pic_sizeb', 'POST :disktier/pic/sizeb', {}) ),
("POST","http://user1.atpic.com/pic/delete", ('post__disktier_pic_delete', 'POST :disktier/pic/delete', {}) ),
("POST","http://user1.atpic.com/pic/post", ('post__disktier_pic_post', 'POST :disktier/pic/post', {}) ),
("POST","http://user1.atpic.com/pic/rotate", ('post__disktier_pic_rotate', 'POST :disktier/pic/rotate', {}) ),
("POST","http://user1.atpic.com/pic/put", ('post__disktier_pic_put', 'POST :disktier/pic/put', {}) ),
("POST","http://user1.atpic.com/pic/chown", ('post__disktier_pic_chown', 'POST :disktier/pic/chown', {}) ),
("POST","http://user1.atpic.com/ftp", ('post__disktier_ftp', 'POST :disktier/ftp', {}) ),
("POST","http://user1.atpic.com/quota", ('post__disktier_quota', 'POST :disktier/quota', {}) ),
("POST","http://user1.atpic.com/secret/put", ('post__disktier_secret_put', 'POST :disktier/secret/put', {}) )
,
("GET","http://atpic.com/gallery/post", ('get_atpic_com_gallery_post', 'GET atpic.com/gallery/post', {}) ),
("GET","http://atpic.com/gallery/53/delete", ('get_atpic_com_gallery__id_delete', 'GET atpic.com/gallery/:id/delete', {'id': '53'}) ),
("GET","http://atpic.com/gallery/53/put", ('get_atpic_com_gallery__id_put', 'GET atpic.com/gallery/:id/put', {'id': '53'}) ),
("POST","http://atpic.com/gallery", ('post_atpic_com_gallery', 'POST atpic.com/gallery', {}) ),
("POST","http://atpic.com/gallery/53/delete", ('post_atpic_com_gallery__id_delete', 'POST atpic.com/gallery/:id/delete', {'id': '53'}) ),
("POST","http://atpic.com/gallery/53/put", ('post_atpic_com_gallery__id_put', 'POST atpic.com/gallery/:id/put', {'id': '53'}) ),
("PUT","http://atpic.com/gallery/53", ('put_atpic_com_gallery__id', 'PUT atpic.com/gallery/:id', {'id': '53'}) ),
("DELETE","http://atpic.com/gallery/53", ('delete_atpic_com_gallery__id', 'DELETE atpic.com/gallery/:id', {'id': '53'}) ),

("GET","http://atpic.com/pic/post", ('get_atpic_com_pic_post', 'GET atpic.com/pic/post', {}) ),
("GET","http://atpic.com/pic/7889/delete", ('get_atpic_com_pic__id_delete', 'GET atpic.com/pic/:id/delete', {'id': '7889'}) ),
("GET","http://atpic.com/pic/7889/put", ('get_atpic_com_pic__id_put', 'GET atpic.com/pic/:id/put', {'id': '7889'}) ),
("POST","http://alex.atpic.com/pic", ('post__uname_atpic_com_pic', 'POST :uname.atpic.com/pic', {'uname': 'alex'}) ),
("POST","http://alex.atpic.com/pic/7889/delete", ('post__uname_atpic_com_pic__id_delete', 'POST :uname.atpic.com/pic/:id/delete', {'uname': 'alex', 'id': '7889'}) ),
("POST","http://alex.atpic.com/pic/7889/put", ('post__uname_atpic_com_pic__id_put', 'POST :uname.atpic.com/pic/:id/put', {'uname': 'alex', 'id': '7889'}) ),
("PUT","http://alex.atpic.com/pic/7889", ('put__uname_atpic_com_pic__id', 'PUT :uname.atpic.com/pic/:id', {'uname': 'alex', 'id': '7889'}) ),
("DELETE","http://alex.atpic.com/pic/7889", ('delete__uname_atpic_com_pic__id', 'DELETE :uname.atpic.com/pic/:id', {'uname': 'alex', 'id': '7889'}) ),

("GET","http://atpic.com/pm", ('get_atpic_com_pm', 'GET atpic.com/pm', {}) ),
("GET","http://atpic.com/pm/88", ('get_atpic_com_pm__id', 'GET atpic.com/pm/:id', {'id': '88'}) ),
("GET","http://atpic.com/pm/post", ('get_atpic_com_pm_post', 'GET atpic.com/pm/post', {}) ),
("GET","http://atpic.com/pm/88/delete", ('get_atpic_com_pm__id_delete', 'GET atpic.com/pm/:id/delete', {'id': '88'}) ),
("GET","http://atpic.com/pm/88/put", ('get_atpic_com_pm__id_put', 'GET atpic.com/pm/:id/put', {'id': '88'}) ),
("POST","http://atpic.com/pm", ('post_atpic_com_pm', 'POST atpic.com/pm', {}) ),
("POST","http://atpic.com/pm/88/delete", ('post_atpic_com_pm__id_delete', 'POST atpic.com/pm/:id/delete', {'id': '88'}) ),
("POST","http://atpic.com/pm/88/put", ('post_atpic_com_pm__id_put', 'POST atpic.com/pm/:id/put', {'id': '88'}) ),
("PUT","http://atpic.com/pm/88", ('put_atpic_com_pm__id', 'PUT atpic.com/pm/:id', {'id': '88'}) ),
("DELETE","http://atpic.com/pm/88", ('delete_atpic_com_pm__id', 'DELETE atpic.com/pm/:id', {'id': '88'}) ),




("GET","http://atpic.com/phrase", ('get_atpic_com_phrase', 'GET atpic.com/phrase', {}) ),
("GET","http://atpic.com/phrase/712", ('get_atpic_com_phrase__id', 'GET atpic.com/phrase/:id', {'id': '712'}) ),
("GET","http://atpic.com/phrase/post", ('get_atpic_com_phrase_post', 'GET atpic.com/phrase/post', {}) ),
("GET","http://atpic.com/phrase/712/delete", ('get_atpic_com_phrase__id_delete', 'GET atpic.com/phrase/:id/delete', {'id': '712'}) ),
("GET","http://atpic.com/phrase/712/put", ('get_atpic_com_phrase__id_put', 'GET atpic.com/phrase/:id/put', {'id': '712'}) ),
("POST","http://atpic.com/phrase", ('post_atpic_com_phrase', 'POST atpic.com/phrase', {}) ),
("POST","http://atpic.com/phrase/712/delete", ('post_atpic_com_phrase__id_delete', 'POST atpic.com/phrase/:id/delete', {'id': '712'}) ),
("POST","http://atpic.com/phrase/712/put", ('post_atpic_com_phrase__id_put', 'POST atpic.com/phrase/:id/put', {'id': '712'}) ),
("PUT","http://atpic.com/phrase/712", ('put_atpic_com_phrase__id', 'PUT atpic.com/phrase/:id', {'id': '712'}) ),
("DELETE","http://atpic.com/phrase/712", ('delete_atpic_com_phrase__id', 'DELETE atpic.com/phrase/:id', {'id': '712'}) ),



("GET","http://atpic.com/comment", ('get_atpic_com_comment', 'GET atpic.com/comment', {}) ),
("GET","http://atpic.com/comment/712", ('get_atpic_com_comment__id', 'GET atpic.com/comment/:id', {'id': '712'}) ),
("GET","http://atpic.com/comment/post", ('get_atpic_com_comment_post', 'GET atpic.com/comment/post', {}) ),
("GET","http://atpic.com/comment/712/delete", ('get_atpic_com_comment__id_delete', 'GET atpic.com/comment/:id/delete', {'id': '712'}) ),
("GET","http://atpic.com/comment/712/put", ('get_atpic_com_comment__id_put', 'GET atpic.com/comment/:id/put', {'id': '712'}) ),
("POST","http://atpic.com/comment", ('post_atpic_com_comment', 'POST atpic.com/comment', {}) ),
("POST","http://atpic.com/comment/712/delete", ('post_atpic_com_comment__id_delete', 'POST atpic.com/comment/:id/delete', {'id': '712'}) ),
("POST","http://atpic.com/comment/712/put", ('post_atpic_com_comment__id_put', 'POST atpic.com/comment/:id/put', {'id': '712'}) ),
("PUT","http://atpic.com/comment/712", ('put_atpic_com_comment__id', 'PUT atpic.com/comment/:id', {'id': '712'}) ),
("DELETE","http://atpic.com/comment/712", ('delete_atpic_com_comment__id', 'DELETE atpic.com/comment/:id', {'id': '712'}) ),



("GET","http://atpic.com/user", ('get_atpic_com_user', 'GET atpic.com/user', {}) ),
("GET","http://atpic.com/user/961", ('get_atpic_com_user__id', 'GET atpic.com/user/:id', {'id': '961'}) ),
("GET","http://atpic.com/user/post", ('get_atpic_com_user_post', 'GET atpic.com/user/post', {}) ),
("GET","http://atpic.com/user/961/delete", ('get_atpic_com_user__id_delete', 'GET atpic.com/user/:id/delete', {'id': '961'}) ),
("GET","http://atpic.com/user/961/put", ('get_atpic_com_user__id_put', 'GET atpic.com/user/:id/put', {'id': '961'}) ),
("POST","http://atpic.com/user", ('post_atpic_com_user', 'POST atpic.com/user', {}) ),
("POST","http://atpic.com/user/961/delete", ('post_atpic_com_user__id_delete', 'POST atpic.com/user/:id/delete', {'id': '961'}) ),
("POST","http://atpic.com/user/961/put", ('post_atpic_com_user__id_put', 'POST atpic.com/user/:id/put', {'id': '961'}) ),
("PUT","http://atpic.com/user/961", ('put_atpic_com_user__id', 'PUT atpic.com/user/:id', {'id': '961'}) ),
("DELETE","http://atpic.com/user/961", ('delete_atpic_com_user__id', 'DELETE atpic.com/user/:id', {'id': '961'}) ),




("GET","http://atpic.com/vote", ('get_atpic_com_vote', 'GET atpic.com/vote', {}) ),
("GET","http://atpic.com/vote/961", ('get_atpic_com_vote__id', 'GET atpic.com/vote/:id', {'id': '961'}) ),
("GET","http://atpic.com/vote/post", ('get_atpic_com_vote_post', 'GET atpic.com/vote/post', {}) ),
("GET","http://atpic.com/vote/961/delete", ('get_atpic_com_vote__id_delete', 'GET atpic.com/vote/:id/delete', {'id': '961'}) ),
("GET","http://atpic.com/vote/961/put", ('get_atpic_com_vote__id_put', 'GET atpic.com/vote/:id/put', {'id': '961'}) ),
("POST","http://atpic.com/vote", ('post_atpic_com_vote', 'POST atpic.com/vote', {}) ),
("POST","http://atpic.com/vote/961/delete", ('post_atpic_com_vote__id_delete', 'POST atpic.com/vote/:id/delete', {'id': '961'}) ),
("POST","http://atpic.com/vote/961/put", ('post_atpic_com_vote__id_put', 'POST atpic.com/vote/:id/put', {'id': '961'}) ),
("PUT","http://atpic.com/vote/961", ('put_atpic_com_vote__id', 'PUT atpic.com/vote/:id', {'id': '961'}) ),
("DELETE","http://atpic.com/vote/961", ('delete_atpic_com_vote__id', 'DELETE atpic.com/vote/:id', {'id': '961'}) ),




("GET","http://atpic.com/tag", ('get_atpic_com_tag', 'GET atpic.com/tag', {}) ),
("GET","http://atpic.com/tag/458", ('get_atpic_com_tag__id', 'GET atpic.com/tag/:id', { 'id': '458'}) ),
("GET","http://atpic.com/tag/post", ('get_atpic_com_tag_post', 'GET atpic.com/tag/post', {}) ),
("GET","http://atpic.com/tag/458/delete", ('get_atpic_com_tag__id_delete', 'GET atpic.com/tag/:id/delete', { 'id': '458'}) ),
("GET","http://atpic.com/tag/458/put", ('get_atpic_com_tag__id_put', 'GET atpic.com/tag/:id/put', { 'id': '458'}) ),
("POST","http://atpic.com/tag", ('post_atpic_com_tag', 'POST atpic.com/tag', {}) ),
("POST","http://atpic.com/tag/458/delete", ('post_atpic_com_tag__id_delete', 'POST atpic.com/tag/:id/delete', { 'id': '458'}) ),
("POST","http://atpic.com/tag/458/put", ('post_atpic_com_tag__id_put', 'POST atpic.com/tag/:id/put', { 'id': '458'}) ),
("PUT","http://atpic.com/tag/458", ('put_atpic_com_tag__id', 'PUT atpic.com/tag/:id', { 'id': '458'}) ),
("DELETE","http://atpic.com/tag/458", ('delete_atpic_com_tag__id', 'DELETE atpic.com/tag/:id', { 'id': '458'}) ),



("GET","http://atpic.com/buy", ('get_atpic_com_buy', 'GET atpic.com/buy', {}) ),
("GET","http://atpic.com/buy/666", ('get_atpic_com_buy__id', 'GET atpic.com/buy/:id', {'id': '666'}) ),
("GET","http://atpic.com/buy/post", ('get_atpic_com_buy_post', 'GET atpic.com/buy/post', {}) ),
("GET","http://atpic.com/buy/666/delete", ('get_atpic_com_buy__id_delete', 'GET atpic.com/buy/:id/delete', {'id': '666'}) ),
("GET","http://atpic.com/buy/666/put", ('get_atpic_com_buy__id_put', 'GET atpic.com/buy/:id/put', {'id': '666'}) ),
("POST","http://atpic.com/buy", ('post_atpic_com_buy', 'POST atpic.com/buy', {}) ),
("POST","http://atpic.com/buy/666/delete", ('post_atpic_com_buy__id_delete', 'POST atpic.com/buy/:id/delete', {'id': '666'}) ),
("POST","http://atpic.com/buy/666/put", ('post_atpic_com_buy__id_put', 'POST atpic.com/buy/:id/put', {'id': '666'}) ),
("PUT","http://atpic.com/buy/666", ('put_atpic_com_buy__id', 'PUT atpic.com/buy/:id', {'id': '666'}) ),
("DELETE","http://atpic.com/buy/666", ('delete_atpic_com_buy__id', 'DELETE atpic.com/buy/:id', {'id': '666'}) ),



("GET","http://atpic.com/pay", ('get_atpic_com_pay', 'GET atpic.com/pay', {}) ),
("GET","http://atpic.com/pay/789", ('get_atpic_com_pay__id', 'GET atpic.com/pay/:id', {'id': '789'}) ),
("GET","http://atpic.com/pay/post", ('get_atpic_com_pay_post', 'GET atpic.com/pay/post', {}) ),
("GET","http://atpic.com/pay/789/delete", ('get_atpic_com_pay__id_delete', 'GET atpic.com/pay/:id/delete', {'id': '789'}) ),
("GET","http://atpic.com/pay/789/put", ('get_atpic_com_pay__id_put', 'GET atpic.com/pay/:id/put', {'id': '789'}) ),
("POST","http://atpic.com/pay", ('post_atpic_com_pay', 'POST atpic.com/pay', {}) ),
("POST","http://atpic.com/pay/789/delete", ('post_atpic_com_pay__id_delete', 'POST atpic.com/pay/:id/delete', {'id': '789'}) ),
("POST","http://atpic.com/pay/789/put", ('post_atpic_com_pay__id_put', 'POST atpic.com/pay/:id/put', {'id': '789'}) ),
("PUT","http://atpic.com/pay/789", ('put_atpic_com_pay__id', 'PUT atpic.com/pay/:id', {'id': '789'}) ),
("DELETE","http://atpic.com/pay/789", ('delete_atpic_com_pay__id', 'DELETE atpic.com/pay/:id', {'id': '789'}) ),




("GET","http://atpic.com/wiki", ('get_atpic_com_wiki', 'GET atpic.com/wiki', {}) ),
("GET","http://atpic.com/wiki/159", ('get_atpic_com_wiki__id', 'GET atpic.com/wiki/:id', {'id': '159'}) ),
("GET","http://atpic.com/wiki/post", ('get_atpic_com_wiki_post', 'GET atpic.com/wiki/post', {}) ),
("GET","http://atpic.com/wiki/159/delete", ('get_atpic_com_wiki__id_delete', 'GET atpic.com/wiki/:id/delete', {'id': '159'}) ),
("GET","http://atpic.com/wiki/159/put", ('get_atpic_com_wiki__id_put', 'GET atpic.com/wiki/:id/put', {'id': '159'}) ),
("POST","http://atpic.com/wiki", ('post_atpic_com_wiki', 'POST atpic.com/wiki', {}) ),
("POST","http://atpic.com/wiki/159/delete", ('post_atpic_com_wiki__id_delete', 'POST atpic.com/wiki/:id/delete', {'id': '159'}) ),
("POST","http://atpic.com/wiki/159/put", ('post_atpic_com_wiki__id_put', 'POST atpic.com/wiki/:id/put', {'id': '159'}) ),
("PUT","http://atpic.com/wiki/159", ('put_atpic_com_wiki__id', 'PUT atpic.com/wiki/:id', {'id': '159'}) ),
("DELETE","http://atpic.com/wiki/159", ('delete_atpic_com_wiki__id', 'DELETE atpic.com/wiki/:id', {'id': '159'}) ),




("GET","http://atpic.com/news", ('get_atpic_com_news', 'GET atpic.com/news', {}) ),
("GET","http://atpic.com/news/13", ('get_atpic_com_news__id', 'GET atpic.com/news/:id', {'id': '13'}) ),
("GET","http://atpic.com/news/post", ('get_atpic_com_news_post', 'GET atpic.com/news/post', {}) ),
("GET","http://atpic.com/news/13/delete", ('get_atpic_com_news__id_delete', 'GET atpic.com/news/:id/delete', {'id': '13'}) ),
("GET","http://atpic.com/news/13/put", ('get_atpic_com_news__id_put', 'GET atpic.com/news/:id/put', {'id': '13'}) ),
("POST","http://atpic.com/news", ('post_atpic_com_news', 'POST atpic.com/news', {}) ),
("POST","http://atpic.com/news/13/delete", ('post_atpic_com_news__id_delete', 'POST atpic.com/news/:id/delete', {'id': '13'}) ),
("POST","http://atpic.com/news/13/put", ('post_atpic_com_news__id_put', 'POST atpic.com/news/:id/put', {'id': '13'}) ),
("PUT","http://atpic.com/news/13", ('put_atpic_com_news__id', 'PUT atpic.com/news/:id', {'id': '13'}) ),
("DELETE","http://atpic.com/news/13", ('delete_atpic_com_news__id', 'DELETE atpic.com/news/:id', {'id': '13'}) ),




("GET","http://atpic.com/faq", ('get_atpic_com_faq', 'GET atpic.com/faq', {}) ),
("GET","http://atpic.com/faq/698", ('get_atpic_com_faq__id', 'GET atpic.com/faq/:id', {'id': '698'}) ),
("GET","http://atpic.com/faq/post", ('get_atpic_com_faq_post', 'GET atpic.com/faq/post', {}) ),
("GET","http://atpic.com/faq/698/delete", ('get_atpic_com_faq__id_delete', 'GET atpic.com/faq/:id/delete', {'id': '698'}) ),
("GET","http://atpic.com/faq/698/put", ('get_atpic_com_faq__id_put', 'GET atpic.com/faq/:id/put', {'id': '698'}) ),
("POST","http://atpic.com/faq", ('post_atpic_com_faq', 'POST atpic.com/faq', {}) ),
("POST","http://atpic.com/faq/698/delete", ('post_atpic_com_faq__id_delete', 'POST atpic.com/faq/:id/delete', {'id': '698'}) ),
("POST","http://atpic.com/faq/698/put", ('post_atpic_com_faq__id_put', 'POST atpic.com/faq/:id/put', {'id': '698'}) ),
("PUT","http://atpic.com/faq/698", ('put_atpic_com_faq__id', 'PUT atpic.com/faq/:id', {'id': '698'}) ),
("DELETE","http://atpic.com/faq/698", ('delete_atpic_com_faq__id', 'DELETE atpic.com/faq/:id', {'id': '698'}) ),




("GET","http://atpic.com/friend", ('get_atpic_com_friend', 'GET atpic.com/friend', {}) ),
("GET","http://atpic.com/friend/698", ('get_atpic_com_friend__id', 'GET atpic.com/friend/:id', {'id': '698'}) ),
("GET","http://atpic.com/friend/post", ('get_atpic_com_friend_post', 'GET atpic.com/friend/post', {}) ),
("GET","http://atpic.com/friend/698/delete", ('get_atpic_com_friend__id_delete', 'GET atpic.com/friend/:id/delete', {'id': '698'}) ),
("GET","http://atpic.com/friend/698/put", ('get_atpic_com_friend__id_put', 'GET atpic.com/friend/:id/put', {'id': '698'}) ),
("POST","http://atpic.com/friend", ('post_atpic_com_friend', 'POST atpic.com/friend', {}) ),
("POST","http://atpic.com/friend/698/delete", ('post_atpic_com_friend__id_delete', 'POST atpic.com/friend/:id/delete', {'id': '698'}) ),
("POST","http://atpic.com/friend/698/put", ('post_atpic_com_friend__id_put', 'POST atpic.com/friend/:id/put', {'id': '698'}) ),
("PUT","http://atpic.com/friend/698", ('put_atpic_com_friend__id', 'PUT atpic.com/friend/:id', {'id': '698'}) ),
("DELETE","http://atpic.com/friend/698", ('delete_atpic_com_friend__id', 'DELETE atpic.com/friend/:id', {'id': '698'}) ),



("GET","http://atpic.com/follower", ('get_atpic_com_follower', 'GET atpic.com/follower', {}) ),
("GET","http://atpic.com/follower/698", ('get_atpic_com_follower__id', 'GET atpic.com/follower/:id', {'id': '698'}) ),
("GET","http://atpic.com/follower/post", ('get_atpic_com_follower_post', 'GET atpic.com/follower/post', {}) ),
("GET","http://atpic.com/follower/698/delete", ('get_atpic_com_follower__id_delete', 'GET atpic.com/follower/:id/delete', {'id': '698'}) ),
("GET","http://atpic.com/follower/698/put", ('get_atpic_com_follower__id_put', 'GET atpic.com/follower/:id/put', {'id': '698'}) ),
("POST","http://atpic.com/follower", ('post_atpic_com_follower', 'POST atpic.com/follower', {}) ),
("POST","http://atpic.com/follower/698/delete", ('post_atpic_com_follower__id_delete', 'POST atpic.com/follower/:id/delete', {'id': '698'}) ),
("POST","http://atpic.com/follower/698/put", ('post_atpic_com_follower__id_put', 'POST atpic.com/follower/:id/put', {'id': '698'}) ),
("PUT","http://atpic.com/follower/698", ('put_atpic_com_follower__id', 'PUT atpic.com/follower/:id', {'id': '698'}) ),
("DELETE","http://atpic.com/follower/698", ('delete_atpic_com_follower__id', 'DELETE atpic.com/follower/:id', {'id': '698'}) ),



# blog on root
("GET","http://atpic.com/blog", ('get_atpic_com_blog', 'GET atpic.com/blog', {}) ),
("GET","http://atpic.com/blog/2011", ('get_atpic_com_blog__year', 'GET atpic.com/blog/:year', {'year': '2011'}) ),
("GET","http://atpic.com/blog/2011/12", ('get_atpic_com_blog__year__month', 'GET atpic.com/blog/:year/:month', {'month': '12', 'year': '2011'}) ),
("GET","http://atpic.com/blog/2011/12/31", ('get_atpic_com_blog__year__month__day', 'GET atpic.com/blog/:year/:month/:day', {'month': '12', 'day': '31', 'year': '2011'}) ),




# calendar on root

("GET","http://atpic.com/calendar", ('get_atpic_com_calendar', 'GET atpic.com/calendar', {}) ),
("GET","http://atpic.com/calendar/2011", ('get_atpic_com_calendar__year', 'GET atpic.com/calendar/:year', {'year': '2011'}) ),
("GET","http://atpic.com/calendar/2011/12", ('get_atpic_com_calendar__year__month', 'GET atpic.com/calendar/:year/:month', {'month': '12', 'year': '2011'}) ),
("GET","http://atpic.com/calendar/2011/12/31", ('get_atpic_com_calendar__year__month__day', 'GET atpic.com/calendar/:year/:month/:day', {'month': '12', 'day': '31', 'year': '2011'}) ),

]



class dispatcherURLtest(unittest.TestCase):
    """USER legacy urls"""
    def testMainURLsGET(self):
        i=0
        for url in urls2:
            i=i+1
            print("----%s -------------" % i)
            environ={}
            environ['REQUEST_METHOD']=url[0]
            print("%s %s" % (url[0],url[1]))
            urltuple=urllib.parse.urlsplit(url[1])
            # print urltuple
            environ['HTTP_HOST']=urltuple[1]
            environ['PATH_INFO']=urltuple[2]
            response=atpic.dispatcher.dispatcher(environ)
            print(response)
            print("FUNCTION",response[0])

            print('TESTENTRY("'+url[0]+'","'+url[1]+'",',response,'),')
            self.assertEqual(response,url[2])

    def NOtestgetid(self):
        for path in paths_id:
            print("%s ->" % (path))
            adic={}
            path,adic=atpic.dispatcher.get_id(path,adic)
            print("   %s, %s" % (path,adic))

    def NOtestgetid_legacy(self):
        for path in paths_id_legacy:
            print("%s ->" % (path))
            adic={}
            path,adic=atpic.dispatcher.get_id_legacy(path,adic)
            print("   %s, %s" % (path,adic))

    def NOtestgetymd(self):
        for path in paths_ymd:
            print("%s ->" % (path))
            adic={}
            path,adic=atpic.dispatcher.get_ymd(path,adic)
            print("   %s, %s" % (path,adic))

    def NONOtestgettree(self):
        for path in paths_tree:
            print("%s ->" % (path))
            adic={}
            path,adic=atpic.dispatcher.get_tree(path,adic)
            print("   %s, %s" % (path,adic))

    def NOtestgetudomain(self):
        for host in hosts:
            print("%s ->" % (host))
            adic={}
            host,adic=atpic.dispatcher.get_udomain(host,adic)
            print("   %s, %s" % (host,adic))

if __name__=="__main__":
    unittest.main()
