#!/usr/bin/python3
# this cleans the database and ensure there is a unique filename per gallery
# the we need to add the constraint on filename
# then we need to put a limit on the number of files per gallery

# http://stackoverflow.com/questions/1746213/how-to-delete-duplicate-entries-in-postgresql
# DELETE FROM user_accounts USING user_accounts ua2
#  WHERE user_accounts.email = ua2.email AND user_account.id < ua2.id;

import atpic.libpqalex
import re
import atpic.mybytes

if __name__ == "__main__":
    db=atpic.libpqalex.db()

    query=b"""WITH duplicates AS (
    SELECT count(_gallery),_gallery,_originalname FROM _user_gallery_pic WHERE _gallery > $1 AND _gallery <= $2 GROUP by _gallery,_originalname HAVING count(_gallery)>1
)
UPDATE _user_gallery_pic SET _originalname=coalesce('_'||id::text||'.'||_extension) FROM duplicates WHERE _user_gallery_pic._gallery=duplicates._gallery AND _user_gallery_pic._originalname=duplicates._originalname
"""

    # Sep 10 17:13:51 localhost ﻿21062-libpqalex.process_result: DEBUG rowcount 0
    # Sep 10 17:13:51 localhost ﻿21062-libpqalex.process_result: DEBUG rowcount 0
    
    # root@acer:~# tail -f /var/log/user.log|grep rowcount

    print("sending",query)
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    for i in range(0,1000):
        afrom=atpic.mybytes.int2bytes(i*100)
        ato=atpic.mybytes.int2bytes((i+1)*100)
        print('doing gallery id', afrom, 'to', ato)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',(afrom,ato))
        result=atpic.libpqalex.process_result(result)

    print('Thanks!')
    print('Now you can create the UNIQUE contraint on file names in galleries')
