import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.set('foo', 'bar')   # or r['foo'] = 'bar'
# r.get('foo')   # or r['foo']
# for i in range(1,10000):
#     key='ke%s'%i
#     r.set(key,i)


for i in range(1,10000):
    key='ke%s'%i
    a=r.get(key)
