# python3 version:
# no python3 module for geoip, use the apache module and var
import re
# apt-get install python-geoip 
# import GeoIP
# import logging
import atpic.log
import atpic.environment


xx=atpic.log.setmod("INFO","lang")

def get_lang_from_header(environ):
    """Parses the Accept-Language if exists"""
    yy=atpic.log.setname(xx,'get_lang_from_header')
    # http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.10
    # http://kbyanc.blogspot.com/2007/04/more-i-dig-through-code-more-paste-is.html
    # http://svn.pythonpaste.org/Paste/trunk/paste/httpheaders.py
    # http://pythonpaste.org/modules/httpheaders.html
    # http://deron.meranda.us/python/httpheader/httpheader.py

# The quality value defaults to "q=1". For example,

    # For example, 
    # Accept-Language: da, en-gb;q=0.8, en;q=0.7

    # would mean: "I prefer Danish, but will accept British English and other types of English. ...
    # www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
    # other example:
    #       en, en-US, en-cockney, i-cherokee, x-pig-latin
    foundlang=b""
    if b"HTTP_ACCEPT_LANGUAGE" in environ:
        # print "HTTP_ACCEPT_LANGUAGE======%s" % environ["HTTP_ACCEPT_LANGUAGE"]
        header=environ[b"HTTP_ACCEPT_LANGUAGE"]
        header=header.decode('utf8')
        # begin copy from http://svn.pythonpaste.org/Paste/trunk/paste/httpheaders.py
        langs = [v for v in header.split(",") if v]
        qs = []
        for lang in langs:
            pieces = lang.split(";")
            lang, params = pieces[0].strip().lower(), pieces[1:]
            q = 1
            for param in params:
                if '=' not in param:
                    # Malformed request; probably a bot, we'll ignore
                    continue
                lvalue, rvalue = param.split("=")
                lvalue = lvalue.strip().lower()
                rvalue = rvalue.strip()
                if lvalue == "q":
                    q = float(rvalue)
            qs.append((lang, q))
        atpic.log.debug(yy,"NotSorted",qs)
        # qs.sort(lambda a, b: -cmp(a[1], b[1]))
        # for py3k the above sort does not work anymore:
        # http://www.daniweb.com/code/snippet216801.html
        import operator
        index1 = operator.itemgetter(1)
        qs.sort(key=index1, reverse=True)
        atpic.log.debug(yy,"Sorted",qs)

        result=[lang for (lang, q) in qs]
        # end copy
        # print result
        if result[0]:
            firstlang=result[0]
            # print "firstlang=%s" % firstlang
            firstpart=firstlang.split("-")
            simplelang=firstpart[0]
            # print "simplelang=%s" % simplelang
            if simplelang.encode('utf8') in lang_array():
                foundlang=simplelang.encode('utf8')
    # print "HTTP_ACCEPT_LANGUAGE says use foundlang=%s" % foundlang
    return foundlang




def get_lang_from_geo(environ):
    """From the IP of the client host"""
    yy=atpic.log.setname(xx,'get_lang_from_geo')
    # this now uses an apache module
    lang=b""
    # if "REMOTE_ADDR" in environ:
    #    gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
    #    country=gi.country_code_by_addr(environ["REMOTE_ADDR"])
    if b"GEOIP_COUNTRY_CODE" in environ:
        country=environ[b"GEOIP_COUNTRY_CODE"]
        atpic.log.debug(yy,"Got country: %s" % country)
        country=country.lower()
        lang=country2lang(country)

    return lang







def lang_array():
    """
    array of 2 char languages supported xx has a special signification: no translation.
    RFC 3066
    http://www.i18nguy.com/unicode/language-identifiers.html
    """
    return [
        b"da",
        b"de",
        b"en",
        b"es",
        b"fr",
        b"it",
        b"jp",
        b"nl",
        b"no",
        b"pt",
        b"ru",
        b"xx", # NO LANGUAGE
        b"zh", # chinese
        ]


def country2lang(country):
    """returns the lang for a 2 letter country code"""
    lang=b""
    countries={
        b"co":b"es", # colombia
        b"cr":b"es", # costa rica
        b"cn":b"zh", # china
        b"cz":b"cs", # czech: csech
        b"fi":b"fi", # finland: finnish
        b"il":b"he", # israel=>hebrew
        b"mx":b"es",
        b"pe":b"es", # peru=>espagnol
        b"uk":b"en",
        b"gb":b"en",
        b"dk":b"da", # denmark=>danish
        b"us":b"en",
        b"fr":b"fr",
        b"gr":b"el", # greece=ellas
        b"de":b"de",
        b"be":b"fr",
        b"it":b"it",
        b"no":b"no", # norway=>norwegian
        b"pl":b"pl", # polan => polish
        b"ru":b"ru", # russian
        b"se":b"sv", # sweden=> svedish
        b"tr":b"tr", # turkey=>turkish
        b"ve":b"es", # venezuela=>espagnol
        b"za":b"en", # zouth africa=>english
        }
    if country in countries:
        lang=countries[country]
    return lang




def get_lang_from_query_string(environ):
    lang=atpic.environment.get_qs_key(environ,b'lang',b"")
    return lang

def get_lang_from_cookie(environ):
    val=atpic.environment.get_cookie(environ,b'lang')
    return val

def get_lang(environ):
    # define the lang precedence
    lang=b""
    lang=get_lang_from_query_string(environ)
    if lang==b"":
        lang=get_lang_from_cookie(environ)
    if lang==b"":
        lang=get_lang_from_header(environ)
    if lang==b"":
        lang=get_lang_from_geo(environ)
    if lang==b"":
        lang=b"en"
    return lang


if __name__=="__main__":
    unittest.main()
