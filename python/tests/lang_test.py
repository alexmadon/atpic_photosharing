#!/usr/bin/python3
# py3k version
"""Unit tests for lang module"""
import unittest


import atpic.lang

# needs
# apt-get install geoip-database

class dispatcherLangtest(unittest.TestCase):
    """Test lang guessing"""


    def test_get_lang_from_geo(self):

        known_ips=[
            (b"it",b"it"),
            (b"us",b"en"),
            (b"uk",b"en"),
            ]

        for test in known_ips:
            print("Doing %s" % test[0])
            environ={b"GEOIP_COUNTRY_CODE":test[0]}
            self.assertEqual(atpic.lang.get_lang_from_geo(environ),test[1])

    def test_get_lang_from_header(self):
        langheaders=[
            (b"da, en-gb;q=0.8, en;q=0.7",b"da"),
            (b"es-ve, en-gb;q=0.8, en;q=0.7",b"es"),
            ]
        for test in langheaders:
            print("Doing %s" % test[0])
            environ={b"HTTP_ACCEPT_LANGUAGE":test[0]}
            self.assertEqual(atpic.lang.get_lang_from_header(environ),test[1])

    def test_get_lang_from_cookie(self):
        cooks=(
            (b"chips=ahoy; vienna=finger",b""),
            (b"chips=ahoy; vienna=finger; lang=fr",b"fr"),
            )
        for cook in cooks:
            environ={b"HTTP_COOKIE":cook[0]}
            print(dir(cook[1]))
            self.assertEqual(atpic.lang.get_lang_from_cookie(environ),cook[1])


    def test_get_lang(self):
        envs=(
            ({b"HTTP_COOKIE":b"chips=ahoy; vienna=finger; lang=fr"},b"fr"),
            ({b"HTTP_ACCEPT_LANGUAGE":b"da, en-gb;q=0.8, en;q=0.7"},b"da"),
            ({b"GEOIP_COUNTRY_CODE":b'it'},b'it'),
            ({b'QUERY_STRING': b'lang=ru&amp;foo=bar'},b'ru'),
            ({},b'en'),
            ({b'QUERY_STRING': b'lang=ru&amp;foo=bar',b"GEOIP_COUNTRY_CODE":b'it'},b'ru'),
            ({b"HTTP_ACCEPT_LANGUAGE":b"da, en-gb;q=0.8, en;q=0.7",b"GEOIP_COUNTRY_CODE":b'it'},b"da"),
            ({b"HTTP_COOKIE":b"chips=ahoy; vienna=finger; lang=fr",b"HTTP_ACCEPT_LANGUAGE":b"da, en-gb;q=0.8, en;q=0.7"},b"fr"),
            )
        i=0
        for (env,res_ex) in envs:
            i=i+1
            print('++++++++++',i,'++++',env)
            res=atpic.lang.get_lang(env)
            self.assertEqual(res,res_ex)


if __name__=="__main__":
    unittest.main()
