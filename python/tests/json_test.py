# import json
# import simplejson
import cjson
import unittest

"""
Can also do:

~/json/jsonval/jsonval  ~/public_html/perso/entreprise/sql_current/site/atpic/python/tests/fixture/json/pic.json 


see

http://www.blik.it/2007/06/24/a-json-validator/
http://www.jsonlint.com/
"""


class jsonPic(unittest.TestCase):
    """Json"""


    def testJsonPic1(self):
        """Testing Json"""
        json_file=open("fixture/json/pic.json","r")
        json_string=json_file.read()
        json_file.close()
        print json_string
        python=cjson.decode(json_string)
        print python

if __name__=="__main__":
    unittest.main()
