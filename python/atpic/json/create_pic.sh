# atpic index
curl -XDELETE localhost:9200/atpic
curl -XPOST localhost:9200/atpic -d '{
    "settings" : {
        "number_of_shards" : 5
    }
}'
curl "localhost:9200/atpic/_settings?pretty=1"
# curl -XDELETE localhost:9200/atpic/pic
curl -XPUT 'http://localhost:9200/atpic/pic/_mapping' -d @schema_pic.json

curl "http://localhost:9200/atpic/pic/_mapping?pretty=1"

# curl -XPUT http://localhost:9200/atpic/pic/2522516 -d @pic2522516.json



#
# path and vpath indexes are used to get once only eahc path
# in a separate index (used for facetting)
# pic index cannot be use as one path may contain more than one pic
# if N pics are in path, then we just override N times that path
# in path index
# we could use SQL, but that would lead to having the same information
# stored more than one time (full path + splitted path)
#

curl -XPUT 'http://localhost:9200/atpic/path/_mapping' -d @schema_path.json
curl "http://localhost:9200/atpic/path/_mapping?pretty=1"



curl -XPUT 'http://localhost:9200/atpic/vpath/_mapping' -d @schema_vpath.json
curl "http://localhost:9200/atpic/vpath/_mapping?pretty=1"

