# inteceptor
# solr results gives uid,gid,pid
# to get the uid to server mapping we do that at another layer
# (probably SQL or Riak but SQL seems faster that 100 riak calls)
# we need that in two case:
# 1) a user is moved to another server
# 2) a server is down and we use a back server for all the users on the dead serrver

# NEW: this interceptor idea is a bit too complex
# it is better to rely on DNS
# and have solr return URL with no IP but with domain names
# see idbased.py:
# http://u11.direct.atpic.com/222/p/3333_1024_2012_12_31_23_59.jpg 
