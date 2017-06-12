#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse


import atpic.dispatcher

"""
This scheme should allow user based SQL partitionning
Has also the cosmetical advantage of not ahaving /tag_g /tag_p
Note that in the url path you can have more than once the same object
In the sql mapping only once.
"""

fileurls=[



(b'GET', b'http://atpic.com', b'/forgot', b'get post atpiccom/forgot/', ([(b'atpiccom', None)], [(b'forgot', None)], [b'get',b'post'], b'anonymous')),
(b'POST', b'http://atpic.com', b'/forgot', b'post atpiccom/forgot/', ([(b'atpiccom', None)], [(b'forgot', None)], [b'post'], b'anonymous')),

(b'GET', b'http://atpic.com', b'/reset/xyzt', b'get post atpiccom/reset_', ([(b'atpiccom', None)], [(b'reset', b'xyzt')], [b'get',b'post'], b'authenticated')),
(b'POST', b'http://atpic.com', b'/reset/xyzt', b'post atpiccom/reset_', ([(b'atpiccom', None)], [(b'reset', b'xyzt')], [b'post'], b'authenticated')),





(b'GET', b'http://atpic.com', b'/robots.txt', b'get atpiccom/robots.txt/', ([(b'atpiccom', None)], [(b'robots.txt', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/robots.txt', b'get uname_robots.txt/', ([(b'uname', b'alex')], [(b'robots.txt', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/sitemap.xml', b'get atpiccom/sitemap.xml/', ([(b'atpiccom', None)], [(b'sitemap.xml', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/favicon.ico', b'get atpiccom/favicon.ico/', ([(b'atpiccom', None)], [(b'favicon.ico', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/dragdrop.js', b'get atpiccom/dragdrop.js/', ([(b'atpiccom', None)], [(b'dragdrop.js', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/dragdrop.js', b'get uname_dragdrop.js/', ([(b'uname', b'alex')], [(b'dragdrop.js', None)], [b'get'], b'anonymous')),



(b'***** home page *****',),
(b'GET', b'http://atpic.com', b'', b'get atpiccom/', ([(b'atpiccom', None)], [], [b'get'], b'anonymous')),
(b'GET', b'http://www.atpic.com', b'', b'get atpiccom/', ([(b'atpiccom', None)], [], [b'get'], b'anonymous')),
(b'*****GET API, use user-based SQL partition*****',),
(b'GET', b'http://atpic.com', b'/user', b'get atpiccom/user/', ([(b'atpiccom', None)], [(b'user', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'', b'get uname_', ([(b'uname', b'alex')], [], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery', b'get uname_gallery/', ([(b'uname', b'alex')], [(b'gallery', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23', b'get uname_gallery_', ([(b'uname', b'alex')], [(b'gallery', b'23')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic', b'get uname_gallery_pic/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152', b'get uname_gallery_pic_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/comment', b'get uname_comment/', ([(b'uname', b'alex')], [(b'comment', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/comment/6', b'get uname_comment_', ([(b'uname', b'alex')], [(b'comment', b'6')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/comment', b'get uname_gallery_comment/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/comment/59', b'get uname_gallery_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', b'59')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/tag', b'get uname_gallery_tag/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/tag/69', b'get uname_gallery_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', b'69')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/phrase', b'get uname_gallery_phrase/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/phrase/68', b'get uname_gallery_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', b'68')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment', b'get uname_gallery_pic_comment/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment/159', b'get uname_gallery_pic_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', b'159')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag', b'get uname_gallery_pic_tag/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag/169', b'get uname_gallery_pic_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', b'169')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase', b'get uname_gallery_pic_phrase/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase/168', b'get uname_gallery_pic_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', b'168')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/vote/169', b'get uname_gallery_pic_vote_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'vote', b'169')], [b'get'], b'anonymous')),
(b'****************',),
(b'GET', b'http://alex.atpic.com', b'/pmsent', b'get uname_pmsent/', ([(b'uname', b'alex')], [(b'pmsent', None)], [b'get'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/pmsent/58', b'get uname_pmsent_', ([(b'uname', b'alex')], [(b'pmsent', b'58')], [b'get'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/pm', b'get uname_pm/', ([(b'uname', b'alex')], [(b'pm', None)], [b'get'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/pm/59', b'get uname_pm_', ([(b'uname', b'alex')], [(b'pm', b'59')], [b'get'], b'owner')),
(b'****************',),
(b'GET', b'http://alex.atpic.com', b'/friend', b'get uname_friend/', ([(b'uname', b'alex')], [(b'friend', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/friend/44', b'get uname_friend_', ([(b'uname', b'alex')], [(b'friend', b'44')], [b'get'], b'anonymous')),
(b'****************',),
(b'GET', b'http://alex.atpic.com', b'/payment', b'get uname_payment/', ([(b'uname', b'alex')], [(b'payment', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/payment/57', b'get uname_payment_', ([(b'uname', b'alex')], [(b'payment', b'57')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/buy', b'get uname_buy/', ([(b'uname', b'alex')], [(b'buy', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/buy/157', b'get uname_buy_', ([(b'uname', b'alex')], [(b'buy', b'157')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/sell', b'get uname_sell/', ([(b'uname', b'alex')], [(b'sell', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/sell/157', b'get uname_sell_', ([(b'uname', b'alex')], [(b'sell', b'157')], [b'get'], b'anonymous')),
(b'****************',),
(b'GET', b'http://alex.atpic.com', b'/du', b'get uname_du/', ([(b'uname', b'alex')], [(b'du', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/preferences', b'get uname_preferences/', ([(b'uname', b'alex')], [(b'preferences', None)], [b'get'], b'anonymous')),
(b'****************',),
(b'****************',),
(b'****POST API, use user-based SQL partition*****',),
(b'****************',),
(b'POST', b'http://atpic.com', b'/user', b'post atpiccom/user/', ([(b'atpiccom', None)], [(b'user', None)], [b'post'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/user/post', b'get post atpiccom/user/', ([(b'atpiccom', None)], [(b'user', None)], [b'get', b'post'], b'anonymous')),
(b'POST', b'http://atpic.com', b'/user/post', b'post post atpiccom/user/', ([(b'atpiccom', None)], [(b'user', None)], [b'post', b'post'], b'anonymous')),
(b'****************',),
(b'GET', b'http://atpic.com', b'/user/1', b'get atpiccom/user_', ([(b'atpiccom', None)], [(b'user', b'1')], [b'get'], b'anonymous')),
(b'****************',),
(b'PUT', b'http://atpic.com', b'/user/1', b'put atpiccom/user_', ([(b'atpiccom', None)], [(b'user', b'1')], [b'put'], b'owner')),
(b'POST', b'http://atpic.com', b'/user/1/put', b'post put atpiccom/user_', ([(b'atpiccom', None)], [(b'user', b'1')], [b'post', b'put'], b'owner')),
(b'GET', b'http://atpic.com', b'/user/1/put', b'get put atpiccom/user_', ([(b'atpiccom', None)], [(b'user', b'1')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://atpic.com', b'/user/1', b'delete atpiccom/user_', ([(b'atpiccom', None)], [(b'user', b'1')], [b'delete'], b'owner')),
(b'POST', b'http://atpic.com', b'/user/1/delete', b'post delete atpiccom/user_', ([(b'atpiccom', None)], [(b'user', b'1')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://atpic.com', b'/user/1/delete', b'get delete atpiccom/user_', ([(b'atpiccom', None)], [(b'user', b'1')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery', b'post uname_gallery/', ([(b'uname', b'alex')], [(b'gallery', None)], [b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/post', b'get post uname_gallery/', ([(b'uname', b'alex')], [(b'gallery', None)], [b'get', b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/post', b'post post uname_gallery/', ([(b'uname', b'alex')], [(b'gallery', None)], [b'post', b'post'], b'owner')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23', b'put uname_gallery_', ([(b'uname', b'alex')], [(b'gallery', b'23')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/put', b'post put uname_gallery_', ([(b'uname', b'alex')], [(b'gallery', b'23')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/put', b'get put uname_gallery_', ([(b'uname', b'alex')], [(b'gallery', b'23')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/23', b'delete uname_gallery_', ([(b'uname', b'alex')], [(b'gallery', b'23')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/delete', b'post delete uname_gallery_', ([(b'uname', b'alex')], [(b'gallery', b'23')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/delete', b'get delete uname_gallery_', ([(b'uname', b'alex')], [(b'gallery', b'23')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic', b'post uname_gallery_pic/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', None)], [b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/post', b'get post uname_gallery_pic/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', None)], [b'get', b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/post', b'post post uname_gallery_pic/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', None)], [b'post', b'post'], b'owner')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23/pic/152', b'put uname_gallery_pic_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/put', b'post put uname_gallery_pic_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/put', b'get put uname_gallery_pic_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/23/pic/152', b'delete uname_gallery_pic_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/delete', b'post delete uname_gallery_pic_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/delete', b'get delete uname_gallery_pic_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/comment', b'post uname_comment/', ([(b'uname', b'alex')], [(b'comment', None)], [b'post'], b'authenticated')),
(b'GET', b'http://alex.atpic.com', b'/comment/post', b'get post uname_comment/', ([(b'uname', b'alex')], [(b'comment', None)], [b'get', b'post'], b'authenticated')),
(b'POST', b'http://alex.atpic.com', b'/comment/post', b'post post uname_comment/', ([(b'uname', b'alex')], [(b'comment', None)], [b'post', b'post'], b'authenticated')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/comment/6', b'put uname_comment_', ([(b'uname', b'alex')], [(b'comment', b'6')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/comment/6/put', b'post put uname_comment_', ([(b'uname', b'alex')], [(b'comment', b'6')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/comment/6/put', b'get put uname_comment_', ([(b'uname', b'alex')], [(b'comment', b'6')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/comment/6', b'delete uname_comment_', ([(b'uname', b'alex')], [(b'comment', b'6')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/comment/6/delete', b'post delete uname_comment_', ([(b'uname', b'alex')], [(b'comment', b'6')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/comment/6/delete', b'get delete uname_comment_', ([(b'uname', b'alex')], [(b'comment', b'6')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/comment', b'post uname_gallery_comment/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', None)], [b'post'], b'authenticated')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/comment/post', b'get post uname_gallery_comment/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', None)], [b'get', b'post'], b'authenticated')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/comment/post', b'post post uname_gallery_comment/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', None)], [b'post', b'post'], b'authenticated')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23/comment/59', b'put uname_gallery_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', b'59')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/comment/59/put', b'post put uname_gallery_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', b'59')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/comment/59/put', b'get put uname_gallery_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', b'59')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/23/comment/59', b'delete uname_gallery_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', b'59')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/comment/59/delete', b'post delete uname_gallery_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', b'59')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/comment/59/delete', b'get delete uname_gallery_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'comment', b'59')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/tag', b'post uname_gallery_tag/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', None)], [b'post'], b'authenticated')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/tag/post', b'get post uname_gallery_tag/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', None)], [b'get', b'post'], b'authenticated')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/tag/post', b'post post uname_gallery_tag/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', None)], [b'post', b'post'], b'authenticated')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23/tag/69', b'put uname_gallery_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', b'69')], [b'put'], b'author')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/tag/69/put', b'post put uname_gallery_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', b'69')], [b'post', b'put'], b'author')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/tag/69/put', b'get put uname_gallery_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', b'69')], [b'get', b'put'], b'author')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/23/tag/69', b'delete uname_gallery_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', b'69')], [b'delete'], b'author')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/tag/69/delete', b'post delete uname_gallery_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', b'69')], [b'post', b'delete'], b'author')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/tag/69/delete', b'get delete uname_gallery_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'tag', b'69')], [b'get', b'delete'], b'author')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/phrase', b'post uname_gallery_phrase/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', None)], [b'post'], b'authenticated')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/phrase/post', b'get post uname_gallery_phrase/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', None)], [b'get', b'post'], b'authenticated')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/phrase/post', b'post post uname_gallery_phrase/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', None)], [b'post', b'post'], b'authenticated')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23/phrase/68', b'put uname_gallery_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', b'68')], [b'put'], b'author')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/phrase/68/put', b'post put uname_gallery_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', b'68')], [b'post', b'put'], b'author')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/phrase/68/put', b'get put uname_gallery_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', b'68')], [b'get', b'put'], b'author')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/23/phrase/68', b'delete uname_gallery_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', b'68')], [b'delete'], b'author')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/phrase/68/delete', b'post delete uname_gallery_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', b'68')], [b'post', b'delete'], b'author')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/phrase/68/delete', b'get delete uname_gallery_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'phrase', b'68')], [b'get', b'delete'], b'author')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment', b'post uname_gallery_pic_comment/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', None)], [b'post'], b'authenticated')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment/post', b'get post uname_gallery_pic_comment/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', None)], [b'get', b'post'], b'authenticated')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment/post', b'post post uname_gallery_pic_comment/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', None)], [b'post', b'post'], b'authenticated')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment/159', b'put uname_gallery_pic_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', b'159')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment/159/put', b'post put uname_gallery_pic_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', b'159')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment/159/put', b'get put uname_gallery_pic_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', b'159')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment/159', b'delete uname_gallery_pic_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', b'159')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment/159/delete', b'post delete uname_gallery_pic_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', b'159')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/comment/159/delete', b'get delete uname_gallery_pic_comment_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'comment', b'159')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag', b'post uname_gallery_pic_tag/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', None)], [b'post'], b'authenticated')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag/post', b'get post uname_gallery_pic_tag/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', None)], [b'get', b'post'], b'authenticated')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag/post', b'post post uname_gallery_pic_tag/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', None)], [b'post', b'post'], b'authenticated')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag/169', b'put uname_gallery_pic_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', b'169')], [b'put'], b'author')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag/169/put', b'post put uname_gallery_pic_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', b'169')], [b'post', b'put'], b'author')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag/169/put', b'get put uname_gallery_pic_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', b'169')], [b'get', b'put'], b'author')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag/169', b'delete uname_gallery_pic_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', b'169')], [b'delete'], b'author')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag/169/delete', b'post delete uname_gallery_pic_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', b'169')], [b'post', b'delete'], b'author')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/tag/169/delete', b'get delete uname_gallery_pic_tag_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'tag', b'169')], [b'get', b'delete'], b'author')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/face', b'post uname_gallery_pic_face/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'face', None)], [b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/face/post', b'get post uname_gallery_pic_face/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'face', None)], [b'get', b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/face/post', b'post post uname_gallery_pic_face/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'face', None)], [b'post', b'post'], b'owner')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23/pic/152/face/169', b'put uname_gallery_pic_face_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'face', b'169')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/face/169/put', b'post put uname_gallery_pic_face_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'face', b'169')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/face/169/put', b'get put uname_gallery_pic_face_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'face', b'169')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/23/pic/152/face/169', b'delete uname_gallery_pic_face_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'face', b'169')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/face/169/delete', b'post delete uname_gallery_pic_face_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'face', b'169')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/face/169/delete', b'get delete uname_gallery_pic_face_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'face', b'169')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase', b'post uname_gallery_pic_phrase/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', None)], [b'post'], b'authenticated')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase/post', b'get post uname_gallery_pic_phrase/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', None)], [b'get', b'post'], b'authenticated')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase/post', b'post post uname_gallery_pic_phrase/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', None)], [b'post', b'post'], b'authenticated')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase/168', b'put uname_gallery_pic_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', b'168')], [b'put'], b'author')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase/168/put', b'post put uname_gallery_pic_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', b'168')], [b'post', b'put'], b'author')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase/168/put', b'get put uname_gallery_pic_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', b'168')], [b'get', b'put'], b'author')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase/168', b'delete uname_gallery_pic_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', b'168')], [b'delete'], b'author')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase/168/delete', b'post delete uname_gallery_pic_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', b'168')], [b'post', b'delete'], b'author')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/phrase/168/delete', b'get delete uname_gallery_pic_phrase_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'phrase', b'168')], [b'get', b'delete'], b'author')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/vote', b'post uname_gallery_pic_vote/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'vote', None)], [b'post'], b'authenticated')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/vote/post', b'get post uname_gallery_pic_vote/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'vote', None)], [b'get', b'post'], b'authenticated')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/vote/post', b'post post uname_gallery_pic_vote/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'vote', None)], [b'post', b'post'], b'authenticated')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23/pic/152/vote/159', b'put uname_gallery_pic_vote_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'vote', b'159')], [b'put'], b'author')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/vote/159/put', b'post put uname_gallery_pic_vote_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'vote', b'159')], [b'post', b'put'], b'author')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/vote/159/put', b'get put uname_gallery_pic_vote_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'vote', b'159')], [b'get', b'put'], b'author')),
(b'****************',),
(b'****************',),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/pmsent/58', b'delete uname_pmsent_', ([(b'uname', b'alex')], [(b'pmsent', b'58')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/pmsent/58/delete', b'post delete uname_pmsent_', ([(b'uname', b'alex')], [(b'pmsent', b'58')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/pmsent/58/delete', b'get delete uname_pmsent_', ([(b'uname', b'alex')], [(b'pmsent', b'58')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/pm', b'post uname_pm/', ([(b'uname', b'alex')], [(b'pm', None)], [b'post'], b'authenticated')),
(b'GET', b'http://alex.atpic.com', b'/pm/post', b'get post uname_pm/', ([(b'uname', b'alex')], [(b'pm', None)], [b'get', b'post'], b'authenticated')),
(b'POST', b'http://alex.atpic.com', b'/pm/post', b'post post uname_pm/', ([(b'uname', b'alex')], [(b'pm', None)], [b'post', b'post'], b'authenticated')),
(b'****************',),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/pm/59', b'delete uname_pm_', ([(b'uname', b'alex')], [(b'pm', b'59')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/pm/59/delete', b'post delete uname_pm_', ([(b'uname', b'alex')], [(b'pm', b'59')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/pm/59/delete', b'get delete uname_pm_', ([(b'uname', b'alex')], [(b'pm', b'59')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/friend', b'post uname_friend/', ([(b'uname', b'alex')], [(b'friend', None)], [b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/friend/post', b'get post uname_friend/', ([(b'uname', b'alex')], [(b'friend', None)], [b'get', b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/friend/post', b'post post uname_friend/', ([(b'uname', b'alex')], [(b'friend', None)], [b'post', b'post'], b'owner')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/friend/44', b'put uname_friend_', ([(b'uname', b'alex')], [(b'friend', b'44')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/friend/44/put', b'post put uname_friend_', ([(b'uname', b'alex')], [(b'friend', b'44')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/friend/44/put', b'get put uname_friend_', ([(b'uname', b'alex')], [(b'friend', b'44')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/friend/44', b'delete uname_friend_', ([(b'uname', b'alex')], [(b'friend', b'44')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/friend/44/delete', b'post delete uname_friend_', ([(b'uname', b'alex')], [(b'friend', b'44')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/friend/44/delete', b'get delete uname_friend_', ([(b'uname', b'alex')], [(b'friend', b'44')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/payment', b'post uname_payment/', ([(b'uname', b'alex')], [(b'payment', None)], [b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/payment/post', b'get post uname_payment/', ([(b'uname', b'alex')], [(b'payment', None)], [b'get', b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/payment/post', b'post post uname_payment/', ([(b'uname', b'alex')], [(b'payment', None)], [b'post', b'post'], b'owner')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/payment/57', b'put uname_payment_', ([(b'uname', b'alex')], [(b'payment', b'57')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/payment/57/put', b'post put uname_payment_', ([(b'uname', b'alex')], [(b'payment', b'57')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/payment/57/put', b'get put uname_payment_', ([(b'uname', b'alex')], [(b'payment', b'57')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/payment/57', b'delete uname_payment_', ([(b'uname', b'alex')], [(b'payment', b'57')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/payment/57/delete', b'post delete uname_payment_', ([(b'uname', b'alex')], [(b'payment', b'57')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/payment/57/delete', b'get delete uname_payment_', ([(b'uname', b'alex')], [(b'payment', b'57')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/buy', b'post uname_buy/', ([(b'uname', b'alex')], [(b'buy', None)], [b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/buy/post', b'get post uname_buy/', ([(b'uname', b'alex')], [(b'buy', None)], [b'get', b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/buy/post', b'post post uname_buy/', ([(b'uname', b'alex')], [(b'buy', None)], [b'post', b'post'], b'owner')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/buy/157', b'put uname_buy_', ([(b'uname', b'alex')], [(b'buy', b'157')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/buy/157/put', b'post put uname_buy_', ([(b'uname', b'alex')], [(b'buy', b'157')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/buy/157/put', b'get put uname_buy_', ([(b'uname', b'alex')], [(b'buy', b'157')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/buy/157', b'delete uname_buy_', ([(b'uname', b'alex')], [(b'buy', b'157')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/buy/157/delete', b'post delete uname_buy_', ([(b'uname', b'alex')], [(b'buy', b'157')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/buy/157/delete', b'get delete uname_buy_', ([(b'uname', b'alex')], [(b'buy', b'157')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/sell', b'post uname_sell/', ([(b'uname', b'alex')], [(b'sell', None)], [b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/sell/post', b'get post uname_sell/', ([(b'uname', b'alex')], [(b'sell', None)], [b'get', b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/sell/post', b'post post uname_sell/', ([(b'uname', b'alex')], [(b'sell', None)], [b'post', b'post'], b'owner')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/sell/157', b'put uname_sell_', ([(b'uname', b'alex')], [(b'sell', b'157')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/sell/157/put', b'post put uname_sell_', ([(b'uname', b'alex')], [(b'sell', b'157')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/sell/157/put', b'get put uname_sell_', ([(b'uname', b'alex')], [(b'sell', b'157')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/sell/157', b'delete uname_sell_', ([(b'uname', b'alex')], [(b'sell', b'157')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/sell/157/delete', b'post delete uname_sell_', ([(b'uname', b'alex')], [(b'sell', b'157')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/sell/157/delete', b'get delete uname_sell_', ([(b'uname', b'alex')], [(b'sell', b'157')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'****************',),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/du', b'post uname_du/', ([(b'uname', b'alex')], [(b'du', None)], [b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/preferences', b'post uname_preferences/', ([(b'uname', b'alex')], [(b'preferences', None)], [b'post'], b'owner')),
(b'*****presentation***********',),
(b'************tree (composite)************',),
(b'GET', b'http://alex.atpic.com', b'', b'get uname_', ([(b'uname', b'alex')], [], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/tree', b'get uname_tree_', ([(b'uname', b'alex')], [(b'tree', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/tree/france', b'get uname_tree_', ([(b'uname', b'alex')], [(b'tree', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/tree/france/paris', b'get uname_tree_', ([(b'uname', b'alex')], [(b'tree', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/tree/france/paris/eiffel_tower.html', b'get uname_tree_', ([(b'uname', b'alex')], [(b'tree', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),
(b'************Treesearch************',),
(b'GET', b'http://alex.atpic.com', b'', b'get uname_', ([(b'uname', b'alex')], [], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/treesearch', b'get uname_treesearch_', ([(b'uname', b'alex')], [(b'treesearch', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/treesearch/france', b'get uname_treesearch_', ([(b'uname', b'alex')], [(b'treesearch', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/treesearch/france/paris', b'get uname_treesearch_', ([(b'uname', b'alex')], [(b'treesearch', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/treesearch/france/paris/eiffel_tower.html', b'get uname_treesearch_', ([(b'uname', b'alex')], [(b'treesearch', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),
(b'************treenav************',),
(b'GET', b'http://alex.atpic.com', b'', b'get uname_', ([(b'uname', b'alex')], [], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/treenav', b'get uname_treenav_', ([(b'uname', b'alex')], [(b'treenav', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/treenav/france', b'get uname_treenav_', ([(b'uname', b'alex')], [(b'treenav', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/treenav/france/paris', b'get uname_treenav_', ([(b'uname', b'alex')], [(b'treenav', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/treenav/france/paris/eiffel_tower.html', b'get uname_treenav_', ([(b'uname', b'alex')], [(b'treenav', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),


(b'************vtree (composite)************',),
(b'GET', b'http://alex.atpic.com', b'', b'get uname_', ([(b'uname', b'alex')], [], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtree', b'get uname_vtree_', ([(b'uname', b'alex')], [(b'vtree', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtree/france', b'get uname_vtree_', ([(b'uname', b'alex')], [(b'vtree', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtree/france/paris', b'get uname_vtree_', ([(b'uname', b'alex')], [(b'vtree', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtree/france/paris/eiffel_tower.html', b'get uname_vtree_', ([(b'uname', b'alex')], [(b'vtree', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),
(b'************Vtreesearch************',),
(b'GET', b'http://alex.atpic.com', b'', b'get uname_', ([(b'uname', b'alex')], [], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtreesearch', b'get uname_vtreesearch_', ([(b'uname', b'alex')], [(b'vtreesearch', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtreesearch/france', b'get uname_vtreesearch_', ([(b'uname', b'alex')], [(b'vtreesearch', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtreesearch/france/paris', b'get uname_vtreesearch_', ([(b'uname', b'alex')], [(b'vtreesearch', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtreesearch/france/paris/eiffel_tower.html', b'get uname_vtreesearch_', ([(b'uname', b'alex')], [(b'vtreesearch', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),
(b'************vtreenav************',),
(b'GET', b'http://alex.atpic.com', b'', b'get uname_', ([(b'uname', b'alex')], [], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtreenav', b'get uname_vtreenav_', ([(b'uname', b'alex')], [(b'vtreenav', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtreenav/france', b'get uname_vtreenav_', ([(b'uname', b'alex')], [(b'vtreenav', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtreenav/france/paris', b'get uname_vtreenav_', ([(b'uname', b'alex')], [(b'vtreenav', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/vtreenav/france/paris/eiffel_tower.html', b'get uname_vtreenav_', ([(b'uname', b'alex')], [(b'vtreenav', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),


(b'***********blog************',),
(b'GET', b'http://alex.atpic.com', b'/blog', b'get uname_blog_', ([(b'uname', b'alex')], [(b'blog', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/blog/2010', b'get uname_blog_', ([(b'uname', b'alex')], [(b'blog', b'/2010')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/blog/2010/12', b'get uname_blog_', ([(b'uname', b'alex')], [(b'blog', b'/2010/12')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/blog/2010/12/31', b'get uname_blog_', ([(b'uname', b'alex')], [(b'blog', b'/2010/12/31')], [b'get'], b'anonymous')),
(b'***********blognav************',),
(b'GET', b'http://alex.atpic.com', b'/blognav', b'get uname_blognav_', ([(b'uname', b'alex')], [(b'blognav', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/blognav/2010', b'get uname_blognav_', ([(b'uname', b'alex')], [(b'blognav', b'/2010')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/blognav/2010/12', b'get uname_blognav_', ([(b'uname', b'alex')], [(b'blognav', b'/2010/12')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/blognav/2010/12/31', b'get uname_blognav_', ([(b'uname', b'alex')], [(b'blognav', b'/2010/12/31')], [b'get'], b'anonymous')),
(b'***********blogsearch************',),
(b'GET', b'http://alex.atpic.com', b'/blogsearch', b'get uname_blogsearch_', ([(b'uname', b'alex')], [(b'blogsearch', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/blogsearch/2010', b'get uname_blogsearch_', ([(b'uname', b'alex')], [(b'blogsearch', b'/2010')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/blogsearch/2010/12', b'get uname_blogsearch_', ([(b'uname', b'alex')], [(b'blogsearch', b'/2010/12')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/blogsearch/2010/12/31', b'get uname_blogsearch_', ([(b'uname', b'alex')], [(b'blogsearch', b'/2010/12/31')], [b'get'], b'anonymous')),
(b'***********geo************',),
(b'GET', b'http://alex.atpic.com', b'/geo', b'get uname_geo_', ([(b'uname', b'alex')], [(b'geo', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/geo/2010', b'get uname_geo_', ([(b'uname', b'alex')], [(b'geo', b'/2010')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/geo/2010/12', b'get uname_geo_', ([(b'uname', b'alex')], [(b'geo', b'/2010/12')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/geo/2010/12/31', b'get uname_geo_', ([(b'uname', b'alex')], [(b'geo', b'/2010/12/31')], [b'get'], b'anonymous')),

(b'***********geonav************',),
(b'GET', b'http://alex.atpic.com', b'/geonav', b'get uname_geonav_', ([(b'uname', b'alex')], [(b'geonav', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/geonav/2010', b'get uname_geonav_', ([(b'uname', b'alex')], [(b'geonav', b'/2010')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/geonav/2010/12', b'get uname_geonav_', ([(b'uname', b'alex')], [(b'geonav', b'/2010/12')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/geonav/2010/12/31', b'get uname_geonav_', ([(b'uname', b'alex')], [(b'geonav', b'/2010/12/31')], [b'get'], b'anonymous')),

(b'***********geosearch************',),
(b'GET', b'http://alex.atpic.com', b'/geosearch', b'get uname_geosearch_', ([(b'uname', b'alex')], [(b'geosearch', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/geosearch/2010', b'get uname_geosearch_', ([(b'uname', b'alex')], [(b'geosearch', b'/2010')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/geosearch/2010/12', b'get uname_geosearch_', ([(b'uname', b'alex')], [(b'geosearch', b'/2010/12')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/geosearch/2010/12/31', b'get uname_geosearch_', ([(b'uname', b'alex')], [(b'geosearch', b'/2010/12/31')], [b'get'], b'anonymous')),




(b'***********************',),
(b'GET', b'http://alex.atpic.com', b'/contact', b'get uname_contact/', ([(b'uname', b'alex')], [(b'contact', None)], [b'get'], b'anonymous')),
(b'********hbase********',),
(b'GET', b'http://alex.atpic.com', b'/audit', b'get uname_audit/', ([(b'uname', b'alex')], [(b'audit', None)], [b'get'], b'anonymous')),
(b'******* disk layer ***',),
(b'POST', b'http://alex.atpic.com', b'/gallery/53/delete', b'post delete uname_gallery_', ([(b'uname', b'alex')], [(b'gallery', b'53')], [b'post', b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/post', b'post post uname_gallery/', ([(b'uname', b'alex')], [(b'gallery', None)], [b'post', b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/53/pic/99/exif', b'get uname_gallery_pic_exif/', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99'), (b'exif', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/53/pic/99/sizeb', b'get uname_gallery_pic_sizeb/', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99'), (b'sizeb', None)], [b'get'], b'anonymous')),
(b'POST', b'http://alex.atpic.com', b'/gallery/53/pic/99/delete', b'post delete uname_gallery_pic_', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99')], [b'post', b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/53/pic/99/post', b'post post uname_gallery_pic_', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99')], [b'post', b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/53/pic/99/rotate', b'post uname_gallery_pic_rotate/', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99'), (b'rotate', None)], [b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/53/pic/99/face', b'get uname_gallery_pic_face/', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99'), (b'face', None)], [b'get'], b'anonymous')),
(b'POST', b'http://alex.atpic.com', b'/gallery/53/pic/99/put', b'post put uname_gallery_pic_', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99')], [b'post', b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/53/pic/99/chown', b'post uname_gallery_pic_chown/', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99'), (b'chown', None)], [b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/53/pic/99/thumbnail', b'post uname_gallery_pic_thumbnail/', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99'), (b'thumbnail', None)], [b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/ftp', b'post uname_ftp/', ([(b'uname', b'alex')], [(b'ftp', None)], [b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/quota', b'post uname_quota/', ([(b'uname', b'alex')], [(b'quota', None)], [b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/53/secret/put', b'post put uname_gallery_secret/', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'secret', None)], [b'post', b'put'], b'owner')),
(b'******* disk layer, done at creation *********',),
(b'**********************************',),
(b'**********************************',),
(b'*********non user based SQL*******',),
(b'**********************************',),
(b'**********************************',),
(b'GET', b'http://atpic.com', b'/translate', b'get atpiccom/translate/', ([(b'atpiccom', None)], [(b'translate', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/translate/1', b'get atpiccom/translate_', ([(b'atpiccom', None)], [(b'translate', b'1')], [b'get'], b'anonymous')),
(b'POST', b'http://atpic.com', b'/translate', b'post atpiccom/translate/', ([(b'atpiccom', None)], [(b'translate', None)], [b'post'], b'authenticated')),
(b'GET', b'http://atpic.com', b'/translate/post', b'get post atpiccom/translate/', ([(b'atpiccom', None)], [(b'translate', None)], [b'get', b'post'], b'authenticated')),
(b'POST', b'http://atpic.com', b'/translate/post', b'post post atpiccom/translate/', ([(b'atpiccom', None)], [(b'translate', None)], [b'post', b'post'], b'authenticated')),
(b'****************',),
(b'PUT', b'http://atpic.com', b'/translate/1', b'put atpiccom/translate_', ([(b'atpiccom', None)], [(b'translate', b'1')], [b'put'], b'admin')),
(b'POST', b'http://atpic.com', b'/translate/1/put', b'post put atpiccom/translate_', ([(b'atpiccom', None)], [(b'translate', b'1')], [b'post', b'put'], b'admin')),
(b'GET', b'http://atpic.com', b'/translate/1/put', b'get put atpiccom/translate_', ([(b'atpiccom', None)], [(b'translate', b'1')], [b'get', b'put'], b'admin')),
(b'****************',),
(b'DELETE', b'http://atpic.com', b'/translate/1', b'delete atpiccom/translate_', ([(b'atpiccom', None)], [(b'translate', b'1')], [b'delete'], b'admin')),
(b'POST', b'http://atpic.com', b'/translate/1/delete', b'post delete atpiccom/translate_', ([(b'atpiccom', None)], [(b'translate', b'1')], [b'post', b'delete'], b'admin')),
(b'GET', b'http://atpic.com', b'/translate/1/delete', b'get delete atpiccom/translate_', ([(b'atpiccom', None)], [(b'translate', b'1')], [b'get', b'delete'], b'admin')),
(b'****************',),
(b'****************',),
(b'GET', b'http://atpic.com', b'/news', b'get atpiccom/news/', ([(b'atpiccom', None)], [(b'news', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/news/1', b'get atpiccom/news_', ([(b'atpiccom', None)], [(b'news', b'1')], [b'get'], b'anonymous')),
(b'POST', b'http://atpic.com', b'/news', b'post atpiccom/news/', ([(b'atpiccom', None)], [(b'news', None)], [b'post'], b'admin')),
(b'GET', b'http://atpic.com', b'/news/post', b'get post atpiccom/news/', ([(b'atpiccom', None)], [(b'news', None)], [b'get', b'post'], b'admin')),
(b'POST', b'http://atpic.com', b'/news/post', b'post post atpiccom/news/', ([(b'atpiccom', None)], [(b'news', None)], [b'post', b'post'], b'admin')),
(b'****************',),
(b'PUT', b'http://atpic.com', b'/news/1', b'put atpiccom/news_', ([(b'atpiccom', None)], [(b'news', b'1')], [b'put'], b'admin')),
(b'POST', b'http://atpic.com', b'/news/1/put', b'post put atpiccom/news_', ([(b'atpiccom', None)], [(b'news', b'1')], [b'post', b'put'], b'admin')),
(b'GET', b'http://atpic.com', b'/news/1/put', b'get put atpiccom/news_', ([(b'atpiccom', None)], [(b'news', b'1')], [b'get', b'put'], b'admin')),
(b'****************',),
(b'DELETE', b'http://atpic.com', b'/news/1', b'delete atpiccom/news_', ([(b'atpiccom', None)], [(b'news', b'1')], [b'delete'], b'admin')),
(b'POST', b'http://atpic.com', b'/news/1/delete', b'post delete atpiccom/news_', ([(b'atpiccom', None)], [(b'news', b'1')], [b'post', b'delete'], b'admin')),
(b'GET', b'http://atpic.com', b'/news/1/delete', b'get delete atpiccom/news_', ([(b'atpiccom', None)], [(b'news', b'1')], [b'get', b'delete'], b'admin')),
(b'****************',),
(b'****************',),
(b'****************',),
(b'GET', b'http://atpic.com', b'/chapter', b'get atpiccom/chapter/', ([(b'atpiccom', None)], [(b'chapter', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/chapter/1', b'get atpiccom/chapter_', ([(b'atpiccom', None)], [(b'chapter', b'1')], [b'get'], b'anonymous')),
(b'POST', b'http://atpic.com', b'/chapter', b'post atpiccom/chapter/', ([(b'atpiccom', None)], [(b'chapter', None)], [b'post'], b'admin')),
(b'GET', b'http://atpic.com', b'/chapter/post', b'get post atpiccom/chapter/', ([(b'atpiccom', None)], [(b'chapter', None)], [b'get', b'post'], b'admin')),
(b'POST', b'http://atpic.com', b'/chapter/post', b'post post atpiccom/chapter/', ([(b'atpiccom', None)], [(b'chapter', None)], [b'post', b'post'], b'admin')),
(b'****************',),
(b'PUT', b'http://atpic.com', b'/chapter/1', b'put atpiccom/chapter_', ([(b'atpiccom', None)], [(b'chapter', b'1')], [b'put'], b'admin')),
(b'POST', b'http://atpic.com', b'/chapter/1/put', b'post put atpiccom/chapter_', ([(b'atpiccom', None)], [(b'chapter', b'1')], [b'post', b'put'], b'admin')),
(b'GET', b'http://atpic.com', b'/chapter/1/put', b'get put atpiccom/chapter_', ([(b'atpiccom', None)], [(b'chapter', b'1')], [b'get', b'put'], b'admin')),
(b'****************',),
(b'DELETE', b'http://atpic.com', b'/chapter/1', b'delete atpiccom/chapter_', ([(b'atpiccom', None)], [(b'chapter', b'1')], [b'delete'], b'admin')),
(b'POST', b'http://atpic.com', b'/chapter/1/delete', b'post delete atpiccom/chapter_', ([(b'atpiccom', None)], [(b'chapter', b'1')], [b'post', b'delete'], b'admin')),
(b'GET', b'http://atpic.com', b'/chapter/1/delete', b'get delete atpiccom/chapter_', ([(b'atpiccom', None)], [(b'chapter', b'1')], [b'get', b'delete'], b'admin')),
(b'****************',),
(b'****************',),
(b'GET', b'http://atpic.com', b'/chapter/1/section', b'get atpiccom/chapter_section/', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/chapter/1/section/99', b'get atpiccom/chapter_section_', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', b'99')], [b'get'], b'anonymous')),
(b'POST', b'http://atpic.com', b'/chapter/1/section', b'post atpiccom/chapter_section/', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', None)], [b'post'], b'admin')),
(b'GET', b'http://atpic.com', b'/chapter/1/section/post', b'get post atpiccom/chapter_section/', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', None)], [b'get', b'post'], b'admin')),
(b'POST', b'http://atpic.com', b'/chapter/1/section/post', b'post post atpiccom/chapter_section/', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', None)], [b'post', b'post'], b'admin')),
(b'****************',),
(b'PUT', b'http://atpic.com', b'/chapter/1/section/99', b'put atpiccom/chapter_section_', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', b'99')], [b'put'], b'admin')),
(b'POST', b'http://atpic.com', b'/chapter/1/section/99/put', b'post put atpiccom/chapter_section_', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', b'99')], [b'post', b'put'], b'admin')),
(b'GET', b'http://atpic.com', b'/chapter/1/section/99/put', b'get put atpiccom/chapter_section_', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', b'99')], [b'get', b'put'], b'admin')),
(b'****************',),
(b'DELETE', b'http://atpic.com', b'/chapter/1/section/99', b'delete atpiccom/chapter_section_', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', b'99')], [b'delete'], b'admin')),
(b'POST', b'http://atpic.com', b'/chapter/1/section/99/delete', b'post delete atpiccom/chapter_section_', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', b'99')], [b'post', b'delete'], b'admin')),
(b'GET', b'http://atpic.com', b'/chapter/1/section/99/delete', b'get delete atpiccom/chapter_section_', ([(b'atpiccom', None)], [(b'chapter', b'1'), (b'section', b'99')], [b'get', b'delete'], b'admin')),
(b'****************',),
(b'****************',),
(b'GET', b'http://atpic.com', b'/entry', b'get atpiccom/entry/', ([(b'atpiccom', None)], [(b'entry', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/entry/1', b'get atpiccom/entry_', ([(b'atpiccom', None)], [(b'entry', b'1')], [b'get'], b'anonymous')),
(b'POST', b'http://atpic.com', b'/entry', b'post atpiccom/entry/', ([(b'atpiccom', None)], [(b'entry', None)], [b'post'], b'admin')),
(b'GET', b'http://atpic.com', b'/entry/post', b'get post atpiccom/entry/', ([(b'atpiccom', None)], [(b'entry', None)], [b'get', b'post'], b'admin')),
(b'POST', b'http://atpic.com', b'/entry/post', b'post post atpiccom/entry/', ([(b'atpiccom', None)], [(b'entry', None)], [b'post', b'post'], b'admin')),
(b'****************',),
(b'PUT', b'http://atpic.com', b'/entry/1', b'put atpiccom/entry_', ([(b'atpiccom', None)], [(b'entry', b'1')], [b'put'], b'admin')),
(b'POST', b'http://atpic.com', b'/entry/1/put', b'post put atpiccom/entry_', ([(b'atpiccom', None)], [(b'entry', b'1')], [b'post', b'put'], b'admin')),
(b'GET', b'http://atpic.com', b'/entry/1/put', b'get put atpiccom/entry_', ([(b'atpiccom', None)], [(b'entry', b'1')], [b'get', b'put'], b'admin')),
(b'****************',),
(b'DELETE', b'http://atpic.com', b'/entry/1', b'delete atpiccom/entry_', ([(b'atpiccom', None)], [(b'entry', b'1')], [b'delete'], b'admin')),
(b'POST', b'http://atpic.com', b'/entry/1/delete', b'post delete atpiccom/entry_', ([(b'atpiccom', None)], [(b'entry', b'1')], [b'post', b'delete'], b'admin')),
(b'GET', b'http://atpic.com', b'/entry/1/delete', b'get delete atpiccom/entry_', ([(b'atpiccom', None)], [(b'entry', b'1')], [b'get', b'delete'], b'admin')),
(b'****************',),
(b'****************',),
(b'GET', b'http://atpic.com', b'/entry/1/line', b'get atpiccom/entry_line/', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/entry/1/line/99', b'get atpiccom/entry_line_', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', b'99')], [b'get'], b'anonymous')),
(b'POST', b'http://atpic.com', b'/entry/1/line', b'post atpiccom/entry_line/', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', None)], [b'post'], b'admin')),
(b'GET', b'http://atpic.com', b'/entry/1/line/post', b'get post atpiccom/entry_line/', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', None)], [b'get', b'post'], b'admin')),
(b'POST', b'http://atpic.com', b'/entry/1/line/post', b'post post atpiccom/entry_line/', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', None)], [b'post', b'post'], b'admin')),
(b'****************',),
(b'PUT', b'http://atpic.com', b'/entry/1/line/99', b'put atpiccom/entry_line_', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', b'99')], [b'put'], b'admin')),
(b'POST', b'http://atpic.com', b'/entry/1/line/99/put', b'post put atpiccom/entry_line_', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', b'99')], [b'post', b'put'], b'admin')),
(b'GET', b'http://atpic.com', b'/entry/1/line/99/put', b'get put atpiccom/entry_line_', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', b'99')], [b'get', b'put'], b'admin')),
(b'****************',),
(b'DELETE', b'http://atpic.com', b'/entry/1/line/99', b'delete atpiccom/entry_line_', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', b'99')], [b'delete'], b'admin')),
(b'POST', b'http://atpic.com', b'/entry/1/line/99/delete', b'post delete atpiccom/entry_line_', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', b'99')], [b'post', b'delete'], b'admin')),
(b'GET', b'http://atpic.com', b'/entry/1/line/99/delete', b'get delete atpiccom/entry_line_', ([(b'atpiccom', None)], [(b'entry', b'1'), (b'line', b'99')], [b'get', b'delete'], b'admin')),
(b'****************',),
(b'****************',),
(b'GET', b'http://atpic.com', b'/faq', b'get atpiccom/faq_', ([(b'atpiccom', None)], [(b'faq', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/faq/howto', b'get atpiccom/faq_', ([(b'atpiccom', None)], [(b'faq', b'/howto')], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/faq/howto/', b'get atpiccom/faq_', ([(b'atpiccom', None)], [(b'faq', b'/howto')], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/faq/howto/video', b'get atpiccom/faq_', ([(b'atpiccom', None)], [(b'faq', b'/howto/video')], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/faq/howto/video/', b'get atpiccom/faq_', ([(b'atpiccom', None)], [(b'faq', b'/howto/video')], [b'get'], b'anonymous')),
(b'***********************',),
(b'***********************',),
(b'****************',),
(b'GET', b'http://atpic.com', b'/product', b'get atpiccom/product/', ([(b'atpiccom', None)], [(b'product', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/product/1', b'get atpiccom/product_', ([(b'atpiccom', None)], [(b'product', b'1')], [b'get'], b'anonymous')),
(b'POST', b'http://atpic.com', b'/product', b'post atpiccom/product/', ([(b'atpiccom', None)], [(b'product', None)], [b'post'], b'admin')),
(b'GET', b'http://atpic.com', b'/product/post', b'get post atpiccom/product/', ([(b'atpiccom', None)], [(b'product', None)], [b'get', b'post'], b'admin')),
(b'POST', b'http://atpic.com', b'/product/post', b'post post atpiccom/product/', ([(b'atpiccom', None)], [(b'product', None)], [b'post', b'post'], b'admin')),
(b'****************',),
(b'PUT', b'http://atpic.com', b'/product/1', b'put atpiccom/product_', ([(b'atpiccom', None)], [(b'product', b'1')], [b'put'], b'admin')),
(b'POST', b'http://atpic.com', b'/product/1/put', b'post put atpiccom/product_', ([(b'atpiccom', None)], [(b'product', b'1')], [b'post', b'put'], b'admin')),
(b'GET', b'http://atpic.com', b'/product/1/put', b'get put atpiccom/product_', ([(b'atpiccom', None)], [(b'product', b'1')], [b'get', b'put'], b'admin')),
(b'****************',),
(b'DELETE', b'http://atpic.com', b'/product/1', b'delete atpiccom/product_', ([(b'atpiccom', None)], [(b'product', b'1')], [b'delete'], b'admin')),
(b'POST', b'http://atpic.com', b'/product/1/delete', b'post delete atpiccom/product_', ([(b'atpiccom', None)], [(b'product', b'1')], [b'post', b'delete'], b'admin')),
(b'GET', b'http://atpic.com', b'/product/1/delete', b'get delete atpiccom/product_', ([(b'atpiccom', None)], [(b'product', b'1')], [b'get', b'delete'], b'admin')),
(b'***********************',),
(b'***********************',),
(b'*******search*********',),
(b'***********************',),
(b'****q= (search), s=random, count, stats, calendar, +driver=flash, maps, google******',),
(b'GET', b'http://atpic.com', b'/search', b'get atpiccom/search/', ([(b'atpiccom', None)], [(b'search', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/search/gallery', b'get atpiccom/search_', ([(b'atpiccom', None)], [(b'search', b'gallery')], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/search/user', b'get atpiccom/search_', ([(b'atpiccom', None)], [(b'search', b'user')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/search', b'get uname_search/', ([(b'uname', b'alex')], [(b'search', None)], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/search', b'get selldns_search/', ([(b'selldns', b'adns.com')], [(b'search', None)], [b'get'], b'anonymous')),
(b'******************************',),
(b'*******presentation but with sell dns*********',),
(b'GET', b'http://adns.com', b'', b'get selldns_', ([(b'selldns', b'adns.com')], [], [b'get'], b'anonymous')),

(b'********this is filesystem tree stored********',),
(b'GET', b'http://adns.com', b'/tree', b'get selldns_tree_', ([(b'selldns', b'adns.com')], [(b'tree', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/tree/france', b'get selldns_tree_', ([(b'selldns', b'adns.com')], [(b'tree', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/tree/france/paris', b'get selldns_tree_', ([(b'selldns', b'adns.com')], [(b'tree', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/tree/france/paris/eiffel_tower.html', b'get selldns_tree_', ([(b'selldns', b'adns.com')], [(b'tree', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),

(b'********this is filesystem treenav stored********',),
(b'GET', b'http://adns.com', b'/treenav', b'get selldns_treenav_', ([(b'selldns', b'adns.com')], [(b'treenav', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/treenav/france', b'get selldns_treenav_', ([(b'selldns', b'adns.com')], [(b'treenav', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/treenav/france/paris', b'get selldns_treenav_', ([(b'selldns', b'adns.com')], [(b'treenav', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/treenav/france/paris/eiffel_tower.html', b'get selldns_treenav_', ([(b'selldns', b'adns.com')], [(b'treenav', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),



(b'********this is filesystem treesearch stored********',),
(b'GET', b'http://adns.com', b'/treesearch', b'get selldns_treesearch_', ([(b'selldns', b'adns.com')], [(b'treesearch', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/treesearch/france', b'get selldns_treesearch_', ([(b'selldns', b'adns.com')], [(b'treesearch', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/treesearch/france/paris', b'get selldns_treesearch_', ([(b'selldns', b'adns.com')], [(b'treesearch', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/treesearch/france/paris/eiffel_tower.html', b'get selldns_treesearch_', ([(b'selldns', b'adns.com')], [(b'treesearch', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),










(b'********this is filesystem vtree stored********',),
(b'GET', b'http://adns.com', b'/vtree', b'get selldns_vtree_', ([(b'selldns', b'adns.com')], [(b'vtree', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/vtree/france', b'get selldns_vtree_', ([(b'selldns', b'adns.com')], [(b'vtree', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/vtree/france/paris', b'get selldns_vtree_', ([(b'selldns', b'adns.com')], [(b'vtree', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/vtree/france/paris/eiffel_tower.html', b'get selldns_vtree_', ([(b'selldns', b'adns.com')], [(b'vtree', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),

(b'********this is filesystem vtreenav stored********',),
(b'GET', b'http://adns.com', b'/vtreenav', b'get selldns_vtreenav_', ([(b'selldns', b'adns.com')], [(b'vtreenav', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/vtreenav/france', b'get selldns_vtreenav_', ([(b'selldns', b'adns.com')], [(b'vtreenav', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/vtreenav/france/paris', b'get selldns_vtreenav_', ([(b'selldns', b'adns.com')], [(b'vtreenav', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/vtreenav/france/paris/eiffel_tower.html', b'get selldns_vtreenav_', ([(b'selldns', b'adns.com')], [(b'vtreenav', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),



(b'********this is filesystem vtreesearch stored********',),
(b'GET', b'http://adns.com', b'/vtreesearch', b'get selldns_vtreesearch_', ([(b'selldns', b'adns.com')], [(b'vtreesearch', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/vtreesearch/france', b'get selldns_vtreesearch_', ([(b'selldns', b'adns.com')], [(b'vtreesearch', b'/france')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/vtreesearch/france/paris', b'get selldns_vtreesearch_', ([(b'selldns', b'adns.com')], [(b'vtreesearch', b'/france/paris')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/vtreesearch/france/paris/eiffel_tower.html', b'get selldns_vtreesearch_', ([(b'selldns', b'adns.com')], [(b'vtreesearch', b'/france/paris/eiffel_tower.html')], [b'get'], b'anonymous')),










(b'********this is hbase/sql tree stored********',),
(b'GET', b'http://adns.com', b'/blog', b'get selldns_blog_', ([(b'selldns', b'adns.com')], [(b'blog', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/blog/2010', b'get selldns_blog_', ([(b'selldns', b'adns.com')], [(b'blog', b'/2010')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/blog/2010/12', b'get selldns_blog_', ([(b'selldns', b'adns.com')], [(b'blog', b'/2010/12')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/blog/2010/12/31', b'get selldns_blog_', ([(b'selldns', b'adns.com')], [(b'blog', b'/2010/12/31')], [b'get'], b'anonymous')),
(b'********this is hbase/sql tree stored********',),
(b'GET', b'http://adns.com', b'/blognav', b'get selldns_blognav_', ([(b'selldns', b'adns.com')], [(b'blognav', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/blognav/2010', b'get selldns_blognav_', ([(b'selldns', b'adns.com')], [(b'blognav', b'/2010')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/blognav/2010/12', b'get selldns_blognav_', ([(b'selldns', b'adns.com')], [(b'blognav', b'/2010/12')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/blognav/2010/12/31', b'get selldns_blognav_', ([(b'selldns', b'adns.com')], [(b'blognav', b'/2010/12/31')], [b'get'], b'anonymous')),
(b'********this is hbase/sql tree stored********',),
(b'GET', b'http://adns.com', b'/blogsearch', b'get selldns_blogsearch_', ([(b'selldns', b'adns.com')], [(b'blogsearch', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/blogsearch/2010', b'get selldns_blogsearch_', ([(b'selldns', b'adns.com')], [(b'blogsearch', b'/2010')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/blogsearch/2010/12', b'get selldns_blogsearch_', ([(b'selldns', b'adns.com')], [(b'blogsearch', b'/2010/12')], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/blogsearch/2010/12/31', b'get selldns_blogsearch_', ([(b'selldns', b'adns.com')], [(b'blogsearch', b'/2010/12/31')], [b'get'], b'anonymous')),

(b'****************',),
(b'****************',),
(b'GET', b'http://adns.com', b'/contact', b'get selldns_contact/', ([(b'selldns', b'adns.com')], [(b'contact', None)], [b'get'], b'anonymous')),
(b'********hbase********',),
(b'GET', b'http://adns.com', b'/audit', b'get selldns_audit/', ([(b'selldns', b'adns.com')], [(b'audit', None)], [b'get'], b'anonymous')),
(b'*******login special auth*********',),
(b'GET', b'http://atpic.com', b'/login', b'get post atpiccom/login/', ([(b'atpiccom', None)], [(b'login', None)], [b'get', b'post'], b'anonymous')),
(b'POST', b'http://atpic.com', b'/login', b'post atpiccom/login/', ([(b'atpiccom', None)], [(b'login', None)], [b'post'], b'anonymous')),
(b'*******admin*********',),
(b'GET', b'http://atpic.com', b'/du', b'get atpiccom/du/', ([(b'atpiccom', None)], [(b'du', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/admin', b'get atpiccom/admin/', ([(b'atpiccom', None)], [(b'admin', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/audit', b'get atpiccom/audit/', ([(b'atpiccom', None)], [(b'audit', None)], [b'get'], b'anonymous')),
(b'*******legacy*********',),
(b'GET', b'http://atpic.com', b'/fr', b'get atpiccom/', ([(b'atpiccom', None)], [], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/fr/1', b'get atpiccom/', ([(b'atpiccom', None)], [], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/1', b'get atpiccom/', ([(b'atpiccom', None)], [], [b'get'], b'anonymous')),
(b'GET', b'http://pic.atpic.com', b'/1569', b'get legacyobject_id_', ([(b'legacyobject', b'pic')], [(b'id', b'1569')], [b'get'], b'anonymous')),
(b'GET', b'http://pic.atpic.com', b'/fr/1569', b'get legacyobject_id_', ([(b'legacyobject', b'pic')], [(b'id', b'1569')], [b'get'], b'anonymous')),
(b'GET', b'http://pic.atpic.com', b'/1569/600', b'get legacyobject_id_', ([(b'legacyobject', b'pic')], [(b'id', b'1569')], [b'get'], b'anonymous')),
(b'GET', b'http://pic.atpic.com', b'/1569/600/fgnydmqidqunurhrylxn', b'get legacyobject_id_secret_', ([(b'legacyobject', b'pic')], [(b'id', b'1569'), (b'secret', b'fgnydmqidqunurhrylxn')], [b'get'], b'anonymous')),
(b'GET', b'http://pic.atpic.com', b'/1569/fgnydmqidqunurhrylxn', b'get legacyobject_id_secret_', ([(b'legacyobject', b'pic')], [(b'id', b'1569'), (b'secret', b'fgnydmqidqunurhrylxn')], [b'get'], b'anonymous')),
(b'GET', b'http://pic.atpic.com', b'/fr/1569/600/fgnydmqidqunurhrylxn', b'get legacyobject_id_secret_', ([(b'legacyobject', b'pic')], [(b'id', b'1569'), (b'secret', b'fgnydmqidqunurhrylxn')], [b'get'], b'anonymous')),
(b'GET', b'http://pic.atpic.com', b'/fr/1569/fgnydmqidqunurhrylxn', b'get legacyobject_id_secret_', ([(b'legacyobject', b'pic')], [(b'id', b'1569'), (b'secret', b'fgnydmqidqunurhrylxn')], [b'get'], b'anonymous')),
(b'GET', b'http://gallery.atpic.com', b'/19', b'get legacyobject_id_', ([(b'legacyobject', b'gallery')], [(b'id', b'19')], [b'get'], b'anonymous')),
(b'GET', b'http://gallery.atpic.com', b'/fr/19', b'get legacyobject_id_', ([(b'legacyobject', b'gallery')], [(b'id', b'19')], [b'get'], b'anonymous')),
(b'GET', b'http://gallery.atpic.com', b'/fr/19/fgnkdmqidqunurhrylxa', b'get legacyobject_id_secret_', ([(b'legacyobject', b'gallery')], [(b'id', b'19'), (b'secret', b'fgnkdmqidqunurhrylxa')], [b'get'], b'anonymous')),
(b'GET', b'http://pm.atpic.com', b'', b'get legacyobject_', ([(b'legacyobject', b'pm')], [], [b'get'], b'anonymous')),
(b'GET', b'http://du.atpic.com', b'', b'get legacyobject_', ([(b'legacyobject', b'du')], [], [b'get'], b'anonymous')),
(b'GET', b'http://wiki.atpic.com', b'', b'get legacyobject_', ([(b'legacyobject', b'wiki')], [], [b'get'], b'anonymous')),
(b'GET', b'http://faq.atpic.com', b'', b'get legacyobject_', ([(b'legacyobject', b'faq')], [], [b'get'], b'anonymous')),
(b'*******short cuts, implies a SQL search + a redirect*********',),
(b'*******money*********',),
(b'*******cart*********',),
(b'GET', b'http://alex.atpic.com', b'/cart', b'get uname_cart/', ([(b'uname', b'alex')], [(b'cart', None)], [b'get'], b'owner')),
(b'*******move a gallery into another (filter to avoid cyclic) *********',),
(b'GET', b'http://alex.atpic.com', b'/gallery/53/gallery', b'get uname_gallery_gallery/', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'gallery', None)], [b'get'], b'anonymous')),
(b'PUT', b'http://alex.atpic.com', b'/gallery/53/gallery/54', b'put uname_gallery_gallery_', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'gallery', b'54')], [b'put'], b'owner')),
(b'*******move a pic into another gallery*********',),
(b'GET', b'http://alex.atpic.com', b'/gallery/53/pic/99/gallery', b'get uname_gallery_pic_gallery/', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99'), (b'gallery', None)], [b'get'], b'anonymous')),
(b'PUT', b'http://alex.atpic.com', b'/gallery/53/pic/99/gallery/54', b'put uname_gallery_pic_gallery_', ([(b'uname', b'alex')], [(b'gallery', b'53'), (b'pic', b'99'), (b'gallery', b'54')], [b'put'], b'owner')),
(b'******* the gallery root/children like an atomsvc service *********',),
(b'GET', b'http://alex.atpic.com', b'/g', b'get uname_g/', ([(b'uname', b'alex')], [(b'g', None)], [b'get'], b'anonymous')),
(b'******* the gallery children *********',),
(b'GET', b'http://alex.atpic.com', b'/gallery/1/g', b'get uname_gallery_g/', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'g', None)], [b'get'], b'anonymous')),
(b'******* the gallery path, returns the text path and the parents gallery IDs *********',),
(b'GET', b'http://alex.atpic.com', b'/gallery/1/path', b'get uname_gallery_path/', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'path', None)], [b'get'], b'anonymous')),
(b'******* path/path (composite) calls pathnav/path below/path *********',),
(b'******* below/path is equivalent to: /gallery/1/below and /gallery/1/pathnav *********',),
(b'GET', b'http://alex.atpic.com', b'/gallery/1/below', b'get uname_gallery_below/', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'below', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/1/treenav', b'get uname_gallery_treenav/', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'treenav', None)], [b'get'], b'anonymous')),
(b'********captcha - returns an image ********',),
(b'GET', b'http://atpic.com', b'/captcha/dddd', b'get atpiccom/captcha_', ([(b'atpiccom', None)], [(b'captcha', b'dddd')], [b'get'], b'anonymous')),
(b'******** pic virtual path ********',),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/path', b'get uname_gallery_pic_path/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/path/159', b'get uname_gallery_pic_path_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', b'159')], [b'get'], b'anonymous')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/path', b'post uname_gallery_pic_path/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', None)], [b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/path/post', b'get post uname_gallery_pic_path/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', None)], [b'get', b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/path/post', b'post post uname_gallery_pic_path/', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', None)], [b'post', b'post'], b'owner')),
(b'PUT', b'http://alex.atpic.com', b'/gallery/23/pic/152/path/159', b'put uname_gallery_pic_path_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', b'159')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/path/159/put', b'post put uname_gallery_pic_path_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', b'159')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/path/159/put', b'get put uname_gallery_pic_path_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', b'159')], [b'get', b'put'], b'owner')),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/23/pic/152/path/159', b'delete uname_gallery_pic_path_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', b'159')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/23/pic/152/path/159/delete', b'post delete uname_gallery_pic_path_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', b'159')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/23/pic/152/path/159/delete', b'get delete uname_gallery_pic_path_', ([(b'uname', b'alex')], [(b'gallery', b'23'), (b'pic', b'152'), (b'path', b'159')], [b'get', b'delete'], b'owner')),
(b'**********gallery friend******',),
(b'GET', b'http://alex.atpic.com', b'/gallery/1/friend', b'get uname_gallery_friend/', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/gallery/1/friend/44', b'get uname_gallery_friend_', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', b'44')], [b'get'], b'anonymous')),
(b'****************',),
(b'POST', b'http://alex.atpic.com', b'/gallery/1/friend', b'post uname_gallery_friend/', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', None)], [b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/1/friend/post', b'get post uname_gallery_friend/', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', None)], [b'get', b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/1/friend/post', b'post post uname_gallery_friend/', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', None)], [b'post', b'post'], b'owner')),
(b'****************',),
(b'PUT', b'http://alex.atpic.com', b'/gallery/1/friend/44', b'put uname_gallery_friend_', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', b'44')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/1/friend/44/put', b'post put uname_gallery_friend_', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', b'44')], [b'post', b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/1/friend/44/put', b'get put uname_gallery_friend_', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', b'44')], [b'get', b'put'], b'owner')),
(b'****************',),
(b'DELETE', b'http://alex.atpic.com', b'/gallery/1/friend/44', b'delete uname_gallery_friend_', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', b'44')], [b'delete'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/gallery/1/friend/44/delete', b'post delete uname_gallery_friend_', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', b'44')], [b'post', b'delete'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/gallery/1/friend/44/delete', b'get delete uname_gallery_friend_', ([(b'uname', b'alex')], [(b'gallery', b'1'), (b'friend', b'44')], [b'get', b'delete'], b'owner')),
(b'****************',),
(b'**********sso******',),
(b'****************',),
(b'GET', b'http://atpic.com', b'/redirect', b'get atpiccom/redirect/', ([(b'atpiccom', None)], [(b'redirect', None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/logout', b'get atpiccom/logout/', ([(b'atpiccom', None)], [(b'logout', None)], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/logout', b'get selldns_logout/', ([(b'selldns', b'adns.com')], [(b'logout', None)], [b'get'], b'anonymous')),
(b'GET', b'http://adns.com', b'/1x1.gif', b'get selldns_1x1.gif/', ([(b'selldns', b'adns.com')], [(b'1x1.gif', None)], [b'get'], b'anonymous')),
(b'*******special pdns*********',),
(b'GET', b'http://pdns.com', b'/favicon.ico', b'get selldns_favicon.ico/', ([(b'selldns', b'pdns.com')], [(b'favicon.ico', None)], [b'get'], b'anonymous')),
(b'GET', b'http://pdns.com', b'/robots.txt', b'get selldns_robots.txt/', ([(b'selldns', b'pdns.com')], [(b'robots.txt', None)], [b'get'], b'anonymous')),
(b'GET', b'http://pdns.com', b'/sitemap.xml', b'get selldns_sitemap.xml/', ([(b'selldns', b'pdns.com')], [(b'sitemap.xml', None)], [b'get'], b'anonymous')),


(b'*******special pdns*********',),


(b'GET', b'http://alex.atpic.com', b'/journal', b'get uname_journal_', ([(b'uname', b'alex')], [(b'journal', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/journal/gallery', b'get uname_journal_', ([(b'uname', b'alex')], [(b'journal', b'/gallery')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/journal/gallery/1', b'get uname_journal_', ([(b'uname', b'alex')], [(b'journal', b'/gallery/1')], [b'get'], b'anonymous')),


(b'GET', b'http://atpic.com', b'/journal', b'get atpiccom/journal_', ([(b'atpiccom', None)], [(b'journal', b'/')], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/journal/gallery', b'get atpiccom/journal_', ([(b'atpiccom', None)], [(b'journal', b'/gallery')], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/journal/gallery/1', b'get atpiccom/journal_', ([(b'atpiccom', None)], [(b'journal', b'/gallery/1')], [b'get'], b'anonymous')),


(b'*********************',),
(b'**********wiki*******',),
(b'*********************',),
(b'GET', b'http://atpic.com', b'/wiki', b'get atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'')], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/API', b'get atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API')], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/API/pictures', b'get atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API/pictures')], [b'get'], b'anonymous')),


(b'PUT', b'http://atpic.com', b'/wiki/API', b'put atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API')], [b'put'], b'admin')),
(b'POST', b'http://atpic.com', b'/wiki/API', b'post atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API')], [b'post'], b'admin')),
(b'DELETE', b'http://atpic.com', b'/wiki/API', b'delete atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API')], [b'delete'], b'admin')),



(b'GET', b'http://atpic.com', b'/wiki/API/_put', b'get put atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API')], [b'get',b'put'], b'admin')),
(b'GET', b'http://atpic.com', b'/wiki/API/_post', b'get post atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API')], [b'get',b'post'], b'admin')),
(b'GET', b'http://atpic.com', b'/wiki/API/_delete', b'get delete atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API')], [b'get',b'delete'], b'admin')),



(b'POST', b'http://atpic.com', b'/wiki/API/_put', b'post put atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API')], [b'post',b'put'], b'admin')),
(b'POST', b'http://atpic.com', b'/wiki/API/_post', b'post post atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API')], [b'post',b'post'], b'admin')),
(b'POST', b'http://atpic.com', b'/wiki/API/_delete', b'post delete atpiccom/wiki_', ([(b'atpiccom', None)], [(b'wiki', b'/API')], [b'post',b'delete'], b'admin')),












(b'GET', b'http://alex.atpic.com', b'/wiki', b'get uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/wiki/europe', b'get uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'/europe')], [b'get'], b'anonymous')),

(b'PUT', b'http://alex.atpic.com', b'/wiki/europe', b'put uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'/europe')], [b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/wiki/europe', b'post uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'/europe')], [b'post'], b'owner')),
(b'DELETE', b'http://alex.atpic.com', b'/wiki/europe', b'delete uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'/europe')], [b'delete'], b'owner')),



(b'GET', b'http://alex.atpic.com', b'/wiki/europe/_put', b'get put uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'/europe')], [b'get',b'put'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/wiki/europe/_post', b'get post uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'/europe')], [b'get',b'post'], b'owner')),
(b'GET', b'http://alex.atpic.com', b'/wiki/europe/_delete', b'get delete uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'/europe')], [b'get',b'delete'], b'owner')),




(b'POST', b'http://alex.atpic.com', b'/wiki/europe/_put', b'post put uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'/europe')], [b'post',b'put'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/wiki/europe/_post', b'post post uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'/europe')], [b'post',b'post'], b'owner')),
(b'POST', b'http://alex.atpic.com', b'/wiki/europe/_delete', b'post delete uname_wiki_', ([(b'uname', b'alex')], [(b'wiki', b'/europe')], [b'post',b'delete'], b'owner')),





(b'***********wiki children **********',),



(b'GET', b'http://atpic.com', b'/wiki/_link', b'get atpiccom/wiki_link/', ([(b'atpiccom', None)], [(b'wiki', b''),(b'link',None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/API/_link', b'get atpiccom/wiki_link/', ([(b'atpiccom', None)], [(b'wiki', b'/API'),(b'link',None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/API/pictures/_link', b'get atpiccom/wiki_link/', ([(b'atpiccom', None)], [(b'wiki', b'/API/pictures'),(b'link',None)], [b'get'], b'anonymous')),








(b'GET', b'http://atpic.com', b'/wiki/europe/_revision', b'get atpiccom/wiki_revision/', ([(b'atpiccom', None)], [(b'wiki', b'/europe'),(b'revision',None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/europe/_revision/xxxxx', b'get atpiccom/wiki_revision_', ([(b'atpiccom', None)], [(b'wiki', b'/europe'),(b'revision',b'xxxxx')], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/europe/_revision/xxxxx,yyyyy', b'get atpiccom/wiki_revision_', ([(b'atpiccom', None)], [(b'wiki', b'/europe'),(b'revision',b'xxxxx,yyyyy')], [b'get'], b'anonymous')),

(b'GET', b'http://atpic.com', b'/wiki/_revision', b'get atpiccom/wiki_revision/', ([(b'atpiccom', None)], [(b'wiki', b''),(b'revision',None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/_revision/xxxxx', b'get atpiccom/wiki_revision_', ([(b'atpiccom', None)], [(b'wiki', b''),(b'revision',b'xxxxx')], [b'get'], b'anonymous')),




(b'GET', b'http://atpic.com', b'/wiki/_deadlink', b'get atpiccom/wiki_deadlink/', ([(b'atpiccom', None)], [(b'wiki', b''),(b'deadlink',None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/API/_deadlink', b'get atpiccom/wiki_deadlink/', ([(b'atpiccom', None)], [(b'wiki', b'/API'),(b'deadlink',None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/API/pictures/_deadlink', b'get atpiccom/wiki_deadlink/', ([(b'atpiccom', None)], [(b'wiki', b'/API/pictures'),(b'deadlink',None)], [b'get'], b'anonymous')),



(b'GET', b'http://atpic.com', b'/wiki/_linktothis', b'get atpiccom/wiki_linktothis/', ([(b'atpiccom', None)], [(b'wiki', b''),(b'linktothis',None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/API/_linktothis', b'get atpiccom/wiki_linktothis/', ([(b'atpiccom', None)], [(b'wiki', b'/API'),(b'linktothis',None)], [b'get'], b'anonymous')),
(b'GET', b'http://atpic.com', b'/wiki/API/pictures/_linktothis', b'get atpiccom/wiki_linktothis/', ([(b'atpiccom', None)], [(b'wiki', b'/API/pictures'),(b'linktothis',None)], [b'get'], b'anonymous')),





(b'GET', b'http://alex.atpic.com', b'/wiki/europe/_revision', b'get uname_wiki_revision/', ([(b'uname', b'alex')], [(b'wiki', b'/europe'),(b'revision',None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/wiki/europe/_revision/xxxxx', b'get uname_wiki_revision_', ([(b'uname', b'alex')], [(b'wiki', b'/europe'),(b'revision',b'xxxxx')], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/wiki/europe/_revision/xxxxx,yyyyy', b'get uname_wiki_revision_', ([(b'uname', b'alex')], [(b'wiki', b'/europe'),(b'revision',b'xxxxx,yyyyy')], [b'get'], b'anonymous')),

(b'GET', b'http://alex.atpic.com', b'/wiki/_revision', b'get uname_wiki_revision/', ([(b'uname', b'alex')], [(b'wiki', b''),(b'revision',None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/wiki/_revision/xxxxx', b'get uname_wiki_revision_', ([(b'uname', b'alex')], [(b'wiki', b''),(b'revision',b'xxxxx')], [b'get'], b'anonymous')),

(b'GET', b'http://alex.atpic.com', b'/wiki/europe/_link', b'get uname_wiki_link/', ([(b'uname', b'alex')], [(b'wiki', b'/europe'),(b'link',None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/wiki/europe/_deadlink', b'get uname_wiki_deadlink/', ([(b'uname', b'alex')], [(b'wiki', b'/europe'),(b'deadlink',None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/wiki/europe/_picture', b'get uname_wiki_picture/', ([(b'uname', b'alex')], [(b'wiki', b'/europe'),(b'picture',None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/wiki/europe/_linktothis', b'get uname_wiki_linktothis/', ([(b'uname', b'alex')], [(b'wiki', b'/europe'),(b'linktothis',None)], [b'get'], b'anonymous')),





(b'GET', b'http://alex.atpic.com', b'/wiki/_link', b'get uname_wiki_link/', ([(b'uname', b'alex')], [(b'wiki', b''),(b'link',None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/wiki/_deadlink', b'get uname_wiki_deadlink/', ([(b'uname', b'alex')], [(b'wiki', b''),(b'deadlink',None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/wiki/_picture', b'get uname_wiki_picture/', ([(b'uname', b'alex')], [(b'wiki', b''),(b'picture',None)], [b'get'], b'anonymous')),
(b'GET', b'http://alex.atpic.com', b'/wiki/_linktothis', b'get uname_wiki_linktothis/', ([(b'uname', b'alex')], [(b'wiki', b''),(b'linktothis',None)], [b'get'], b'anonymous')),
(b'*********** old legacy urls **********',),


(b'GET', b'http://u6166.direct.atpic.com', b'/36462/0/2222081/0.gif', b'get legacy/', ([(b'legacy', None)], [], [b'get'], b'anonymous')),


]



# signature (b'object',True),(b'object',False)



paths_id_legacy=[
(b"/999",[(b'id', b'999')]),
(b"/999/1024",[(b'id', b'999')]),
(b"/fr/999",[(b'id', b'999')]),
(b"/999/mysecret",[(b'id', b'999'), (b'secret', b'mysecret')]),
(b"/fr/999/mysecret",[(b'id', b'999'), (b'secret', b'mysecret')]),
(b"/999/1024/mysecret",[(b'id', b'999'), (b'secret', b'mysecret')]),
(b"/171546/0/jtfgimzxcdylugbmebyq",[(b'id', b'171546'), (b'secret', b'jtfgimzxcdylugbmebyq')]),
(b"/fr/171546/600/jtfgimzxcdylugbmebyq",[(b'id', b'171546'), (b'secret', b'jtfgimzxcdylugbmebyq')]),
(b"/fr/1538986",[(b'id', b'1538986')]),
(b"/de/1282892/600",[(b'id', b'1282892')]),
]

paths_path=[
b"/path",
b"/path/",
b"/path/france",
b"/path/france/",
b"/path/france/paris",
b"/path/france/paris/",
b"/path/france/paris/eiffel_tower",
]


paths_ymd=[
b"/blog/2009",
# "/blog/2009.xml",
# "/blog/2009.xml.xsl",
b"/blog/2009/12",
# "/blog/2009/12.xml",
# "/blog/2009/12.xml.xsl",
b"/blog/2009/12/31",
# "/blog/2009/12/31.xml",
# "/blog/2009/12/31.xml.xsl",
]

hosts=[
b"www.atpic.com",
b"alex.atpic.com",
b"pic.atpic.com",
b"gallery.atpic.com",
b"faq.atpic.com",
b"www.atpic.faa",
b"alex.atpic.faa",
b"my.photo.com", # sell DNS

]



class dispatcherURLtest(unittest.TestCase):
    """USER legacy urls"""
    def testMainURLsGET(self):
        print("******** test dispatcher ********")
        i=0
        bigurls=[fileurls]
        for urls in bigurls:
            print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")

            for url in urls:
                thelen=len(url)
                if thelen==1:
                    print("XXXX",url,",",sep="")
                else:
                    i=i+1
                    print("----%s -------------" % i)
                    environ={}
                    environ[b'REQUEST_METHOD']=url[0]
                    print("input=%s %s%s" % (url[0],url[1],url[2]))
                    urltuple=urllib.parse.urlsplit(url[1]+url[2])
                    # print(urltuple)
                    environ[b'HTTP_HOST']=urltuple[1]
                    environ[b'PATH_INFO']=urltuple[2]
                    environ[b'QUERY_STRING']=urltuple[3]
                    response=atpic.dispatcher.dispatcher(environ)
                    print('response=',response)
                    
                    signature=atpic.dispatcher.signature(atpic.xplo.Xplo(response[0]),atpic.xplo.Xplo(response[1]),response[2])
                    print("ZZZ ",signature,",",sep='')

                    a=(url[0],url[1],url[2],signature,response)
                    print("XXXX",a,",",sep="")

                    self.assertEqual(response,url[4])
                    self.assertEqual(signature,url[3])

    def NOtestgetid_legacy(self):
        print("******** test get_id_legacy ********")
        for line in paths_id_legacy:
            print("%s ->" % (line[0]))
            adic=[]
            adic=atpic.dispatcher.get_id_legacy(line[0],adic)
            print('XXXX   ',line[0],',',adic,"),",sep="")
            self.assertEqual(line[1],adic)

    def NOtestgetymd(self):
        print("******** test get_ymd ********")
        for path in paths_ymd:
            print("%s ->" % (path))
            adic={}
            path,adic=atpic.dispatcher.get_ymd(path,adic)
            print("   %s, %s" % (path,adic))

    def NOtestgetpath(self):
        print("******** test get_path ********")
        for path in paths_path:
            print("%s ->" % (path))
            adic={}
            path,adic=atpic.dispatcher.get_tree(path,adic)
            print("   %s, %s" % (path,adic))

    def NOtestgetudomain(self):
        print("******** test get_udomain ********")
        for host in hosts:
            print(" ->" ,host)
            adic={}
            host,adic=atpic.dispatcher.get_udomain(host,adic)
            print("  ",host,adic)

if __name__=="__main__":


    unittest.main()
