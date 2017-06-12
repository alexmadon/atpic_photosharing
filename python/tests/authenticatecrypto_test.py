#!/usr/bin/python3

import atpic.authenticatecrypto
import atpic.xplo
import atpic.mybytes

import unittest
import time



class authenticatecrypto_test(unittest.TestCase):
    """USER legacy urls"""
    def NOtest_login_redirect(self):
        inputs=(
                ([],b'alex',{},()),
                )
        for (headers,servershort,environ,expect) in inputs: 
            res=atpic.authenticatecrypto.login_redirect(headers,servershort,environ)
            print(res)

    def NNOtest_authenticate_nosql(self):
        inputs=(
            ([(b'atpiccom', None)], [(b'user', None)], [b'get'],{ b'HTTP_HOST': b'atpic.faa',b'PATH_INFO': b'/user',b'REQUEST_URI': b'/user',}, [], (False, (), [])),
            ([(b'atpiccom', None)], [(b'user', None)], [b'get'],{ b'HTTP_HOST': b'atpic.faa',b'PATH_INFO': b'/user',b'REQUEST_URI': b'/user',b'HTTP_COOKIE': b'session='+atpic.authenticatecrypto.make_session(b'session',b'atpic.com',atpic.mybytes.int2bytes(int(time.time())),b'1', b'alex', b'Alex M'),}, [], (True, (b'1', b'alex', b'Alex M'), [])),
            ([(b'atpiccom', None)], [(b'user', None)], [b'get'],{ b'HTTP_HOST': b'atpic.faa',b'PATH_INFO': b'/user',b'REQUEST_URI': b'/user',b'HTTP_COOKIE': b'session='+atpic.authenticatecrypto.make_session(b'session',b'atpic.com',atpic.mybytes.int2bytes(int(time.time())-3601),b'1', b'alex', b'Alex M'),}, [], (False, (), [])),

            )
        for (ahxplo,apxplo,actions,environ,headers,expect) in inputs:
            hxplo=atpic.xplo.Xplo(ahxplo)
            pxplo=atpic.xplo.Xplo(apxplo)
            res=atpic.authenticatecrypto.authenticate_nosql(hxplo,pxplo,actions,environ,headers)
            print('VVVV',(hxplo.list(),pxplo.list(),actions,environ,headers,res))
            self.assertEqual(res,expect)

    def NOtest_session(self):
        (servicetype,servicename,timeseconds,uid,username,displayname)=(b'session', b'atpic.com', b'1367001641', b'1', b'alex', b'Alex M')


        # (b'session', b'atpic.com', b'1367001424', b'1', b'alex', b'Alex M') 
        # (b'SS',b'sn',b'1111',b'1',b'alex',b'Alex M')
        session=atpic.authenticatecrypto.make_session(servicetype,servicename,timeseconds,uid,username,displayname)
        print('session',session)
        res=atpic.authenticatecrypto.decode_session(session,servicetype,servicename)
        self.assertEqual(res,(servicetype,servicename,timeseconds,uid,username,displayname))



    def NOtestPassword(self):
        """Legacy User ID"""
        password=b'testuser59'
        salt=b'76'
        crypted=b'76TfT2JxBotNI'
        self.assertEqual(atpic.authenticatecrypto.mycrypt(password,salt),crypted)


    def NOtest_get_session_from_cookie(self):
        cookies=(
            (b'session=alex;',b'alex'),
            (b"chips=ahoy; vienna=finger",b''),
            )
        for (cookie,session_ex) in cookies:
            env={b"HTTP_COOKIE":cookie}
            ses=atpic.authenticatecrypto.get_session_from_cookie(env)
            print('ses=',ses)
            self.assertEqual(ses,session_ex)




    def NOtest_append_st(self):
        inputs=[
            (b'http://some.faa',b'FFF',b'http://some.faa?st=FFF'),
            (b'http://some.faa/?f=xml',b'FFF',b'http://some.faa/?f=xml&st=FFF'),
            (b'http://some.faa/user?f=xml',b'FFF',b'http://some.faa/user?f=xml&st=FFF'),
            (b'http://some.faa/user?f=xml#id1',b'FFF',b'http://some.faa/user?f=xml&st=FFF'),
            ]
        for (url,session,newex) in inputs:
            newurl=atpic.authenticatecrypto.append_service_ticket(url,session)
            print('YYY',(url,session,newurl),',')
            self.assertEqual(newurl,newex)

    def test_redirect(self):
        inputs=[
            ([(b'selldns', b'pdns.faa')], [], [b'get'], b'anonymous',{b'wsgi.url_scheme': b'http',b'SERVER_PORT': b'80',b'HTTP_HOST': b'pdns.faa',b'REQUEST_URI': b'/',b'QUERY_STRING': b''},(True, b'http://atpic.faa/redirect?url=http%3A%2F%2Fpdns.faa%2F', [])),
            ([(b'atpiccom', None)], [(b'redirect', None)], [b'get'], b'anonymous', {b'wsgi.url_scheme': b'http',b'SERVER_PORT': b'80',b'HTTP_HOST': b'atpic.faa',b'REQUEST_URI':  b'/redirect?url=http%3A%2F%2Fpdns.faa%2F',b'QUERY_STRING': b'url=http%3A%2F%2Fpdns.faa%2F'},(True, b'http://pdns.faa/?st=notauthenticated', [])),
            ([(b'selldns', b'pdns.faa')], [], [b'get'], b'anonymous', {b'wsgi.url_scheme': b'http',b'SERVER_PORT': b'80',b'HTTP_HOST': b'pdns.faa',b'REQUEST_URI': b'/?st=notauthenticated',b'QUERY_STRING': b'st=notauthenticated'},(False, b'', [(b'Set-Cookie', b'alreadychecked=1; Domain=pdns.faa;')])),
            ([(b'selldns', b'pdns.faa')], [], [b'get'], b'anonymous', {b'wsgi.url_scheme': b'http',b'SERVER_PORT': b'80',b'HTTP_HOST': b'pdns.faa',b'REQUEST_URI': b'/?f=xml',b'QUERY_STRING':  b'f=xml'},(True, b'http://atpic.faa/redirect?url=http%3A%2F%2Fpdns.faa%2F%3Ff%3Dxml', [])),
            ([(b'atpiccom', None)], [(b'redirect', None)], [b'get'], b'anonymous', {b'wsgi.url_scheme': b'http',b'SERVER_PORT': b'80',b'HTTP_HOST': b'atpic.faa',b'REQUEST_URI': b'/redirect?url=http%3A%2F%2Fpdns.faa%2F%3Ff%3Dxml',b'QUERY_STRING':  b'url=http%3A%2F%2Fpdns.faa%2F%3Ff%3Dxml'},(True, b'http://pdns.faa/?f=xml&st=notauthenticated', [])),
            ([(b'selldns', b'pdns.faa')], [], [b'post'], b'anonymous',{b'wsgi.url_scheme': b'http',b'SERVER_PORT': b'80',b'HTTP_HOST': b'pdns.faa',b'REQUEST_URI': b'/',b'QUERY_STRING': b''},(False, b'', [])),


            ([(b'legacyobject', b'wiki')], [], [b'get'], b'anonymous',{},(False, b'', [])),
            
            ([(b'legacyobject', b'pic')], [(b'id', b'1569')], [b'get'], b'anonymous',{},(False, b'', [])),
            ([(b'legacy', None)], [], [b'get'], b'anonymous',{},(False, b'', [])),



            ]
        for (ahxplo,apxplo,actions,autor,environ,resex) in inputs:
            hxplo=atpic.xplo.Xplo(ahxplo)
            pxplo=atpic.xplo.Xplo(apxplo)
            res=atpic.authenticatecrypto.check_redirect(hxplo,pxplo,actions,autor,environ)
            print('XXXX',(ahxplo,apxplo,actions,autor,environ,res),',')
            self.assertEqual(res,resex)
            

if __name__=="__main__":
    print("ddd")
    unittest.main()

