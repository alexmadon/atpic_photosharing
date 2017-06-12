#!/usr/bin/python3

# we add a '_user' column to each table below user:
# this can help in database partitionning and database clustering

import atpic.libpqalex
import atpic.cleaner
import types
import time
import difflib
import atpic.mybytes
import atpic.log

xx=atpic.log.setmod("INFO","sql_pop")
query=b"""UPDATE _user_gallery_pic SET _pathstore='o/'||_user::text||'/'||_gallery::text||'/0/'||id::text||'/0.'||_extension WHERE _user=$1"""
import atpic.libpqalex
import atpic.cleaner
import types
import difflib
import atpic.mybytes
import atpic.log

xx=atpic.log.setmod("INFO","sql_cleanB")
db=atpic.libpqalex.db()

ps=atpic.libpqalex.pq_prepare(db,b'',query)
maxuser=12803
for i in range(0,maxuser):
    print("echo doing user",i,"/",maxuser)
    uid=atpic.mybytes.int2bytes(i)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',(uid,))
    print(result)
    result=atpic.libpqalex.process_result(result)
    print(result)
