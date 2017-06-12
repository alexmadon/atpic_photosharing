# root
# gallery
#      g1100       g1110        g1111
# 1000 ----> 1100  ----->  1110 ----->    1111
#            1200
#            1300
# 
# 
# 
# 2000 ----> 2100
#            2200
# 
# 3000
# 
# QUERY:
# curl http://127.0.0.1:8098/riak/gallery/1000/gallery,g1100,0/gallery,g1110,0/gallery,g1111,1
import string

for i in range(1000,10000,1000):
    print "# i=%s" % i
    linki=[]
    for j in range(i+100,i+1000,100):
        print "# j=  %s" % j
        linkj=[]
        for k in range(j+10,j+100,10):
            print "# k=    %s" % k
            linkk=[]
            for l in range(k+1,k+10,1):
                print "# l=      %s" % l
                print """curl -X PUT -d "{\"id\":\"%s\"}" -H "Content-Type: application/json" "http://127.0.0.1:8098/riak/gallery/%s?returnbody=true" """ % (l,l)
                linkk.append(""" </riak/gallery/%s>; riaktag=\\"g%s\\" """ % (l,l))
                Linkk="Link: "+",".join(linkk)
            print """curl -X PUT -d "{\"id\":\"%s\"}" -H "Content-Type: application/json" -H "%s" "http://127.0.0.1:8098/riak/gallery/%s?returnbody=true" """ % (k,Linkk,k)



            linkj.append(""" </riak/gallery/%s>; riaktag=\\"g%s\\" """ % (k,k))
            Linkj="Link: "+",".join(linkj)
        print """curl -X PUT -d "{\"id\":\"%s\"}" -H "Content-Type: application/json" -H "%s" "http://127.0.0.1:8098/riak/gallery/%s?returnbody=true" """ % (j,Linkj,j)


        linki.append(""" </riak/gallery/%s>; riaktag=\\"g%s\\" """ % (j,j))
        Linki="Link: "+",".join(linki)
    print """curl -X PUT -d "{\"id\":\"%s\"}" -H "Content-Type: application/json" -H "%s" "http://127.0.0.1:8098/riak/gallery/%s?returnbody=true" """ % (i,Linki,i)
