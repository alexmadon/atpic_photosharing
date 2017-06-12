this is for elasticsearch
note: you analyze in pythin so need to store but not index original title
and index but not store tokenized title


--------------
Index Shard Allocation:
shard and repliquas allocation (per index!)
http://blog.sematext.com/2012/05/29/elasticsearch-shard-placement-control/
curl -XPUT 'localhost:9200/sematext1' -d '{
   "index.routing.allocation.include.zone" : "zone_one"
}'

index.routing.allocation.total_shards_per_node 
setting allows to control how many total shards for an index will be allocated per node.
--------------

for wurfl: a lot of repliquas: one per node
no need to use haproxy to elasticsearch if each node can connect to it on localhost (?)
repliquas placement using DNS?

curl http://localhost:9200
{
  "ok" : true,
  "status" : 200,
  "name" : "Asp",
  "version" : {
    "number" : "0.19.10",
    "snapshot_build" : false
  },
  "tagline" : "You Know, for Search"
}



logs:
index by date+ routing by user


pic:
routing by user
5 shards



curl -XPOST localhost:9200/pic -d '{
    "settings" : {
        "number_of_shards" : 5
    },
    "mappings" : {
        "type1" : {
            "_source" : { "enabled" : false },
            "properties" : {
                "field1" : { "type" : "string", "index" : "not_analyzed" }
            }
        }
    }
}'



curl -XPUT localhost:9200/atpic
{"ok":true,"acknowledged":true}

curl localhost:9200/atpic/_settings
{"pic":{"settings":{"index.number_of_shards":"5","index.number_of_replicas":"1","index.version.created":"191099"}}}


curl -XDELETE localhost:9200/atpic
{"ok":true,"acknowledged":true}


curl localhost:9200/atpic/_settings
{"error":"IndexMissingException[[pic] missing]","status":404}

curl -XPUT http://localhost:9200/atpic/pic/1 -d '{
    "title" : "Some Title",
    "text" : "Some Description"
}'
{"ok":true,"_index":"atpic","_type":"pic","_id":"1","_version":1}



curl http://localhost:9200/atpic/pic/1
{"_index":"atpic","_type":"pic","_id":"1","_version":1,"exists":true, "_source" : {
    "title" : "Some Title",
    "text" : "Some Description"
}}


curl http://localhost:9200/atpic/pic/_mapping
{"pic":{"properties":{"text":{"type":"string"},"title":{"type":"string"}}}}




curl 'localhost:9200/atpic/_analyze?pretty=1&analyzer=whitespace' -d 'foo,bar baz'
{
  "tokens" : [ {
    "token" : "foo,bar",
    "start_offset" : 0,
    "end_offset" : 7,
    "type" : "word",
    "position" : 1
  }, {
    "token" : "baz",
    "start_offset" : 8,
    "end_offset" : 11,
    "type" : "word",
    "position" : 2
  } ]
}

curl 'localhost:9200/atpic/_analyze?pretty=1' -d 'foo,bar baz'
{
  "tokens" : [ {
    "token" : "foo",
    "start_offset" : 0,
    "end_offset" : 3,
    "type" : "<ALPHANUM>",
    "position" : 1
  }, {
    "token" : "bar",
    "start_offset" : 4,
    "end_offset" : 7,
    "type" : "<ALPHANUM>",
    "position" : 2
  }, {
    "token" : "baz",
    "start_offset" : 8,
    "end_offset" : 11,
    "type" : "<ALPHANUM>",
    "position" : 3
  } ]
}

# http://www.elasticsearch.org/guide/reference/mapping/

curl -XPUT 'http://localhost:9200/my_index/my_type/_mapping' -d '
{"my_type":
 {"properties":
   {
    "title": {"type":"string", "store" : "yes"},
    "reference":{"type":"string", "index":"not_analyzed"}
   }
 }
}'

curl -XDELETE localhost:9200/atpic

curl -XPOST localhost:9200/atpic -d '{
    "settings" : {
        "number_of_shards" : 5
    },
    "mappings" : {
        "pic" : {
            "_source" : { "enabled" : false },
            "properties" : {
                "title" : { "type" : "string", "index" : "not_analyzed" }
            }
        }
    }
}'

curl localhost:9200/atpic/_settings

curl localhost:9200/atpic/pic/_mapping

==================================================================
OR BETTER, one by one:

curl -XDELETE localhost:9200/atpic

curl -XPOST localhost:9200/atpic -d '{
    "settings" : {
        "number_of_shards" : 5
    }
}'
curl localhost:9200/atpic/_settings

curl localhost:9200/atpic/_settings?pretty=1
{
  "atpic" : {
    "settings" : {
      "index.number_of_shards" : "5",
      "index.number_of_replicas" : "1",
      "index.version.created" : "191099"
    }
  }
}
'

curl -XDELETE localhost:9200/atpic/pic
curl -XPUT 'http://localhost:9200/atpic/pic/_mapping' -d @schema_json.json


curl -XPUT 'http://localhost:9200/atpic/pic/_mapping' -d '
{
    "pic" : {

        "dynamic_templates" : [
            {
                "store_generic" : {
                    "match" : "dir_*",
                    "match_mapping_type" : "string",
                    "mapping" : {
                        "store" : "no",
                        "type" : "string",
                        "index" : "not_analyzed"

                    },
		    {
                    "match" : "vdir_*",
                    "match_mapping_type" : "string",
                    "mapping" : {
                        "store" : "no",
                        "type" : "string",
                        "index" : "not_analyzed"

                    },
		    {	    
                    "match" : "rand_*",
                    "match_mapping_type" : "string",
                    "mapping" : {
                        "store" : "no",
                        "type" : "long",
                        "precision_step" : "8"
                    }
                }
            }
        ],
        "properties" : {
            "_id" : {"type" : "long", "store" : "yes"},
            "user" : {"type" : "long", "store" : "yes" },
            "username" : {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
            "servershort" : {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
            "gallery" : {"type" : "long", "store" : "yes"},
            "location" : {"type" : "geo_point", "store" : "yes"},
            "licence" : {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
            "dir" : {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer" : "whitespace"},
            "depth" : {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer" : "whitespace"},
            "path" : {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
            "pathtext" : {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
            "year" : {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
            "yearmonth" : {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
            "yearmonthday" : {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
            "price" : {"type" : "float", "store" : "yes"},
            "datetimeoriginalsql" : {"type" : "date", "store" : "yes"},
            "fnumber" : {"type" : "byte", "store" : "yes"},
            "speed" : {"type" : "short", "store" : "yes"},
            "mode" : {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
            "mime" : {"type" : "string", "store" : "yes", "index" : "not_analyzed"},
            "gtitle_source" : {"type" : "string", "store" : "yes", "index" : "no"},
            "gtitle" : {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer" : "whitespace"},
            "gtext" : {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer" : "whitespace"},
            "ptitle_source" : {"type" : "string", "store" : "yes", "index" : "no" },
            "ptitle" : {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer" : "whitespace"},
            "ptext" : {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer" : "whitespace"},
            "gtags" : {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer" : "whitespace"},
            "gphrases" : {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer" : "whitespace"},
            "ptags" : {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer" : "whitespace"},
            "pphrases" : {"type" : "string", "store" : "yes", "index" : "analyzed", "analyzer" : "whitespace"}
       }
    }
}
'

store the logarithm of speed as they are powers of 2

like that you get a flater distribution

 curl -XGET 'localhost:9200/atpic/_analyze?field=pic.dir_1&pretty=1' -d 'this is a test'


curl -XPUT http://localhost:9200/atpic/pic/1 -d '{
    "ptitle" : "Some Title",
    "ptags" : "Some Description",
"dir_1" : "some text"
}'
now if you redo the query it works:
 curl -XGET 'localhost:9200/atpic/_analyze?field=pic.dir_1&pretty=1' -d 'this is a test'
and you can see dir_1 in the _mapping

root-object-type.textile:p. Another option is to use @path_match@, which allows to match the dynamic template against the "full" dot notation name of the field (for example @obj1.*.value@ or @obj1.obj2.*@), with the respective @path_unmatch@.



curl http://localhost:9200/atpic/pic/_mapping?pretty=1


curl -XPUT http://localhost:9200/atpic/pic/1 -d '{
    "title" : "Some Title",
    "text" : "Some Description",
    "rand_1" : 12989
}'


curl -XGET 'localhost:9200/atpic/_analyze?field=pic.year' -d 'this is a test'

curl -XGET 'localhost:9200/atpic/_analyze?field=pic.year&pretty=1' -d 'this is a test'
{
  "tokens" : [ {
    "token" : "this is a test",
    "start_offset" : 0,
    "end_offset" : 14,
    "type" : "word",
    "position" : 1
  } ]
}
curl -XGET 'localhost:9200/atpic/_analyze?field=pic.rand_1&pretty=1' -d '61308'

curl -XGET 'localhost:9200/atpic/_analyze?field=pic.gtags&pretty=1' -d 'this is a test'
{
  "tokens" : [ {
    "token" : "this",
    "start_offset" : 0,
    "end_offset" : 4,
    "type" : "word",
    "position" : 1
  }, {
    "token" : "is",
    "start_offset" : 5,
    "end_offset" : 7,
    "type" : "word",
    "position" : 2
  }, {
    "token" : "a",
    "start_offset" : 8,
    "end_offset" : 9,
    "type" : "word",
    "position" : 3
  }, {
    "token" : "test",
    "start_offset" : 10,
    "end_offset" : 14,
    "type" : "word",
    "position" : 4
  } ]
}

curl -XPUT http://localhost:9200/atpic/pic/1 -d '{
   "title" : "Some Title",
   "text" : "Some Description",
   "rand_1" : 12989
}'


 curl -XGET 'localhost:9200/atpic/_analyze?field=pic.rand_1&pretty=1' -d '128888'
{
  "tokens" : [ {
    "token" : " \u0001\u0000\u0000\u0000\u0000\u0000\u0000\u0007nx",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "fullPrecNumeric",
    "position" : 1
  }, {
    "token" : "$\b\u0000\u0000\u0000\u0000\u0000\u0000>w",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "(@\u0000\u0000\u0000\u0000\u0000\u0003w",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : ",\u0004\u0000\u0000\u0000\u0000\u0000\u0000\u001F",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "0 \u0000\u0000\u0000\u0000\u0000\u0001",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "4\u0002\u0000\u0000\u0000\u0000\u0000\u0000",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "8\u0010\u0000\u0000\u0000\u0000\u0000",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "<\u0001\u0000\u0000\u0000\u0000\u0000",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "@\b\u0000\u0000\u0000\u0000",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "D@\u0000\u0000\u0000",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "H\u0004\u0000\u0000\u0000",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "L \u0000\u0000",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "P\u0002\u0000\u0000",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "T\u0010\u0000",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "X\u0001\u0000",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  }, {
    "token" : "\\\b",
    "start_offset" : 0,
    "end_offset" : 0,
    "type" : "lowerPrecNumeric",
    "position" : 1
  } ]

curl -XPUT http://localhost:9200/atpic/pic/1 -d '{
    "title" : "Some Title",
    "text" : "Some Description",
    "rand_2" : "12989"
}'
     "rand_1" : {
        "type" : "long"
      },
      "rand_2" : {
        "type" : "long",
        "precision_step" : 8
      },


SEARCH

$ curl -XGET http://localhost:9200/twitter/tweet/_search?q=user:kimchy

$ curl -XGET http://localhost:9200/twitter/tweet/_search -d '{
    "query" : {
        "term" : { "user": "kimchy" }
    }
}'

MULTIVALUE

curl -XPOST localhost:9200/test
curl -XPUT localhost:9200/test/multi/1 -d '{"data" : ["one","two"]}'
curl -XGET http://localhost:9200/test/multi/_search?q=data:one
curl -XPUT localhost:9200/test/multi/1 -d '{"data" : ["two","three","㭟 䂖"]}'
curl -XGET http://localhost:9200/test/multi/_search -d '{
    "query" : {
        "term" : { "data": "㭟" }
    }
}'

WURFL

Index can be in memory! (for wurfl??)
http://www.elasticsearch.org/blog/2010/02/16/searchengine_time_machine.html

$ curl -XPUT http://localhost:9200/twitter/ -d '
index :
    store:
        type : memory



HEALTH

curl -XGET http://localhost:9200/_cluster/health/atpic?level=cluster&pretty=1'
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 5,
  "active_shards" : 5,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 5
}





 curl -XGET http://localhost:9200/_cluster/health/atpic?level=indices&pretty=1'
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 5,
  "active_shards" : 5,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 5,
  "indices" : {
    "atpic" : {
      "status" : "yellow",
      "number_of_shards" : 5,
      "number_of_replicas" : 1,
      "active_primary_shards" : 5,
      "active_shards" : 5,
      "relocating_shards" : 0,
      "initializing_shards" : 0,
      "unassigned_shards" : 5
    }
  }


 curl -XGET http://localhost:9200/_cluster/health/atpic?level=shards&pretty=1'
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 5,
  "active_shards" : 5,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 5,
  "indices" : {
    "atpic" : {
      "status" : "yellow",
      "number_of_shards" : 5,
      "number_of_replicas" : 1,
      "active_primary_shards" : 5,
      "active_shards" : 5,
      "relocating_shards" : 0,
      "initializing_shards" : 0,
      "unassigned_shards" : 5,
      "shards" : {
        "0" : {
          "status" : "yellow",
          "primary_active" : true,
          "active_shards" : 1,
          "relocating_shards" : 0,
          "initializing_shards" : 0,
          "unassigned_shards" : 1
        },
        "1" : {
          "status" : "yellow",
          "primary_active" : true,
          "active_shards" : 1,
          "relocating_shards" : 0,
          "initializing_shards" : 0,
          "unassigned_shards" : 1
        },
        "2" : {
          "status" : "yellow",
          "primary_active" : true,
          "active_shards" : 1,
          "relocating_shards" : 0,
          "initializing_shards" : 0,
          "unassigned_shards" : 1
        },
        "3" : {
          "status" : "yellow",
          "primary_active" : true,
          "active_shards" : 1,
          "relocating_shards" : 0,
          "initializing_shards" : 0,
          "unassigned_shards" : 1
        },
        "4" : {
          "status" : "yellow",
          "primary_active" : true,
          "active_shards" : 1,
          "relocating_shards" : 0,
          "initializing_shards" : 0,
          "unassigned_shards" : 1
        }
      }
    }
  }
}


 curl -XGET http://localhost:9200/_cluster/nodes?pretty=1'
{
  "ok" : true,
  "cluster_name" : "elasticsearch",
  "nodes" : {
    "gfH0mZqSRTum5UmSYzzn6w" : {
      "name" : "Abominable Snowman",
      "transport_address" : "inet[acer/127.0.1.1:9300]",
      "hostname" : "acer",
      "http_address" : "inet[acer/127.0.1.1:9200]"
    }
  }
}


curl -XGET http://localhost:9200/_cluster/nodes?all=true&pretty=1'
{
  "ok" : true,
  "cluster_name" : "elasticsearch",
  "nodes" : {
    "gfH0mZqSRTum5UmSYzzn6w" : {
      "name" : "Abominable Snowman",
      "transport_address" : "inet[acer/127.0.1.1:9300]",
      "hostname" : "acer",
      "http_address" : "inet[acer/127.0.1.1:9200]",
      "settings" : {
        "path.logs" : "/var/log/elasticsearch",
        "path.work" : "/tmp/elasticsearch",
        "path.conf" : "/etc/elasticsearch",
        "path.data" : "/var/lib/elasticsearch",
        "config" : "/etc/elasticsearch/elasticsearch.yml",
        "path.home" : "/usr/share/elasticsearch",
        "pidfile" : "/var/run/elasticsearch.pid",
        "logger.prefix" : "",
        "name" : "Abominable Snowman",
        "cluster.name" : "elasticsearch"
      },
      "os" : {
        "refresh_interval" : 1000,
        "cpu" : {
          "vendor" : "Intel",
          "model" : "Atom(TM) CPU N450   @ 1.66GHz",
          "mhz" : 1666,
          "total_cores" : 2,
          "total_sockets" : 1,
          "cores_per_socket" : 2,
          "cache_size" : "512b",
          "cache_size_in_bytes" : 512
        },
        "mem" : {
          "total" : "992.1mb",
          "total_in_bytes" : 1040359424
        },
        "swap" : {
          "total" : "1.8gb",
          "total_in_bytes" : 2031087616
        }
      },
      "process" : {
        "refresh_interval" : 1000,
        "id" : 2754,
        "max_file_descriptors" : 65535
      },
      "jvm" : {
        "pid" : 2754,
        "version" : "1.7.0_03",
        "vm_name" : "OpenJDK 64-Bit Server VM",
        "vm_version" : "22.0-b10",
        "vm_vendor" : "Oracle Corporation",
        "start_time" : 1350640206157,
        "mem" : {
          "heap_init" : "256mb",
          "heap_init_in_bytes" : 268435456,
          "heap_max" : "247.5mb",
          "heap_max_in_bytes" : 259522560,
          "non_heap_init" : "23.1mb",
          "non_heap_init_in_bytes" : 24313856,
          "non_heap_max" : "214mb",
          "non_heap_max_in_bytes" : 224395264,
          "direct_max" : "247.5mb",
          "direct_max_in_bytes" : 259522560
        }
      },
      "thread_pool" : {
        "generic" : {
          "type" : "cached",
          "keep_alive" : "30s"
        },
        "index" : {
          "type" : "cached",
          "keep_alive" : "5m"
        },
        "get" : {
          "type" : "cached",
          "keep_alive" : "5m"
        },
        "cache" : {
          "type" : "scaling",
          "min" : 1,
          "max" : 4,
          "keep_alive" : "5m"
        },
        "snapshot" : {
          "type" : "scaling",
          "min" : 1,
          "max" : 5,
          "keep_alive" : "5m"
        },
        "merge" : {
          "type" : "scaling",
          "min" : 1,
          "max" : 20,
          "keep_alive" : "5m"
        },
        "bulk" : {
          "type" : "cached",
          "keep_alive" : "5m"
        },
        "flush" : {
          "type" : "scaling",
          "min" : 1,
          "max" : 10,
          "keep_alive" : "5m"
        },
        "search" : {
          "type" : "cached",
          "keep_alive" : "5m"
        },
        "percolate" : {
          "type" : "cached",
          "keep_alive" : "5m"
        },
        "management" : {
          "type" : "scaling",
          "min" : 1,
          "max" : 5,
          "keep_alive" : "5m"
        },
        "refresh" : {
          "type" : "scaling",
          "min" : 1,
          "max" : 10,
          "keep_alive" : "5m"
        }
      },
      "network" : {
        "refresh_interval" : 5000,
        "primary_interface" : {
          "address" : "0.0.0.0",
          "name" : "wlan0",
          "mac_address" : "00:26:C7:CA:1F:C6"
        }
      },
      "transport" : {
        "bound_address" : "inet[/0:0:0:0:0:0:0:0:9300]",
        "publish_address" : "inet[acer/127.0.1.1:9300]"
      },
      "http" : {
        "bound_address" : "inet[/0:0:0:0:0:0:0:0:9200]",
        "publish_address" : "inet[acer/127.0.1.1:9200]"
      }
    }
  }
}



curl -XGET 'http://localhost:9200/atpic/_segments?pretty=1'
{
  "ok" : true,
  "_shards" : {
    "total" : 10,
    "successful" : 5,
    "failed" : 0
  },
  "indices" : {
    "atpic" : {
      "shards" : {
        "0" : [ {
          "routing" : {
            "state" : "STARTED",
            "primary" : true,
            "node" : "gfH0mZqSRTum5UmSYzzn6w"
          },
          "num_committed_segments" : 0,
          "num_search_segments" : 0,
          "segments" : { }
        } ],
        "1" : [ {
          "routing" : {
            "state" : "STARTED",
            "primary" : true,
            "node" : "gfH0mZqSRTum5UmSYzzn6w"
          },
          "num_committed_segments" : 0,
          "num_search_segments" : 0,
          "segments" : { }
        } ],
        "2" : [ {
          "routing" : {
            "state" : "STARTED",
            "primary" : true,
            "node" : "gfH0mZqSRTum5UmSYzzn6w"
          },
          "num_committed_segments" : 0,
          "num_search_segments" : 0,
          "segments" : { }
        } ],
        "3" : [ {
          "routing" : {
            "state" : "STARTED",
            "primary" : true,
            "node" : "gfH0mZqSRTum5UmSYzzn6w"
          },
          "num_committed_segments" : 0,
          "num_search_segments" : 0,
          "segments" : { }
        } ],
        "4" : [ {
          "routing" : {
            "state" : "STARTED",
            "primary" : true,
            "node" : "gfH0mZqSRTum5UmSYzzn6w"
          },
          "num_committed_segments" : 0,
          "num_search_segments" : 0,
          "segments" : { }
        } ]
      }
    }
  }
}





LOGS

'
ROUTING














RANDOM
http://elasticsearch-users.115913.n3.nabble.com/Random-sorting-td3486880.html
http://www.elasticsearch.org/guide/reference/api/search/sort.html

{"query":{"custom_score":{"script":"random()*20","query":{"query_string":{"default_field":"_all", "default_operator":"AND","query":"майка~0.7"}},"size":10}},"sort":{"_score":{"order":"desc"}}}

https://github.com/elasticsearch/elasticsearch/issues/1170
I have implemented this by storing set of "random" numbers e.g. each object has say 20 additional integers (each one of these is a sorting field named as rand1, rand2, rand3 etc). For each user I select (calculate based on date and UA) number 1...20 which is used to select which "random" field will be used. When new objects are added each simply receives set of random. Umbers. You decide how many random states you need. Remember that reverse order in this case doubles the number of random states. This solution is all about perception.







http://www.elasticsearch.org/blog/2011/03/24/new-search-types.html



count

The first is the count search type. It allows to get back the total number of hits matching a query, with the ability to have facets configured in an optimized (implementation wise and performance wise) manner. For example:

curl -XGET 'http://localhost:9200/twitter/tweet/_search?search_type=count' -d '{
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

The result will not include any hits, just the total_hits and optional facets results.



scan

The new scan type allows to scroll a very large result set in an optimized manner.





http://jontai.me/blog/2012/10/using-elasticsearch-to-speed-up-filtering/

Use filters instead of queries — From the elasticsearch Query DSL documentation:

    Filters are very handy since they perform an order of magnitude better than plain queries since no scoring is performed and they are automatically cached.

    Filters can be a great candidate for caching. Caching the result of a filter does not require a lot of memory, and will cause other queries executing against the same filter (same parameters) to be blazingly fast.

We don’t care about scoring, so we use a match_all query and encode the rest of the search criteria as filters.

Disable the _source field ‐ To enable highlighting of results, elasticsearch stores a pristine copy of each indexed document by default. If you don’t plan on doing highlighting or retrieving entire documents from elasticsearch, disable the _source field to save space in the index.

In one of our smaller indexes, disabling the _source field reduced the index size by 58% (953.5mb to 399.9mb).

Disable the _all field ‐ To make searching more convenient, elasticsearch combines all searchable fields into a hidden _all field by default. If you don’t specify a field to search, queries will be made against the _all field. If you’re always going to specify the field to filter against, disable the _all field to save space in the index.

In the same index I mentioned earlier, disabling the _all field reduced the index size by another 30% (399.9mb to 276.5mb).


{
    "filtered" : {
        "query" : {
            "term" : { "tag" : "wow" }
        },
        "filter" : {
            "range" : {
                "age" : { "from" : 10, "to" : 20 }
            }
        }
    }
}

The filter object can hold only filter elements, not queries. Filters can be much faster compared to queries since they don’t perform any scoring, especially when they are cached.


http://elasticsearch-users.115913.n3.nabble.com/Filters-vs-Queries-td3219558.html

Here are 3 variations:

* Query only:

   { query: { text: {  _all: "foo bar" }}}


* Filter only:

   { query: {
         constant_score: {
             filter: {  term: { status: "open" }}
         }
   }}

* Query and Filter:

   { query: {
         filtered: {
             query:  {  text: { _all:   "foo bar"}}
             filter: {  term: { status: "open" }}
         }
   }}


So:
---
1) You always need wrap your query in a top-level query element
2) A "constant_score" query says "all docs are equal", so no scoring
   has to happen - just the filter gets applied
3) In the third example, filter reduces the number of docs that
   can be matched (and scored) by the query 

====
Is there a performance difference between using a constant scored
query and a filtered query?  All of our current queries are generated
as filtered queries and I'm concerned that this might be slower than
the constant score method.  Examples:

* Constant Score:
   { query: {
         constant_score: {
             filter: {  term: { status: "open" }}
         }
   }}

* Filtered Query
   { query: {
         filtered: {
             query:  { match_all: {} } ,
             filter: {  term: { status: "open" }}
         }
   }} 

A filtered query with a match_all query is automatically converted internally to a constant_score one, so guess which one is better? :)
=====================
http://www.elasticsearch.org/guide/reference/api/search/from-size.html

Though can be set as request parameters, they can also be set within the search body. from defaults to 0, and size defaults to 10.

{
    "from" : 0, "size" : 10,
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}

 curl -s -XPOST localhost:9200/atpic/pic/_bulk --data-binary @bulk.json


========================


curl -XPUT http://localhost:9200/atpic/test/1 -d '{
    "title" : "Some Title",
    "text" : "Some Description"
}'

curl localhost:9200/atpic/test/1


curl -XPUT http://localhost:9200/atpic/test/1 -d '{
    "title" : "Some Title2"
}'

curl -XPOST http://localhost:9200/atpic/test/1/_update -d '{
    "title" : "Some Title2"
}'


===========integers=======
curl -XGET 'localhost:9200/atpic/_analyze?field=pic.rand_1&pretty=1' -d '61308'

2^63
9223372036854775808

 curl -XGET'localhost:9200/atpic/_analyze?field=pic.rand_1&pretty=1' -d '-9223372036854775808'

curl -XGET'localhost:9200/atpic/_analyze?field=pic.rand_1&pretty=1' -d '-9223372036854775809'
{
  "error" : "NumberFormatException[For input string: \"-9223372036854775809\"]",
  "status" : 500


curl -XGET'localhost:9200/atpic/_analyze?field=pic.rand_1&pretty=1' -d '9223372036854775807'
OK
curl -XGET'localhost:9200/atpic/_analyze?field=pic.rand_1&pretty=1' -d '9223372036854775808'
{
  "error" : "NumberFormatException[For input string: \"9223372036854775808\"]",
  "status" : 500
}
