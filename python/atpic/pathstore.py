#!/usr/bin/python3

import datetime

import atpic.log


xx=atpic.log.setmod("INFO","pathstore")


def forge_pathstore(uid,pic,resolution,extension):
    # create a new pathstore
    # not idempotent
    yy=atpic.log.setname(xx,'forge_pathstore')
    atpic.log.debug(yy,'input=',uid,pic,resolution,extension)
    datetimefirst=datetime.datetime.now()
    # store at: year / month / day / hour / minute
    dirpath=b'n/'+datetimefirst.strftime("%Y/%m/%d/%H/%M").encode('utf8')
    # use that datetimeobject to create a path
    atpic.log.debug(yy,'dirpath=',dirpath)
    # extension="jpg"
    # does NOT depend on gallery ID (faster moves)
    filename=uid+b"_"+pic+b"_"+resolution+b"."+extension
    pathstore=dirpath+b"/"+filename
    atpic.log.debug(yy,"output=",pathstore)
    return pathstore

# note the is also the equivalent in SQL in forgesql.py
# select 'n/'||extract(YEAR from now())||'/'||lpad(extract(MONTH from now())::text,2,'0')||'/'||lpad(extract(DAY from now())::text,2,'0')||'/'||lpad(extract(hour from now())::text,2,'0')||'/'||lpad(extract(minute from now())::text,2,'0')||'/'||'.bin';

if __name__ == "__main__":
    uid=b'1'
    pic=b'999'
    resolution=b'1024'
    extension=b'jpg'
    pathstore=forge_pathstore(uid,pic,resolution,extension)
    print(pathstore)
