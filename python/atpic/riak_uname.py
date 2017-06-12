import atpic.database

con = atpic.database.connect()

def get_users(con):
    query="select id,servershort from artist order by id"
    listofdict=atpic.database.query(query, con)
    rows=len(listofdict)
    output=[] # we will store in a list (more efficient that a string)
    output.append("<add>")
    for thedict in listofdict:
        print thedict


# get the unames from SQL
# print """curl -X PUT -d "{\"id\":\"%s\"}" -H "Content-Type: application/json" -H "%s" "http://127.0.0.1:8098/riak/gallery/%s?returnbody=true" """ % (j,Linkj,j)

get_users(con)
