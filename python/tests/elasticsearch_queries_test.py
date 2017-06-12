#!/usr/bin/python3
import atpic.elasticsearch_queries
import atpic.queryparser
import unittest

class elasticsearch_queries_test(unittest.TestCase):
    def NOtest_parse2json(self):
        
        inputs=(
            b'alex madon',
            b'+"alex madon"',
            b'alex date:2012-12',
            b'alex +f:5.6to8.0',
            b'alex date:2012-01TO2012-09',
            b'alex +f:5.6to8.0 +speed:1to4',
            )
        i=0
        for query in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')
            print('XXX query is=',query)
            parsed=atpic.queryparser.parse_first(query)
            ajson=atpic.elasticsearch_queries.parsed2json(parsed,b'')
            print('XXX',ajson)


    def NOtest_parse2json_utf8(self):
        
        inputs=(
            '私の名前は中野です', # [['+', 'word', '私 の 名前 は 中野 です']]),
            '个性化首页', # [['+', 'word', '个 性 化 首 页']]),
            'แล้วพบกันใหม่', #[['+', 'word', 'แล้ว พบ กัน ใหม่']]),
            )
        i=0
        for query in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')
            print('query is=',query)
            parsed=atpic.queryparser.parse_first(query.encode('utf8'))
            ajson=atpic.elasticsearch_queries.parsed2json(parsed)
            ajson=ajson.decode('utf8')
            print(ajson)


    def NOtest_path(self):
        inputs=(
            (b'/nathalie', [(b'gpath', b'nathalie')]) ,
            (b'/nathalie/*', [(b'dir_0', b'/nathalie')]) ,
            (b'alex/nathalie', [(b'servershort', b'alex'), (b'gpath', b'nathalie')]) ,
            (b'alex/nathalie/*', [(b'servershort', b'alex'), (b'dir_0', b'/nathalie')]) ,
            )
        i=0
        for (avalue,alistex) in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')
            alist=atpic.elasticsearch_queries.get_path(avalue)
            print('HHH',(avalue,alist),',')
            self.assertEqual(alist,alistex)



    def NOtest_get_facet_geo_list(self):
        inputs=(
            (b'/-180/-90/180/90'),
            )
        i=0
        for (avalue) in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')
            alist=atpic.elasticsearch_queries.get_facet_geo_list(avalue)

    def test_get_facet_date_list(self):
        inputs=(
            (b'/2009',[]),
            (b'/2009/02',[]),
            (b'/2009/11',[]),
            (b'/2009/12',[]),
            (b'/200',[]),
            )
        i=0
        for (avalue,ex) in inputs:
            i=i+1
            print('++++++++++++++++',i,'++++++++++++++++++')
            alist=atpic.elasticsearch_queries.get_facet_date_list(avalue)
            print((avalue,alist))

if __name__=="__main__":
    unittest.main()
