#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
import atpic.composite


class compositetest(unittest.TestCase):
    """USER legacy urls"""
    def testExplode(self):
        list1=[
            ((b"<a><b><composite><link>url1</link><link>url2</link></composite></b></a>",b'atpic.com'),(b'<a><b>', b'</b></a>', [b'url1', b'url2'])),
            ((b"<a><b><c>blah</c><composite><link>url1</link><link>url2</link></composite></b></a>",b'atpic.com'),(b'<a><b><c>blah</c>', b'</b></a>', [b'url1', b'url2'])),
            ((b"<composite><link>http://atpic.com/login</link><link>http://atpic.com/search?sort=random</link><link>http://atpic.com/news</link></composite>",b'atpic.com'),(b'',b'',[b'http://atpic.com/login', b'http://atpic.com/search?sort=random', b'http://atpic.com/news'])),
            ((b"<composite><link>http://atpic.com/login</link><link>http://atpic.com/search?sort=random</link><link>http://atpic.com/news</link></composite>",b'atpic.faa'),(b'',b'',[b'http://atpic.faa/login', b'http://atpic.faa/search?sort=random', b'http://atpic.faa/news'])),
            # (b"<composite><link>http://atpic.com/login</link><link>http://atpic.com/search?sort=random</link><link>http://atpic.com/news</link></composite>",b'atpic.faa',[b'http://atpic.faa/login', b'http://atpic.faa/search?sort=random', b'http://atpic.faa/news']),

]
        # for (xmlcomposite, host,expected_listoflinks) in list1:
        # host=b'atpic.faa'
        for ((xmlcomposite,host),expected) in list1:
            pass
            listoflinks=atpic.composite.explode(xmlcomposite,host)
            print(listoflinks)
            self.assertEqual(listoflinks,expected)


    def NOtestCreateenv(self):

        listenv=[
            (b"http://atpic.com/login?f=xml",
             {b'HTTP_HOST':b'',b'PATH_INFO':b'',b'QUERY_STRING':b''},
             {b'QUERY_STRING': b'f=xml', b'HTTP_HOST': b'atpic.com', b'PATH_INFO': b'/login',b'REQUEST_URI': b'/login?f=xml'}),
            (b"http://atpic.com/login",
             {b'HTTP_HOST':b'',b'PATH_INFO':b'',b'QUERY_STRING':b'f=xml'},
             {b'QUERY_STRING': b'f=xml', b'HTTP_HOST': b'atpic.com', b'PATH_INFO': b'/login',b'REQUEST_URI': b'/login?f=xml'}),
            (b"http://atpic.com/login?foo=bar",
             {b'HTTP_HOST':b'',b'PATH_INFO':b'',b'QUERY_STRING':b'f=xml'},
             {b'QUERY_STRING': b'foo=bar&f=xml', b'HTTP_HOST': b'atpic.com', b'PATH_INFO': b'/login',b'REQUEST_URI': b'/login?foo=bar&f=xml'}),
            ]
        i=0
        for (url,env,newenv) in listenv:
            i=i+1
            print('+++++++++',i,'+++++++++++++')
            newenv_expected=atpic.composite.create_env(url,env)
            print(newenv)
            print(newenv_expected)
            self.assertEqual(newenv_expected,newenv)
            print('\n')

if __name__=="__main__":
    unittest.main()
