#!/usr/bin/python3

import urllib.parse

import atpic.errors
import atpic.log


"""
A pure security oriented module
aimed at blocking CSRF attacks

As we use HTML content types allowed by the HTTP POST methode
we are particularly vulnerable.

The solution is based on the Referer header:
we do not use tokens.
It's a good compromise between security and simplicity.

Of course it assumes that the attack does not originates from our site,
hence we need to prevent users from creating their own HTML forms.
"""

xx=atpic.log.setmod("INFO","anticsrf")


def isattack(environ):
    # easy to unit test
    yy=atpic.log.setname(xx,'isattack')
    atpic.log.debug(yy,'input=',environ)
    attack=False

    method=environ.get(b'REQUEST_METHOD')
    atpic.log.debug(yy,'method=',method)
    if method!=b'GET':
        referer=environ.get(b'HTTP_REFERER',b'')
        atpic.log.debug(yy,'referer=',referer)
        if referer!=b'':
            host=environ.get(b'HTTP_HOST',b'')
            atpic.log.debug(yy,'host=',host)
            parsed=urllib.parse.urlparse(referer)
            atpic.log.debug(yy,'parsed=',parsed)
            referer_hostname=parsed.hostname
            atpic.log.debug(yy,'referer_hostname=',referer_hostname)
            if referer_hostname!=host:
                atpic.log.debug(yy,'referer is not correct, possible ATTACK')
                attack=True
    atpic.log.debug(yy,'output=',attack)
    return attack          


def protect(environ):
    yy=atpic.log.setname(xx,'protect')
    atpic.log.debug(yy,'input=',environ)
    attack=isattack(environ)

    if attack:
        atpic.log.debug(yy,'attempt to attack')
        raise atpic.errors.AnticsrfError
    else:
        atpic.log.debug(yy,'no attack')
