#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse
import io



import atpic.validate
import atpic.xmlob

class validate_test(unittest.TestCase):
    """Validate tests"""
    def test_validate_simple(self):
        inputs=(
            (
                ({b'title':[b'Macro4']},[]),
                {},[],[],[],{},
                ( 
                    ({b'title': [b'Macro4']}, []),
                    {b'title': [b'title cannot be Macro4', b'title cannot contain 4']}
                    )
                ),

       (
                ({b'captchahidden': [b'78515'], b'captchapublic': [b'3553257016741604514572636108748']}, []) , 
                {b'captchahidden': [b'captcha error']} , 
                [(b'atpiccom', None)] ,
                [(b'user', None)] , 
                [b'post', b'post'] , 
                {},
                ( ({b'captchahidden': [b'78515'], b'captchapublic': [b'3553257016741604514572636108748']}, []) , {b'password': [b'password cannot be empty'], b'login': [b'login cannot be empty'], b'email': [b'email cannot be empty'], b'captchahidden': [b'captcha error']} )
            ),




            )
        
        i=0
        for (indata,dataerror,hxplo1,pxplo1,actions,environ,expect) in inputs:
            i=i+1
            print('++++++++',i,'++++++++++')
            print('doing',hxplo1,pxplo1,actions)
            hxplo=atpic.xplo.Xplo(hxplo1)
            pxplo=atpic.xplo.Xplo(pxplo1)
            res=atpic.validate.validate_simple(indata,dataerror,hxplo,pxplo,actions,environ)
            self.assertEqual(res,expect)



if __name__=="__main__":
    unittest.main()
