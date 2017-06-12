# create table
# flow:
# buyer puts several lines in his cart (can update the cart)
# ====================================
# GET http://alex.atpic.com/cart (collection)
# POST add to cart a pic
# delete from cart an entry

# PROBLEM: we can sell pics AND storage

# then click on 
# POST http://alex.atpic.com/cart/_pay
# two methods: 
# 1) pay with virtual money if enough funds
# 2) pay with paypal
#
# method 1:
# --------
#
#
# method 2:
# --------
# buyer is redirected to paypal
# once payment is terminated
# atpic.com is notified 
# in details:
# 1) INSERT a new SQL line in 'orders' order status: CREATED, get orderID
# return URL should be complicated enough as there is a money exchange
# if user decides NOT to continue, he could try to validate 
# the order on atpic's side without paying
# 2) atpic does an API call to paypal (with return URL and orderID) 
# to get a preapproval key 
# 3) atpic redirects buyer to paypal with preapproval key
# 4) once completed, buyer is redirected to atpic; this triggers a change 
# of the order status: COMPLETED
# and move virtual money to the photographers, taggers, tax and atpic money accounts, and debit (paid) buyer (for accounting purposes)
# and empty the cart

# note all this move should be done in one transaction?
# or at least very easy to debug and with logs, with emails and fs write
# transaction is sharding? pl/proxy: http://wiki.postgresql.org/wiki/PL/Proxy
# or in partitions
#
# cf: http://plproxy.projects.postgresql.org/doc/faq.html
# There is no need for complex transaction handling as any multi-statement transactions can be put into functions. PL/Proxy can just execute all queries in autocommit mode.
# Simple autocommit transactions mean that the connection handling is simple and can be done automatically.

# then present the links to the downloadable files

# Note: the taggers' fee is calculated before the order is made (at cart level?)
# as you need to get the correct price, but correct price is calculatd very early (at pic search time)

# Note: in acounting DATE is very important, 
# so save the create date and completed date

# SIMPLIFY!

# needs clear URL scheme as table name and structure should be derived from URL?
# find out the views necessary, so you can get the best SQL scheme

# tagger money earned, tagger transactions, total money available
# photograher earned, pic sold, total money available
# buyer: pic purchased, list orders
# user: disk purchased, du, total avaiable, date end

# accounting like:
# ecriture/23/line/2909 (stored on main server)
# #################################################
# THIS IS THE ONE CHOSEN: entry/23/line/2909
# sharding by date
# premium per gallery (nb of times it was tagged, phrased)
# premium per pic (nb of times it was tagged, phrased)
# price set by the photographer

                Table "public._entry"
  Column   |            Type             | Modifiers 
-----------+-----------------------------+-----------
 id        | integer                     | not null
 _started  | timestamp without time zone | 
 _finished | timestamp without time zone | 
 _status   | character varying(127)      | 




         Table "public._entry_line"
  Column  |         Type         | Modifiers 
----------+----------------------+-----------
 id       | integer              | not null
 _entry   | integer              | 
 _account | integer              | 
 _amount  | real                 | 
 _type    | character varying(1) | 
 _user    | integer              | 
 _gallery | integer              | 
 _pic     | integer              | 
 _tag     | integer              | 
 _phrase  | integer              | 
 _storage | integer              | 

# _pic can be empty is tag is _user,_gallery related

# or based on the account (uid)
# account/11/transaction/123 (stored by uid)

# order/125/pic/999/line/156 (tagger:2,amount:+10)
# order/125/pic/999/line/156 (commission,atpic:1,amount:+10)
#                            type:pic, pay for hosting, move to paypal (withdraw)
# or
# order/125/pic/999/account/2/line/156 (type: pictagger, amount:+10)
# order/125/pic/999/account/2/line/157 (type: galtagger, amount:+1)
# order/125/pic/999/account/1/line/158 (type: photographer, amount:+100)
# order/125/pic/999/account/3/line/159 (type: buyer, amount:-320)

# order/125/pic/999/tagger/156 (or ptagger and gtagger)
# use a SQL VIEW for accounts

CREATE TABLE _user_cart(
id integer,
_user integer,
_seller integer,
_gallery integer,
_pic integer,
_price double,
)


# alex/galery/1/pic/22/selected/put
# to select and put in cart
# need to be careful with permissions
