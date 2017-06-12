#!/usr/bin/python3
import atpic.elasticsearch_client
import unittest

class elasticsearch_test(unittest.TestCase):
    def test_query(self):
        inputs=(
            (b'1',b'/italia2006',b'1',b''),
            )
        for (uid,path,aid,ajson_expect) in inputs:
            ajson=atpic.elasticsearch_client.forge_facet_path_search(uid,path,aid)
            print(ajson)

if __name__=="__main__":
    unittest.main()
