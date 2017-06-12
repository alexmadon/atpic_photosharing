# py3k version
"""
this populate the memcache db with the SQL hosts
"""
import atpic.memcached3 as mc
# import atpic.database
import postgresql

db = postgresql.open("pq://dbuser:dbpass@localhost/dbname")
# this needs to be retrieved from a config (zookeeper)
conmc=mc.connect()
#
def get_servershot():
    # need to have servershort not null and not ''
    name_sel=db.prepare("select artist.id,artist.servershort, artist.admin_login,storing.serverip, storing.servername from artist join storing on storing.id=artist.storefrom order by id limit 10000")
    with db.xact():
        for row in name_sel():
            print(row)
            mc.set(conmc,"s:%s"%row["servershort"],row["serverip"])
            a=mc.get(conmc,"s:%s"%row["servershort"])
            print(a)

if __name__ == "__main__":
    print("populating memcache with DNS")
    get_servershot()
