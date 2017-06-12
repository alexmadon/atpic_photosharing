#!/usr/bin/python3
import atpic.log

"""
Implement a ticket based authentication similar to CAS.
This allows to securely implemement Single Sign On (SSO).
To be secure the ticket needs to be valid for one service only.
The service is the user DNS (white box).
Session is stored in redis.
It allows 'logout'.
Redis has the TTL feature.

or each server share a secret: DES3 symmetric encoding decoding
python3-openssl or ctypes?
openssl enc -e -des3 -k secret -in test.txt -out test.txt.enc  
openssl enc -d -des3 -k secret -in test.txt.enc -out test.txt.dec 
(-a)
svn checkout http://ctypescrypto.googlecode.com/svn/trunk/ ctypescrypto-read-only 
(openssl ctypes)

Problem: unlike the redis used by filesystem, sharding is less obvious?
One big central redis server for session management?
http://wanderr.com/jay/redis-saves-and-ruins-the-day/2010/05/16/

so we could do only service ticket in a central redis (db to invalidate 'use once')
and use the in cookie hash or relax the requirement on invalidate

or store on the user dns mapping (pdns.com -> userofpdns.atpic.com)
and have this servershort put in the name of the session

In redis:
-----
atpic_session=uid|uname|servershort

================ticket granting cookie TGC
http://www.unicon.net/node/1268
The ticket granting cookie TGT is typically an SSL-vended, tightly-scoped (just for your CAS server), session-scoped (expired by your browser when your browser session ends) cookie.

is login ticket necessary? bug in browsers that allow to replay

================service ticket ST_
service_ticket=uid|uname|servershort|service
http://www.unicon.net/node/1269
ST
The service ticket is typically an SSL-vended, tightly-scoped (just for your CAS server and just for the purpose of authenticating to one identified service), short-lived (expired by the CAS server after a configurable duration of time that defaults to five minutes) URL parameter.
Service Tickets are too hard to guess

Service tickets are generated randomly using a sufficient length and a sufficiently large set of characters such that they are cryptographically impossible to guess within their short lifespan.
Service Tickets are not replayable

Service tickets are one-time-use only. 

A CAS server will successfully validate a given service ticket only once, and only when the validator declares the service to which it properly authenticates, and only within the short window of time within which a given service ticket is valid. Since each service ticket has associated with it in the CAS server ticket store the identifier of the service to which it is intended to authenticate, that service cannot use a not-yet-validated ticket as an illicit delegation credential with which to access another service, which other service will specify itself, not the misbehaving service, as the service identifier to which it is 

==============
service_session: a cookie for that service (site)


https://bitbucket.org/desmaj/wsgicas/src
hg clone https://bitbucket.org/desmaj/wsgicas

http://www.jasig.org/cas/protocol

http://wiki.case.edu/Central_Authentication_Service
logout

"""


xx=atpic.log.setmod("INFO","authenticateredis")



if __name__ == "__main__":
    print('hi')
