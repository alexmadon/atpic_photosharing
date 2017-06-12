curl -XDELETE localhost:9200/wurfl

curl -XPOST localhost:9200/wurfl -d @create_wurfl.json
curl "localhost:9200/wurfl/_settings?pretty=1"
curl -XPUT 'http://localhost:9200/wurfl/agent/_mapping' -d @schema_wurfl.json
# curl -POST localhost:9200/wurlf/agent/_bulk --data-binary @wurfl_data.json

# curl -XGET 'localhost:9200/wurfl/_analyze?field=agent.ua&pretty=1' -d 'Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; Smartphone; 176x220; Smartphone; 176x220; SPV C500; OpVer 4.1.2.0)'
# should see shingle

# curl -XGET http://localhost:9200/wurfl/agent/_search?q=ua:"Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; Smartphone; 176x220; Smartphone; 176x220; SPV C500; OpVer 4.1.2.0)"
 curl -XGET "http://localhost:9200/wurfl/agent/_search?q=ua:4.1.2.0"

# http://localhost:9999/guide/reference/query-dsl/match-query.html


curl -XGET http://localhost:9200/wurfl/agent/_search?pretty=1 -d '{
 "query" : {
    "match" : {
        "ua" : { 
           "query": "Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; Smartphone; 176x220; Smartphone; 176x220; SPV C500; OpVer 4.1.2.0)"
           }
        }
     }
}'

# this will return exactly one html_wi_oma_xhtmlmp_1_0
curl -XGET http://localhost:9200/wurfl/agent/_search?pretty=1 -d '{
 "query" : {
    "match" : {
        "ua" : { 
           "query": "Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; Smartphone; 176x220; Smartphone; 176x220; SPV C500; OpVer 4.1.2.0)",
            "analyzer" : "myAnalyzer2",
            "type" : "phrase"
           }
        }
     }
}'





curl -XGET http://localhost:9200/wurfl/agent/_search?pretty=1 -d '{
    "query" : {
        "match_phrase" : { 
           "ua": "Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; Smartphone; 176x220; Smartphone; 176x220; SPV C500; OpVer 4.1.2.0)"
           }
    }
}'


curl -XGET http://localhost:9200/wurfl/agent/_search?pretty=1 -d '{
    "query" : {
        "match" : { 
           "ua": "Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; Smartphone; 176x220; Smartphone; 176x220; SPV C500; OpVer 4.1.2.0)"
           }
    },
    "size" : 2
}'




curl -XGET http://localhost:9200/wurfl/agent/_search?pretty=1 -d '{
    "query" : {
        "term" : { 
           "ua": "Mozilla/4.0"
           }
    }
}'



# should match first "orange_spv_c500_ver1_subopver4120"

curl -XGET http://localhost:9200/wurfl/_stats


curl -XGET http://localhost:9200/wurfl/_stats?pretty=1
