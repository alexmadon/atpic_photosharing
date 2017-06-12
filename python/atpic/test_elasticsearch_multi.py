#!/usr/bin/python3
import time
import atpic.zmq_elastic_client
def test():
    # compare the speed of one Multi of N queries
    # vs N single queries
    t1=time.time()
    maxi=10
    ajson=b'{ "query" : {"term": {"uid":1}}, "size" : 10}'
    for i in range(0,maxi):
        uri='/atpic/pic/_search?routing=1'
        content=atpic.zmq_elastic_client.http_general(essock,b'GET',uri,ajson)
        print((status,content))
    t2=time.time()
    print('ONE',t2-t1)
    # print(content)
    ajson_list=list()
    for i in range(0,maxi):
        ajson_list.append(b'{"index" : "atpic", "type" : "pic", "routing": "1"}')
        ajson_list.append(b'{ "query" : {"term": {"uid":1}}, "size" : 10}')
    t1b=time.time()
    ajson=b'\n'.join(ajson_list)
    uri='/atpic/pic/_msearch?routing=1'
    content=atpic.zmq_elastic_client.http_general(essock,b'GET',uri,ajson)
    t2b=time.time()
    # print(content)
    print('TWO',t2b-t1b)

    print('ONE',t2-t1)

if __name__ == "__main__":
    test()
