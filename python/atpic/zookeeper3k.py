#!/usr/bin/python3
# attempts of a 3k ctypes module
#  libzookeeper2
import ctypes
libzk = ctypes.CDLL("libzookeeper_mt.so.2")

# need to install packages:
# libzookeeper2
# libzookeeper-dev
# /usr/include/c-client-src/zookeeper.h
# h2xml.py   /usr/include/c-client-src/zookeeper.h -o zookeeper.xml
# xml2py.py zookeeper.xml -o zookeeper.py
# https://github.com/ce/ruby-zookeeper
# A Ruby FFI binding for the Apache ZooKeeper C API library. 

# https://github.com/myelin/zookeeper_client
# https://github.com/smingins/zookeeper
# see ce-ruby-zookeeper-cd083c5/lib/zookeeper/zookeeper.rb
# @zk_handle = zookeeper_init(args[:host], args[:watcher], args[:timeout], args[:session_id], nil, 0)

# root@amadon:/usr/local/zookeeper-3.3.1/src/c/tests# grep zookeeper_init *


# see:
# /usr/local/zookeeper-3.3.1/contrib/zkpython3/src/test
# /usr/local/zookeeper-3.3.1/contrib/zkpython3/src/c

# zh=libzk.zookeeper_init(b"127.0.0.1:2121",0,10000,0,0,0)
zh=libzk.zookeeper_init(b"127.0.0.1:2181",0,10000,0,0,0)
print(zh)
state=libzk.zoo_state(zh)
print(state)
# zoo_acreate(@zk_handle, args[:path], args[:data], data_len, args[:acl], flags, args[:callback].proc, YAML.dump(args[:context]))


rc = libzk.zoo_acreate(zh, b"/child3",b"", 0, &ZOO_OPEN_ACL_UNSAFE, 0,create_completion_fn, 0);

libzk.zookeeper_close(zh)
