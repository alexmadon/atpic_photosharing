$ curl -XPOST 'http://localhost:9200/twitter/tweet?routing=kimchy' -d '{
    "user" : "kimchy",
    "postDate" : "2009-11-15T14:12:12",
    "message" : "trying out Elastic Search"
}
'

=======================

$ curl -XGET 'http://localhost:9200/twitter/tweet/_search?routing=kimchy' -d '{
    "query": {
        "filtered" : {
            "query" : {
                "query_string" : {
                    "query" : "some query string here"
                }
            },
            "filter" : {
                "term" : { "user" : "kimchy" }
            }
        }
    }
}
'

=======================

curl -XGET 'http://localhost:9200/atpic/pic/_search?routing=1' -d '{
    "query": {
        "filtered" : {
            "query" : {
                "query_string" : {
                    "query" : "*:*"
                }
            },
            "filter" : {
                "term" : { "user" : "1" }
            }
        }
    }
}
'
==============


Simple wildcard can also be used to search “within” specific inner elements of the document. For example, if we have a city object with several fields (or inner object with fields) in it, we can automatically search on all “city” fields:

{
    "query_string" : {
        "fields" : ["city.*"],
        "query" : "this AND that OR thus",
        "use_dis_max" : true
    }
}

=================validate======

curl -XGET 'http://localhost:9200/twitter/_validate/query?q=user:foo'
{"valid":true,"_shards":{"total":1,"successful":1,"failed":0}}

Or, with a request body:

---------------------

curl -XGET 'http://localhost:9200/twitter/tweet/_validate/query' -d '{
  "filtered" : {
    "query" : {
      "query_string" : {
        "query" : "*:*"
      }
    },
    "filter" : {
      "term" : { "user" : "kimchy" }
    }
  }
}'



{"valid":true,"_shards":{"total":1,"successful":1,"failed":0}}





curl -XGET 'http://localhost:9200/log2013/journal/_search'
curl -XGET 'http://localhost:9200/log2013/journal/_search?pretty=1'
curl -XGET 'http://localhost:9200/log2013/journal/_search?q=aid:1&pretty=1'
curl -XGET 'http://localhost:9200/log2013/journal/973838e5-909c-408a-bcec-d4a9dd6d6785?pretty=1'
