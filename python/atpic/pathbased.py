#!/usr/bin/python3
"""
Path utilities:
converts path to gallery
gallery to path, etc...


cache is stored in two classes:
1) the directory tree for one user in one redis hash
2) for each gallery, one redis hash storing the pictures details
(lists are not cached and are gotten from SQL (faster?)) 


NEW:
we have no path anymore: we use SQL regex for list of dirs

select id,_path from _user_gallery where _user=1;
select id,_path from _user_gallery where _user=1 and _path ~ 'ita.*';
select id,_path from _user_gallery where _user=1 and _path ~ '^ita[^/]+$';

"""
# import logging
import datetime
import traceback
import time

import atpic.log
import atpic.libpqalex
import atpic.forgesql
from atpic.redisconst import *


xx=atpic.log.setmod("INFO","pathbased")


# ===================
# NEW 
# ===================



def path_split(path):
    # splits alex/avignon/dama/pont.jpg
    # into (alex,avignon/dama,pont.jpg) pathuser,path,picture
    yy=atpic.log.setname(xx,'path_split')
    atpic.log.debug(yy,path)
    if path==b'/':
        atpic.log.debug(yy,'slashtype')
        return (b's',()) # s=slash
    splitted=path.split(b'/')

    atpic.log.debug(yy,splitted)
    if len(splitted)==2:
        atpic.log.debug(yy,'usertype')
        return (b'u',(splitted[1],))
    pathuser=splitted[1]
    plist=[pathuser]
    try:
        # atpic.log.debug(yy,'dot?',splitted[-1][-4:-3])
        if splitted[-1][-4:-3]==b'.': # extension .jpg
            atpic.log.debug(yy,'this is a pic')
            pathdir=b'/'+b'/'.join(splitted[2:-1])
            pathfile=splitted[-1]
            ptype=b'p'
            plist.append(pathdir)
            plist.append(pathfile)
        else:
            atpic.log.debug(yy,'this is a gallery')
            pathdir=b'/'+b'/'.join(splitted[2:])
            pathfile=b''
            plist.append(pathdir)
            ptype=b'g'

    except:
        atpic.log.debug(yy,'except2')
        pathdir=b'/'+b'/'.join(splitted[1:])
        pathfile=b''
        plist.append(pathdir)
        ptype=b'g'
    ptuple=tuple(plist)
    atpic.log.debug(yy,ptype,ptuple)
    return (ptype,ptuple)



if __name__ == "__main__":

    paths=(
        b'/alexmadon/avignon/dama',
        b'/alexmadon/avignon/dama/pint.jpg',
        b'/alexmadon/pint.jpg',
        b'/alexmadon',
        b'/',
        )
    for path in paths:
        print(path,'->',path_split(path))
