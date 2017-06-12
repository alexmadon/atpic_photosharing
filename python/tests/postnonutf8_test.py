#!/usr/bin/python3
import unittest
import http.client

class worker_test(unittest.TestCase):
    """USER legacy urls"""

    def NOtest_notutf8(self):
        # curl -d "username=alexmadon&password=mypass" "http://atpic.faa/login?f=xml"
        # b='\xce\xb3\xce\xb5\xce\xb9\xff\xb1'    
        b='username=alexmadon&password=invalid\xff'
        con = http.client.HTTPConnection('atpic.faa:80')
        params=b
        headers={}
        headers = {
                   "Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain",
                   "User-Agent": "Mozilla",
                   }
        con.request("POST", "/login?f=xml", params, headers)
        r = con.getresponse()
        print(r.status,r.reason)
        content=r.readall()
        print(content)
        con.close()
        self.assertEqual(content,b"'utf-8' codec can't decode byte 0xff in position 35: invalid start byte")








    def test_no_user_agent(self):
        # tests: user_agent=atpic.wurflex.sxmlw(environ[b\'HTTP_USER_AGENT\'])\nKeyError: b\'HTTP_USER_AGENT\'\n'

        b='username=alexmadon&password=mypass'
        con = http.client.HTTPConnection('atpic.faa:80')
        params=b
        headers={}
        headers = {
                   "Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain",
                   }
        con.request("POST", "/login?f=xml", params, headers)
        r = con.getresponse()
        print(r.status,r.reason)
        content=r.readall()
        print(content)
        con.close()

if __name__=="__main__":
    unittest.main()
