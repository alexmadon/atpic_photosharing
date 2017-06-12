#!/usr/bin/python3

import atpic.log
import atpic.libpqalex

"""
keeps a db connection young (less that MAX requests)
init with (None,0)
"""

xx=atpic.log.setmod("INFO","connection_young")



def get_db(db,dbcounter):
    yy=atpic.log.setname(xx,'get_db')
    # global dbcounter
    # global db
    maxc=30 # MAX
    dbcounter=dbcounter+1
    atpic.log.debug(yy,'dbcounter=',dbcounter)
    if not db:
        atpic.log.debug(yy,'no db connection, creating one')
        db=atpic.libpqalex.db_native()
    elif dbcounter>maxc: # do maxc requests per connnection
        atpic.log.debug(yy,'db connection too old, creating a new one')
        atpic.libpqalex.close(db)
        db=atpic.libpqalex.db_native()
        dbcounter=0
    else:
        try:
            query=b'SELECT version()'
            result=atpic.libpqalex.pq_exec_params(db,query,[])
            atpic.log.debug(yy,'result1',result)
            result=atpic.libpqalex.process_result(result)
            atpic.log.debug(yy,'result2',result)
        except:
            atpic.log.debug(yy,'DB IS DEAD!, try to restart')
    atpic.log.debug(yy,'will return db=',db)
    return (db,dbcounter)


if __name__ == "__main__":
    dbcounter = 0
    db=None
    for i in range(0,33):
        (db,dbcounter)=get_db(db,dbcounter)
