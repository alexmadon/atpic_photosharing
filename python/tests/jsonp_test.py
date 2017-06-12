# -*- coding: utf-8 -*-
import unittest



import atpic.jsonp


query={
"action":"insert",
"field1":"value1",
"field2":u"cet été là",
}

class json_test(unittest.TestCase):
    """JSON protocols"""

   
    def test_jsonproto(self):
        query_new=atpic.jsonp.unserialize(atpic.jsonp.serialize(query))
        self.assertEqual(query["action"],query_new["action"])
        self.assertEqual(query["field1"],query_new["field1"])
        self.assertEqual(query["field2"],query_new["field2"])



if __name__ == "__main__":
    unittest.main()
